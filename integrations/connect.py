import json
import requests
from django.conf import settings


class TrueLayerConnect:
    """True Layer API Connector"""

    def __init__(self, token):
        """
        Initialize class
        Parameters:
            basic_auth (tuple): A tuple value of username and password
        """
        self.token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjE0NTk4OUIwNTdDOUMzMzg0MDc4MDBBOEJBNkNCOUZFQjMzRTk1MTBSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IkZGbUpzRmZKd3poQWVBQ291bXk1X3JNLWxSQSJ9.eyJuYmYiOjE2Mjc0OTUwMTIsImV4cCI6MTYyNzQ5ODYxMiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnRydWVsYXllci1zYW5kYm94LmNvbSIsImF1ZCI6ImRhdGFfYXBpIiwiY2xpZW50X2lkIjoic2FuZGJveC1qYW5kLTUzYjI2MCIsInN1YiI6InIwYzAvN21PanU2a3JmMnY1L0lQeHl3R3RLc2E5SjA0aHpuOHBWajRDOUk9IiwiYXV0aF90aW1lIjoxNjI3NDk0MTg3LCJpZHAiOiJsb2NhbCIsImp0aSI6IjJBOTM4RDI5QjlERURGMkNGMDEyMjExOTUxRkIxMjREIiwic2lkIjoiYXV0aC1URFhqa2c5RmFLQ2Q3eDdid0RfSFk3MmlMd05STzFmX2syTkFkOXM2NzZjIiwiaWF0IjoxNjI3NDk0MjE3LCJjb25uZWN0b3JfaWQiOiJtb2NrIiwiY3JlZGVudGlhbHNfa2V5IjoiODA3NGNlMDljM2ExMjQyN2MyM2MyNTY0MzJlYTU4YmUyZGFjNmRlZGMzNWM2OWU2MGUyODY1OGQ5Mjc4NzE1NyIsInByaXZhY3lfcG9saWN5IjoiRmViMjAxOSIsImNvbnNlbnRfaWQiOiJiMmE2YTRkMS1lNGIwLTRiN2QtOGRlNS1kOGZkYTg3ZTViYWUiLCJzY29wZSI6WyJpbmZvIiwiYWNjb3VudHMiLCJiYWxhbmNlIiwiY2FyZHMiLCJ0cmFuc2FjdGlvbnMiLCJkaXJlY3RfZGViaXRzIiwic3RhbmRpbmdfb3JkZXJzIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbInB3ZCJdfQ.YuMKONRLUV4n1gKHneG2rOjeBmxxuK5fCruwsNcasDr-u-sHP4GLr9vlc_RI8h9xv19QJz9BqjJF9z56NkV2H-DszzCv6KkcfwdxCzVtn8wORag-SVk8VK5Pl_IWlJc7dM68LcxNhx4awv1F8ue15tZ6LubH2llyCe19RQMSMOTCtBjE6LrWfqSZ003kpV8ElfXBstgWgVm4QwsZfVRwS3qVRjF29QPTKmq7Spz5hdF3WAqh_extSvNqt68kqNekMA2p7OiZU7388x_ZB7A1pZoKNSmthJYgcVUI4BgRTRHUuMFR7oDomCz2q2HmeUOPoG_lL7XizF28kKG7VSDdeg'
        self.host_api = settings.INTEGRATIONS['TRUELAYER']['HOST_API']
        self.host_auth = settings.INTEGRATIONS['TRUELAYER']['HOST_AUTH']
        self.verify_https = True

        print(self.host_api)

        # request configuration
        self.request_headers = {'Content-Type': 'application/json',
                                "Authorization": "Bearer %s" % (self.token)}

    def fetch(self, method, url, query_params=None, data=None, headers=None, is_api=True):
        """
        Send request to odoo API
        Parameters:
            method (string): Request method
            url (string): Url path of API. Exclude Odoo host in string value
            query_params (dict): Dict of query parameters
            data (dict): Dict of payload
            headers (dict): Additional headers
            use_admin_auth (bool): Force use admin credentials
            add_pagination_params (bool): Force add pagination parameters if not found
            domain_filter_name (string):
                Domain filter set to be used
                Domain filter configuration is in connectors.odoo.configs.domain.DOMAIN_FILTER_MAP
        Returns:
            requests.Response: A request response
        """
        # pylint: disable=too-many-arguments
        if headers:
            merge_headers = {**self.request_headers.copy(), **headers}
        else:
            merge_headers = {**self.request_headers.copy()}
        if query_params is None:
            query_params = {}

        if is_api:
            full_url = self.host_api + url
        else:
            full_url = self.host_auth + url
        merge_query_params = query_params.copy()

        # if no data is set use query params as body
        if data:
            data = json.dumps({'params': data})
        else:
            data = json.dumps({'params': merge_query_params.copy()})
            merge_query_params = {}

        # submit request
        response = requests.request(method.lower(), full_url, params=query_params, data=data, headers=merge_headers,
                                    verify=self.verify_https)
        return response
