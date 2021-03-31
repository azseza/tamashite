from __future__ import absolute_import

import json
import os
import random
import string

# import .api
from .api.bank_service import BankService
from Token.api.member import Member
from Token.api.principal import Principal
from Token.api.provider_service import ProviderService
from Token.api.alias_service import AliasService


def welcome_message():
    print("Welcome to the Token console. Type Token.help() for help.")


def help():
    print("+-------------------------------------------------------------+")
    print("| Welcome to the  console. Here we can issue commands to      |")
    print("| interact with the Token system. Please know that the system |")
    print("| is still in development and therefore there will be bugs/   |")
    print("| missing pieces                                              |")
    print("+-------------------------------------------------------------+")
    print("| KEYS                                                        |")
    print("| In order to execute some of these commands, you will need   |")
    print("| configuration parameters. Please ask a Token employee to    |")
    print("| obtain these.                                               |")
    print("+-------------------------------------------------------------+")
    print("| COMMANDS - Token                                            |")
    print("| Token.gateway(path_to_config_file)                          |")
    print("| Token.bank(path_to_config_file)                             |")
    print("| Token.create_member(provider, ...)                          |")
    print("+-------------------------------------------------------------+")
    print("| You can use dir(object) to see what methods its has.        |")
    print("| Token.demo(1) to view demo. (You can copy paste this)       |")
    print("+-------------------------------------------------------------+")


def demo(demo_num):
    script_path = os.path.dirname(os.path.abspath(__file__))
    try:
        f = open(os.path.join(script_path, 'demos/demo' + str(demo_num) + '.py'))
        print(f.read())
    except IOError:
        print("Demo does not exist.")


def gateway(config_file_path):
    config = _read_json(config_file_path)
    return ProviderService(config['code'], config['key'], config['url'])


def bank(config_file_path):
    config = _read_json(config_file_path)
    return BankService(config['code'], config['key'], config['url'])


def create_member(prov, member_alias, device_name, push_id):
    [sk, pk, response] = prov.create_member(device_name, push_id)
    security_ctx = Principal('provider-' + prov.code() + '-device-' + response.device.id, sk)
    prov.create_alias(security_ctx, member_alias)

    return Member(
        prov,
        member_alias,
        response.device.id,
        device_name,
        sk,
        pk)


def generate_id(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def _read_json(file_path):
    try:
        with open(file_path) as config_data:
            return json.load(config_data)
    except OSError:
        raise Exception("Could not read config file: " + file_path)


welcome_message()
