"""
Copyright (c) 2016-2017 Levi Sabah <x@levisabah.com> (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying permission
"""

import sys
from we_get.core.we_get import WG
from we_get.core.utils import msg_error
from we_get.core.utils import msg_err_trace
from we_get.core.tests import Tests

def main():
    test = Tests()
    test.init()
    we_get = WG()
    we_get.parse_arguments()
    try:
        we_get.start() 
    except (EOFError, KeyboardInterrupt):
        msg_error("[KeyboardInterrupt]", True)
