import codecs
import datetime
import json
import ed25519
from urllib.parse import quote

from .principal import Principal


def create_key_pair():
    """
    Creates a new secret/private and public key pair.

    :return: tuple of secret/private and public keys
    """
    sk, vk = ed25519.create_keypair()
    return str(sk.to_ascii(encoding="hex"), encoding='UTF-8'), str(vk.to_ascii(encoding="hex"), encoding='UTF-8')


def create_authorization(principal, method='GET', url='/', body=None, iso_date=None, nonce=None):
    """
    Creates authorization object to be used when performing all the server calls.

    :param principal: security principal who is making the request
    :type principal: Principal
    :param method: HTTP method
    :type method: str
    :param url: HTTP request URL
    :type url: str
    :param body: HTTP request body
    :type body: dict
    :param iso_date:
    :param nonce:
    :return:
    """
    if not iso_date:
        iso_date = datetime.datetime.utcnow().isoformat()[:23] + 'Z'
    if not nonce:
        while nonce is None or nonce[0] == '0':
            nonce = str(ed25519.create_keypair()[0].to_ascii(encoding='hex'), encoding='UTF-8')

    index0 = url.index('/')
    index1 = url.index('/', index0 + 1)
    index2 = url.index('/', index1 + 1)
    path_and_query = url[index2:]
    path = path_and_query
    and_query = ""

    if '?' in path_and_query:
        index3 = path_and_query.index('?')
        path = path_and_query[0:index3]
        sorted_query = path_and_query[index3 + 1:]
        sorted_query = "&".join(sorted(sorted_query.split('&')))
        and_query = "?" + sorted_query

    andd = " "
    anddBody = ""

    if body is not None and body != '':
        anddBody = andd + json.dumps(body, sort_keys=True, separators=(',',':'))

    payload = principal.subject() + andd + iso_date + andd + nonce + andd + method + andd \
              + path + and_query + anddBody

    key = ed25519.SigningKey(ed25519.keys.from_ascii(principal.secret_key(), encoding="hex"))
    signature = str(codecs.encode(key.sign(str.encode(payload)), 'hex'), encoding="UTF-8")

    comma = ','

    credentials = "subject-id=" + quote(principal.subject()) + comma + \
                  "request-timestamp=" + quote(iso_date) + comma + \
                  "request-nonce=" + nonce + comma + \
                  "request-signature=" + signature

    scheme = "Token-Ed25519-SHA512"
    return scheme + andd + credentials
