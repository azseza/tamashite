from urllib.parse import quote

from .common import create_authorization
from .principal import Principal
from urllib.parse import quote

from Token.generated.bank import ApiClient
from Token.generated.bank.apis import ClientsApi
from Token.generated.bank.apis import AccessesApi


class BankService(object):
    """
    Provides Token Bank service API.
    """

    def __init__(self, bank_code, sk, url):
        """
        :param bank_code: identifies the bank
        :type bank_code: str
        :param sk: bank's private key
        :type sk: str
        :param url: bank' service URL
        :type url: str
        """
        self._bank_code = bank_code
        self._sk = sk
        self._base_url = url
        self._clients = ClientsApi(ApiClient(self._base_url))
        self._accesses = AccessesApi(ApiClient(self._base_url))

    def bank_code(self):
        """
        :return: bank code
        """
        return self._bank_code

    def create_access(self, client_id, account_id, public_key, session_id='test'):
        """
        Creates a request to link a bank account for a Token member. The result
        is then used to make a call to USP to link the account.

        :param client_id: bank's client id, used by the bank to identify a customer
        :param account_id: bank's client account id
        :param public_key: customer's public key
        :param session_id: session id
        :return: access object that is used to call USP to link the account
        """
        request = {
            'sessionId': session_id,
            'verificationPublicKey': public_key,
        }
        auth = create_authorization(
            self._security_context(),
            'POST',
            self._base_url + '/clients/' + client_id + '/accounts/' + quote(account_id) + '/accesses',
            request)
        return self._clients.create_access_route(client_id, account_id, request, authorization=auth)

    def verify_access(self, access_id, payload, signature):
        """
        Verifies that the supplied access id is valid and active.

        :param access_id: access id
        :param payload:
        :param signature:
        :return:
        """
        request = {
            "verificationPayload": payload,
            "verificationSignature": signature
        }
        auth = create_authorization(
            self._security_context(),
            'PUT',
            self._base_url + '/accesses/' + quote(access_id) + '/verify',
            request)
        return self._accesses.verify_access_route(access_id, request, authorization=auth)

    def _security_context(self):
        """
        Security principal to be used to make server requests. Used to
        authenticate the server requests.

        :return: security principal
        :rtype Principal
        """
        return Principal('bank-' + self._bank_code, self._sk)
