""" Authenticator class implementation This authenticator object shall be the object to get the authentication
This will implement different OAuth2 authentication flows

"""
import time
import random
import string
import base64
import hashlib
import hmac
import logging
import simplejson as json

import requests

log = logging.getLogger()

class Authenticator(object):

    def __init__(self, access_token, client_id, client_secret, host_url, refresh_token, client_ip=None):
        self.access_token   = access_token
        self.client_id      = client_id
        self.client_secret  = client_secret
        self.refresh_token  = refresh_token
        self.host_url       = host_url
        self._user_agent    = 'Accellion EAPI python client'
        self.client_ip      = client_ip

    @classmethod
    def from_user_password_auth_flow(cls, host_url, username, password, client_secret, client_key):
        params = {
                    'grant_type':'authorization_code',
                    'code':code,
                    'client_id':client_key,
                    'client_secret':client_secret                    
                }

        resp = requests.post("%s%s" % (host_url, ,"oauth2/token"))
        if resp

        return r['access_token']


    @classmethod
    def from_signature_based_auth(cls, host_url, email, client_id, client_secret, sig_key, scope, redirect_uri, client_ip=None):
        log.info("Getting a token using signature based auth")
        authorize_url = host_url + "oauth/token"
        redirect_uri  = host_url + redirect_uri

        timestamp = str(int(time.time()))
        nonce = ''.join(random.choice(string.digits) for x in range(6))

        text   = '|@@|'.join([ client_id, email, timestamp, nonce ])
        digest = hmac.new(str(sig_key), text, hashlib.sha1).hexdigest()

        code_param = '|@@|'.join([ base64.b64encode(client_id),
                                   base64.b64encode(email),
                                   timestamp, nonce, digest ])

        payload = { 'client_id'     : client_id,
                    'client_secret' : client_secret,
                    'code'          : code_param,
                    'grant_type'    : 'authorization_code',
                    'redirect_uri'  : redirect_uri,
                    'scope'         : scope
                  }

        log.info("payload content is %s", payload)
        response = requests.post(authorize_url, verify=False, data=payload)
        if response.ok:
            log.info("response content is %s", response.content)
            try:
                resp_dict = json.loads(response.content)
                if resp_dict.get('access_token', None):
                    access_token = resp_dict['access_token']
                    refresh_token = resp_dict['refresh_token']
                    obj = cls(access_token, client_id, client_secret, host_url, refresh_token, client_ip=client_ip)
                    return obj
            except (json.JSONDecodeError, TypeError):
                log.error('Error while decoding the json content:%s', response.text)
                raise Exception(403, 'Not able to get the oauth token')

        log.error('Error while getting access token %s ', response.text)
        raise Exception(403, 'Not able to get the oauth token')

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value


    def _refresh_token(self):

        authorize_url = self.host_url + "oauth/token"

        payload = {
            'client_id'     : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type'    : 'refresh_token',
            'refresh_token' : self.refresh_token
          }

        response = requests.post(authorize_url, verify=False, data=payload)
        if response.ok:
            try:
                resp_dict = json.loads(response.content)
                log.info(' response %s ' % str(resp_dict))
                if resp_dict.get('access_token', None):
                    self.access_token = resp_dict['access_token']
                    return True

            except (json.JSONDecodeError, TypeError):
                raise Exception(403, 'Unable to do rauthentication')

        log.error('Failed to refresh authentication %s', response.content)
        raise Exception(403, 'Unable to do authentication')


    def get_headers(self, renew_auth=False):
        if renew_auth:
            self._refresh_token()

        headers = {'Authorization' : 'Bearer {0}'.format(self.access_token),
                   'User-Agent'    : self._user_agent,
                   'Accept'        : 'application/json',
                   }
        if self.client_ip:
            headers['X-Real-IP'] = self.client_ip

        return headers


if __init__ == "__main__":
    host_url = "https://www.dropbox.com/1/"
    app_key = '0f0ve5nvnlsx0f7'
    app_secret = 'tmv8XJFrio8AAAAAAAAoozW-i1K4nWzcHgdZZQJfODN4rWdRhpwBlbk2PUQghTxY'

    Authenticator(
    def __init__(self, access_token, client_id, client_secret, host_url, refresh_token, client_ip=None):
