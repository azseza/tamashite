import binascii
from hashlib import sha256

from .common import create_authorization

from Token.generated.alias import ApiClient
from Token.generated.alias.apis import AliasesApi


class AliasService(object):
    """
    Provides Token Alias service API.
    """

    def __init__(self, url):
        """
        :param url: bank' service URL
        :type url: str
        :param url:
        """
        self._base_url = url
        self._aliases = AliasesApi(ApiClient(self._base_url))

    def get_alias(self, principal, alias):
        """
        Looks up customer information for a given alias.

        :param principal: used to authenticate and identify user making the request
        :type principal: Principal
        :param alias: member alias
        :type alias: str
        :return:
        """
        m = sha256()
        m.update(alias.encode())
        base = binascii.b2a_base64(m.digest())
        no_padding = (base.decode('utf-8')).split('=')[0]
        replace1 = no_padding.replace('+', '-')
        replace2 = replace1.replace('/', '_')
        auth = create_authorization(principal, 'GET', self._base_url + '/aliases/' + replace2)
        return self._aliases.get_alias_route(replace2, authorization=auth)
