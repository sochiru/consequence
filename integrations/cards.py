from .path import CARDS
from .connect import TrueLayerConnect


class CardsConnect(TrueLayerConnect):
    """ Manage cards related API """

    def __init__(self, token):
        """
        Initialize class
        Parameters:
            token: access token
        """
        super().__init__(token)

    def get(self, card_id=None, query_params=None):
        """
        Fetch cards
        Parameters:
            card_id (str): Card id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        if card_id is not None:
            # url here
            return self.fetch('get',
                              '%s/%s' % (CARDS, card_id),
                              query_params=query_params)

        return self.fetch('get',
                          CARDS,
                          query_params=query_params)

    def get_card_balance(self, card_id=None, query_params=None):
        """
        Fetch card balance
        Parameters:
            card_id (str): Card id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        return self.fetch('get',
                          '%s/%s/balance' % (CARDS, card_id),
                          query_params=query_params)

    def get_card_transactions(self, card_id=None, query_params=None):
        """
        Fetch card transactions
        Parameters:
            card_id (str): Card id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        return self.fetch('get',
                          '%s/%s/transactions' % (CARDS, card_id),
                          query_params=query_params)

    def get_card_transactions_pending(self, card_id=None, query_params=None):
        """
        Fetch card transactions pending
        Parameters:
            card_id (str): Card id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        return self.fetch('get',
                          '%s/%s/transactions/pending' % (CARDS, card_id),
                          query_params=query_params)
