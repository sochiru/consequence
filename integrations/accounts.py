from .path import ACCOUNTS
from .connect import TrueLayerConnect


class AccountsConnect(TrueLayerConnect):
    """ Manage accounts related API """

    def __init__(self, token):
        """
        Initialize class
        Parameters:
            token: access token
        """
        super().__init__(token)

    def get(self, account_id=None, query_params=None):
        """
        Fetch accounts
        Parameters:
            account_id (str): account id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        if account_id is not None:
            # url here
            return self.fetch('get',
                              '%s/%s' % (ACCOUNTS, account_id),
                              query_params=query_params)

        return self.fetch('get',
                          ACCOUNTS,
                          query_params=query_params)

    def get_account_balance(self, account_id=None, query_params=None):
        """
        Fetch account balance
        Parameters:
            account_id (str): account id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        return self.fetch('get',
                          '%s/%s/balance' % (ACCOUNTS, account_id),
                          query_params=query_params)

    def get_account_transactions(self, account_id=None, query_params=None):
        """
        Fetch account transactions
        Parameters:
            account_id (str): account id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        return self.fetch('get',
                          '%s/%s/transactions' % (ACCOUNTS, account_id),
                          query_params=query_params)

    def get_account_transactions_pending(self, account_id=None, query_params=None):
        """
        Fetch account transactions pending
        Parameters:
            account_id (str): account id
            query_params (dict): Dict of query parameters
        Returns:
            requests.Response: A request response
        """

        return self.fetch('get',
                          '%s/%s/transactions/pending' % (ACCOUNTS, account_id),
                          query_params=query_params)
