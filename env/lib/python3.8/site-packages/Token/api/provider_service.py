import codecs
import ed25519
from urllib.parse import quote
from urllib.parse import urlencode

from .common import create_key_pair
from .common import create_authorization
from .member import Member
from .principal import Principal

from Token.generated.provider import ApiClient
from Token.generated.provider.apis import AccountsApi
from Token.generated.provider.apis import AliasesApi
from Token.generated.provider.apis import DevicesApi
from Token.generated.provider.apis import MembersApi
from Token.generated.provider.apis import TokensApi


class ProviderService(object):
    """
    Provides User Service Provider (USP) API.
    """

    def __init__(self, provider_code, sk, url):
        """
        :param provider_code: USP code, used to identify the USP to connect to
        :type provider_code: str
        :param url: USP URL to connect to
        :type url: str
        """
        self._provider_code = provider_code
        self._sk = sk
        self._base_url = url
        self._accounts = AccountsApi(ApiClient(self._base_url))
        self._aliases = AliasesApi(ApiClient(self._base_url))
        self._devices = DevicesApi(ApiClient(self._base_url))
        self._members = MembersApi(ApiClient(self._base_url))
        self._tokens = TokensApi(ApiClient(self._base_url))

    def code(self):
        """
        :return: USP code
        :rtype str
        """
        return self._provider_code

    def principal(self):
        """
        Security principal to be used to make server requests. Used to
        authenticate the server requests.

        :return: security principal
        :rtype Principal
        """
        return Principal('provider-' + self.code(), self._sk)

    def create_member(self, device_name, push_id):
        """
        Creates a new USP member account. Member account must be created before
        executing any other operations on USP.

        :param device_name: name of the device used to hold the member private
            information (e.g. private key)
        :type device_name: str
        :param push_id: used to deliver member push notifications, when account
            activity is detected
        :type push_id: str
        :return: private/public keys of the newly created member along with the
            response that provides member information
        """
        sk, pk = create_key_pair()
        request = {
            'device':
                {
                    'name': device_name,
                    'pushNotificationId': push_id,
                    'publicKeys': [pk]
                }
        }
        return [sk, pk, self._members.create_member_route(request)]

    def create_device(self, alias, device_name, push_id, pk):
        """
        TODO(alexey): How is this used, still needed?

        :param alias:
        :param device_name:
        :param push_id:
        :param pk:
        :return:
        """
        request = {'name': device_name, 'pushNotificationId': push_id, 'publicKeys': [pk]}
        return self._aliases.create_alias_device_route(alias, request)

    def create_alias(self, principal, alias, description=''):
        """
        Creates an alias for a given user.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param alias: alias that can be used to identify the acount
        :type alias: str
        :param description: alias description
        :type description: str
        :return: server response
        """
        request = {'description': description}
        auth = create_authorization(principal, 'POST', self._base_url + '/aliases/' + alias, request)
        return self._aliases.create_alias_route(alias, request, authorization=auth)

    def get_accounts(self, principal):
        """
        Looks up all the accounts linked to the given principal.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param principal:
        :return: server response
        """
        auth = create_authorization(principal, 'GET', self._base_url + '/accounts')
        return self._accounts.get_accounts_route(authorization=auth)

    def get_account(self, principal, account_id):
        """
        Looks up principal account by account id.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param account_id: account id
        :type account_id: str
        :return: server response
        """
        auth = create_authorization(principal, 'GET', self._base_url + '/accounts/' + quote(account_id))
        return self._accounts.get_account_route(account_id, authorization=auth)

    def create_account(self, member, bank_code, access_id, name):
        """
        Creates a new account for a given member. Before calling this method
        caller needs to obtain authorization to link the account using bank
        API.

        :param member: used to authenticate and identify user making the request
        :type member: Member
        :param bank_code: code that identifies that bank that issued account
            linking authorization
        :type bank_code: str
        :param access_id: bank issued account access id. The id will be used to
            identify the account when making bank calls.
        :type access_id: str
        :param name: name to associate with the account
        :return: server response
        """
        key = ed25519.SigningKey(ed25519.keys.from_ascii(member.secret_key(), encoding="hex"))
        signature = str(codecs.encode(key.sign(str.encode(member.device_id())), 'hex'), encoding="UTF-8")
        request = {
            "bankCode": bank_code,
            "accessId": access_id,
            "verificationSignature": signature,
            "name": name
        }
        auth = create_authorization(member.principal(), 'POST', self._base_url + '/accounts', request)
        return self._accounts.create_account_route(request, authorization=auth)

    def get_tokens(self, principal, page_offset, page_limit):
        """
        Returns all the tokens associated with the principal making the request.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param page_offset: page offset to fetch the tokens at
        :type page_offset: int
        :param page_limit: max number of results to return
        :type page_limit: int
        :return: list of tokens
        """
        page_query = self._page_query(page_offset, page_limit)
        auth = create_authorization(
            principal,
            'GET',
            self._base_url + '/tokens?%s' % page_query)
        return self._tokens.get_tokens_route(page_offset, page_limit, authorization=auth)

    def get_token(self, principal, token_id):
        """
        Returns the token specified by the provided token id.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param token_id: page offset to fetch the tokens at
        :type token_id: str
        :return: server response
        """
        auth = create_authorization(principal, 'GET', self._base_url + '/tokens/' + quote(token_id))
        return self._tokens.get_token_route(token_id, authorization=auth)

    def create_payee_token(self, principal, payee_alias, terms, description=''):
        """
        Creates a payee token. The token needs to be endorsed by the payer
        before it can be charged.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param payee_alias: payee alias
        :type payee_alias: str
        :param terms: terms associated with the token, such as max amount, single or
            multi use, etc
        :type terms: object
        :param description: token description
        :type description: str
        :return: server response
        """
        request = {
            "payee": {"aliasCode": payee_alias},
            "description": description,
            "terms": terms
        }
        auth = create_authorization(principal, 'POST', self._base_url + '/tokens', request)
        return self._tokens.create_token_route(request, authorization=auth)

    def create_payer_token(self, principal, payer_alias, terms, description=''):
        """
        Creates a payer token. The token is endorsed and ready to be charged.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param payer_alias: payer alias
        :type payer_alias: str
        :param terms: terms associated with the token, such as max amount, single or
            multi use, etc
        :type terms: object
        :param description: token description
        :type description: str
        :return: server response
        """
        request = {
            "payer": {"aliasCode": payer_alias},
            "description": description,
            "terms": terms
        }
        auth = create_authorization(principal, 'POST', self._base_url + '/tokens', request)
        return self._tokens.create_token_route(request, authorization=auth)

    def create_token(self, principal, payer_alias, payee_alias, terms, description=''):
        """
        Creates a token that defines a money transfer between payer and payee.
        The token is endorsed and ready to be charged.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param payer_alias: payer alias
        :type payer_alias: str
        :param payee_alias: payee alias
        :type payee_alias: str
        :param terms: terms associated with the token, such as max amount, single or
            multi use, etc
        :type terms: object
        :param description: token description
        :type description: str
        :return: server response
        """
        request = {
            "payer": {"aliasCode": payer_alias},
            "payee": {"aliasCode": payee_alias},
            "description": description,
            "terms": terms
        }
        auth = create_authorization(principal, 'POST', self._base_url + '/tokens', request)
        return self._tokens.create_token_route(request, authorization=auth)

    def endorse_token(self, principal, token_id, account_id):
        """
        Used by payer to endorse a token that was generated by payee. After the
        token is endorsed it is ready to be charged.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param token_id: token id
        :type token_id: str
        :param account_id: payer account id to be used as the source of funds
        :type account_id: str
        :return: server response
        """
        request = {'accountId': account_id}
        auth = create_authorization(
            principal,
            'PUT',
            self._base_url + '/tokens/' + quote(token_id) + '/endorse',
            request)
        return self._tokens.endorse_token_route(token_id, request, authorization=auth)

    def decline_token(self, principal, token_id):
        """
        Used by payer to decline a token payment request. After the token is
        declined it can no longer be used.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param token_id: token id
        :type token_id: str
        :return: server response
        """
        auth = create_authorization(
            principal,
            'PUT',
            self._base_url + '/tokens/' + quote(token_id) + '/decline')
        return self._tokens.decline_token_route(token_id, authorization=auth)

    def create_payment(self, principal, token_id, account_id, amount, unit, description=''):
        """
        Creates a new payment by charging a supplied token.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param token_id: token id
        :type token_id: str
        :param account_id: account id
        :type account_id: str
        :param amount: amount
        :type amount: int
        :param unit: currency, such as "USD" or "EUR"
        :type unit: str
        :param description: payment description
        :type description: str
        :return: server response
        """
        request = {
            "accountId": account_id,
            "description": description,
            "amount": {
                "value": str(amount),
                "unit": unit
            }
        }
        auth = create_authorization(
            principal,
            'POST',
            self._base_url + '/tokens/' + quote(token_id) + '/payments',
            request)
        return self._tokens.create_payment_route(token_id, request, authorization=auth)

    def get_transactions(self, principal, account_id, page_offset=0, page_limit=100):
        """
        Returns list of transactions for a user identified as the principal.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param account_id: account id to retrieve the transactions for
        :type account_id: str
        :param page_offset: page offset to fetch the transactions at
        :type page_offset: int
        :param page_limit: max number of results to return
        :type page_limit: int
        :return:
        """
        page_query = self._page_query(page_offset, page_limit)
        auth = create_authorization(
            principal,
            'GET',
            self._base_url + '/accounts/' + quote(account_id) + '/transactions?%s' % page_query)
        return self._accounts.get_transactions_route(account_id, page_offset, page_limit, authorization=auth)

    @staticmethod
    def _page_query(offset, limit):
        return urlencode({'pageOffset': offset, 'pageLimit': limit})
