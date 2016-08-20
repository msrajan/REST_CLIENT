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

    def __init__(self, access_token, client_id, client_secret, host_url, refresh_token=None):
        self.access_token   = access_token
        self.client_id      = client_id
        self.client_secret  = client_secret
        self.refresh_token  = refresh_token
        self.host_url       = host_url
        self._user_agent    = 'REST API python client'
        self.client_ip      = client_ip

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value

    def get_headers(self):

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
