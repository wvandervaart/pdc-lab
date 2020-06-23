import requests
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NBRestConnection:

    def __init__(self,host, token):
        self._base_url = 'https://' + host + '/api/'
        self._host = host
        self._token = token

    def api_post(self, command, payload={}):
        headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'Authorization': "Token "+self._token
        }
        url = "{b}{c}".format(b=self._base_url, c=command)
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        payload = payload.encode(encoding='utf-8')
        req = requests.request("POST", url, data=payload, headers=headers, verify=False)
        success, resp = self.parse_resp(req)
        if not success:
            print("FAIL")
        return (resp)

    def api_call(self, command, payload={}):
        headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'Authorization': "Token "+self._token
        }
        url = "{b}{c}".format(b=self._base_url, c=command)
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        req = requests.request("GET", url, data=payload, headers=headers, verify=False)
        success, resp = self.parse_resp(req)
        if not success:
            print("FAIL")
        return (resp)

    def api_get(self, command, payload={}):
        headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'Authorization': "Token "+self._token
        }
        url = "{b}{c}".format(b=self._base_url, c=command)
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        req = requests.request("GET", url, data=payload, headers=headers, verify=False)
        resp = json.loads(req.text)
        return resp

    def parse_resp(self, req):
        resp = json.loads(req.text)
        out = resp
        if 'code' in resp.keys():
            success = False
        else:
            success = True
        return (success, out)

   # get prefix id
    def api_get_prefixid(self, prefix):
        command = "ipam/prefixes/?prefix=" + prefix
        payload = {}
        response = self.api_call(command, payload)
        return response["results"][0]["id"]

