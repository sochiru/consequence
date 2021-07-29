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
        self.token = token
        self.host_api = settings.INTEGRATIONS['TRUELAYER']['HOST_API']
        self.host_auth = settings.INTEGRATIONS['TRUELAYER']['HOST_AUTH']
        self.secret = settings.INTEGRATIONS['TRUELAYER']['SECRET']

        self.verify_https = True

        # request configuration
        self.request_headers = {'Content-Type': 'application/json'}
        if self.token:
            self.request_headers["Authorization"] = "Bearer %s" % (self.token)

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

        print(data)

        # submit request
        response = requests.request(method.lower(), full_url, params=query_params, data=data, headers=merge_headers,
                                    verify=self.verify_https)
        return response
