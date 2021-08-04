from .path import CARDS
from .connect import TrueLayerConnect


class AuthConnect(TrueLayerConnect):
    """ Manage cards related API """

    def __init__(self, token):
        """
        Initialize class
        Parameters:
            token: access token
        """
        super().__init__(token)

    def exchange_token(self, data=None, is_api=False):
        """
        Fetch cards
        Parameters:
            card_id (str): Card id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        return self.fetch('post',
                          '/connect/token',
                          data=data,
                          headers=headers,
                          is_api=is_api)
