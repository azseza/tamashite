from .account import Account
from .principal import Principal


class Member:
    """
    Represents a Token member. The member account must be created before
    any other operations can be performed. The member account is then linked
    with potentially multiple bank accounts that act as source of funds.
    """

    def __init__(self, provider, alias, device_id, device_name, sk, pk):
        """
        :param provider: User Service Provider (USP) that the member belongs to
        :param alias: member Token alias
        :type alias: str
        :param device_id: device id
        :type device_id: str
        :param device_name: device name
        :type device_name: str
        :param sk: member secret/private key
        :type sk: str
        :param pk: member public key
        :type pk: str
        """
        self._provider = provider
        self._alias = alias
        self._sk = sk
        self._pk = pk
        self._device_id = device_id
        self._device_name = device_name

    def public_key(self):
        """
        :return: member public key
        :rtype str
        """
        return self._pk

    def secret_key(self):
        """
        :return: member secret/private key
        :rtype str
        """
        return self._sk

    def principal(self):
        """
        Security principal to be used to make server requests. Used to
        authenticate the server requests.

        :return: security principal
        :rtype Principal
        """
        return Principal(
            'provider-' + self._provider.code() + '-device-' + self._device_id,
            self._sk)

    def device_id(self):
        """
        :return: member device id
        :rtype str
        """
        return self._device_id

    def alias(self):
        """
        :return: member Token alias
        :rtype str
        """
        return self._alias

    def add_alias(self, alias):
        """
        Adds new alias for this member account.

        :param alias: new Token member alias to add
        :type alias: str
        """
        self._provider.create_alias(self.principal(), alias)
        self._alias = alias

    def get_accounts(self):
        """
        Returns list of the available member accounts.

        :return: list of the available member accounts.
        :rtype List(Account)
        """
        response = self._provider.get_accounts(self.principal())
        return [Account(self._provider, self, a.id, a.name) for a in response.accounts]

    def get_tokens(self, page_offset=0, page_limit=1000):
        """
        Returns list of the tokens created by this member.

        :param page_offset: page offset to fetch the transactions at
        :type page_offset: int
        :param page_limit: max number of results to return
        :type page_limit: int
        :return: list of the tokens
        :rtype List
        """
        return self._provider.get_tokens(self.principal(), page_offset, page_limit).tokens

    def get_token(self, token):
        """
        Returns list of the tokens created by this member.

        :param page_offset: page offset to fetch the transactions at
        :type page_offset: int
        :param page_limit: max number of results to return
        :type page_limit: int
        :return: list of the tokens
        :rtype List
        """
        return self._provider.get_token(self.principal(), token.id)


    def link_account(self, bank_code, access, name):
        """
        Links a bank account to be associated with this member account.

        :param bank_code: identifies the bank that the account is at
        :type bank_code: str
        :param access: returned by the bank's create_access call
        :type access: str
        :param name: account name to use
        :type name: str
        :return: account object for the newly created account
        :rtype Account
        """
        account = self._provider.create_account(self, bank_code, access.id, name)
        return Account(self._provider, self, account.id, name)

    def create_payee_token(self, payer_alias, terms):
        """
        Creates new token. The token needs to be endorsed by the payer before
        it can be charted.

        :param payer_alias: identifies the payer
        :param terms: payment terms
        :return: token that can be used to create a payment after the payer
            endorses it
        """
        return self._provider.create_payee_token(self.principal(), payer_alias, terms)

    def create_payer_token(self, payee_alias, terms):
        """
        Creates new token. The token is endorsed and ready to be charged.

        :param payee_alias: identifies the payee
        :param terms: payment terms
        :return: token that can be used to create a payment
        """
        return self._provider.create_payer_token(self.principal(), payee_alias, terms)

    def endorse_token(self, token, account):
        """
        Endorses a token created by payee who requested a payment.

        :param token: token to endorse
        :type token: str
        :param account: account to take the money from
        :type account: Account
        :return: server response
        """
        return self._provider.endorse_token(self.principal(), token.id, account.id())

    def decline_token(self, token):
        """
        Declines a token created by payee who requested a payment.

        :param token: token to endorse
        :type token: str
        :return: server response
        """
        return self._provider.decline_token(self.principal(), token.id)
