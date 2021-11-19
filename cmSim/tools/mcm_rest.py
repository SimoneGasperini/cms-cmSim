import ssl
import json
import sys
import urllib.request as urllib
from urllib.error import HTTPError


class McM:

    def __init__(self):
        self.server = 'https://cms-pdmv.cern.ch/mcm/public/'
        ssl._create_default_https_context = ssl._create_unverified_context
        self.opener = urllib.build_opener()

    def __http_request(self, url, method='GET'):
        url = self.server + url
        request = urllib.Request(url=url, method=method)
        try:
            response = self.opener.open(request)
            response = response.read().decode('utf-8')
            return json.loads(response)
        except HTTPError:
            print(f'Error while making a "{method}" request to "{url}"')
            sys.exit()

    def get_by_prep_id(self, prep_id):
        url = f'restapi/requests/get/{prep_id}'
        response = self.__http_request(url=url)
        results = response.get('results')
        return results

    def get_by_dataset_name(self, dataset_name):
        url = f'restapi/requests/produces{dataset_name}'
        response = self.__http_request(url=url)
        results = response.get('results')
        return results
