class Account:
    """
    Represents Token member funding account. A member can have multiple
    accounts linked.
    """

    def __init__(self, provider, member, account_id, name):
        """
        :param provider: User Service Provider service client
        :type provider: ProviderService
        :param member: Token member object that owns the account
        :type member: Member
        :param account_id: member account id
        :type account_id: str
        :param name: account name
        :type name: str
        """
        self._provider = provider
        self._member = member
        self._account_id = account_id
        self._name = name

    def id(self):
        """
        :return: account id
        :rtype str
        """
        return self._account_id

    def transactions(self, page_offset, page_limit):
        """
        Returns the list of transactions for this account.

        :param page_offset: page offset to fetch the tokens at
        :type page_offset: int
        :param page_limit: max number of results to return
        :type page_limit: int
        :return:
        """
        return self._provider.get_transactions(
            self._member.principal(),
            self._account_id,
            page_offset,
            page_limit)

    def charge_token(self, token, amount, currency, description=''):
        """
        Charges a token endorsed by a payer.

        :param token: token to endorse
        :param amount: amount to charge
        :param currency: currency, such as "EUR" or "USD"
        :type currency: str
        :param description: payment description
        :type description: str
        :return:
        """
        return self._provider.create_payment(
            self._member.principal(),
            token.id,
            self._account_id,
            amount,
            currency,
            description)

    def transfer_money(self, payee_alias, amount, currency, description=''):
        """
        Transfers money to the specified payee.

        :param payee_alias: payee Token alias
        :type payee_alias: str
        :param amount: amount to charge
        :param currency: currency, such as "EUR" or "USD"
        :type currency: str
        :param description: payment description
        :type description: str
        :return:
        """
        token = self._provider.create_payee_token(
            self._member.principal(),
            payee_alias,
            {
                'currency': currency,
                'singlePayment': {
                    'amount': amount
                }
            },
            description)
        self._member.endorse_token(token, self)
        return token

    def info(self):
        """
        Looks up principal account by account id.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param account_id: account id
        :type account_id: str
        :return: server response
        """
        return self._provider.get_account(
            self._member.principal(),
            self._account_id)
