""""
Author: Shanmugarajan

This is a simple generic REST client. 
Currently it doesn't support authentication (avoided it for simplicity)
but we can implement a authenticator class based on the authentication needed in the server

If you run this file then it will get the data from the following url and will print it.

Top 250 ULR: http://www.myapifilms.com/imdb/top 
Bottom 100 ULR: http://www.myapifilms.com/imdb/bottom 
In Theaters ULR: http://www.myapifilms.com/imdb/inTheaters 
Coming Soon ULR: http://www.myapifilms.com/imdb/comingSoon 


redirect the output to a file for clean screen.
python api_client.py > output.txt

"""


import requests
import functools
import json

class APIError(Exception):

    def __init__(self, status_code, reason):
        self.errno = status_code
        self.msg   = reason

    def __str__(self):
        return '%s: %s' % (self.errno, self.msg)


class HttpRequester(object):

    def __init__(self, baseurl, authenticator, session=None):

        self.baseurl = baseurl.rstrip('/')
        self.authenticator = authenticator
        self.session = session if session else requests.Session()
        self.session.verify = False

    def _build_url(self, path, params):

        params['baseurl'] = self.baseurl
        params['path']    = path.rstrip('/')
        return '{baseurl}{path}'.format(**params)

    def _make_request(self, method, url, data=None, files=None ):

        #headers = self.authenticator.get_headers()
        #print 'Calling url %s method %s ' % (url, method)
        headers = {}

        if method in ('delete', 'patch'):
            response = self.session.request(method = method, url = url, headers = headers)
        elif method == 'get':
            response = self.session.get(url=url, headers=headers, stream=True)
        elif method == 'post':
            response = self.session.post(url = url, headers = headers, data=data, files=files)
        elif method == 'put':
            response = self.session.put(url = url, headers = headers, data=data)

        return response

    def _send_raw_response(self, response):
        if response.ok:
            return response
        else:
            raise APIError(response.status_code, response.raw.reason)

    def _send_response(self, response):

        try:
            response = self._send_raw_response(response)
            content = ''.join(list(response.iter_content(chunk_size=512*1024)))
            json_obj = json.loads(content)
            return json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return response.content

    def get_raw(self, path, **kwargs):

        url = self._build_url(path, kwargs)
        response = self._make_request('get', url)

        # just create a new http session for subsequent api calls.
        if kwargs.get('new_session', None) :
            self.session = requests.Session()
            self.session.verify = False

        return self._send_raw_response(response)

    def get(self, path, **kwargs):
        response = self.get_raw(path, **kwargs)
        return self._send_response(response)

    def post(self, path, data, files=None, **kwargs):
        url = self._build_url(path, kwargs)
        if files:
            response = self._make_request('post', url = url, data = data, files=files)
        else:
            response = self._make_request('post', url = url, data = data)

        return self._send_response(response)

    def delete(self, path, **kwargs):

        url = self._build_url(path, kwargs)
        response = self._make_request('delete', url = url)
        return self._send_response(response)

    def put(self, path, data, id, **kwargs):
        kwargs.update({'id' : id})
        url = self._build_url(path, kwargs)
        response = self._make_request('put', url = url, data = data)
        return self._send_response(response)

    def patch(self, path, id, **kwargs):
        kwargs.update({'id' : id})
        url = self._build_url(path, kwargs)
        response = self._make_request('patch', url = url)
        return self._send_response(response)

    def get_api(self, path):
        api_docs = self.get('/documentation/%s' % path.strip('/'))
        return api_docs.get('apis', {})


class APIClient(object):
    def __init__(self, baseurl, authenticator):
        self.path       = '/'
        self.baseurl    = baseurl.rstrip('/')
        self.requester = HttpRequester(baseurl, authenticator)
        self.resources = {}

    def __getattr__(self, name):
        if name not in self.resources:
            self.resources[name] = Resource(name, self.requester)
        return self.resources[name]

class Resource(object):

    def __init__(self, name, requester, parent=None):
        self.path = '%(parent)s/%(name)s' % {'parent' : parent.path if parent else '', 'name': name}
        self.requester = requester

    def __call__(self, **kwargs):
        # this gets called, for example, as api.channels.insert.post() which would 
        # translate to /channels/insert POST
        assert(len(kwargs)==1)
        return Resource(kwargs.values()[0], self.requester, parent=self)

    def __getattr__(self, attr_name):
        if attr_name in ('get', 'post', 'put', 'delete'):
            http_method = getattr(self.requester, attr_name)
            return functools.partial(http_method, path=self.path)
        else:
            return Resource(attr_name, self.requester, parent=self)


if __name__ == "__main__":

    api = APIClient("http://www.myapifilms.com/", None)
    print api.imdb.top.get()
    print "**"*40
    print api.imdb.bottom.get()
    print "**"*40
    print api.imdb.inTheaters.get()
    print "**"*40
    print api.imdb.comingSoon.get()


