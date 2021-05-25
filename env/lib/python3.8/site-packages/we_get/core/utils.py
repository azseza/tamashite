"""
Copyright (c) 2016-2017 Levi Sabah <x@levisabah.com> (https://github.com/levisabah/we-get/)
See the file 'LICENSE' for copying.
"""

import sys
from random import choice
import re
from os import sep
from we_get import __file__ as p
from glob import glob
from colorama import init as colorama_init
from colorama import Fore, Style
colorama_init(autoreset=True)

COLORS = {"red" : Fore.RED, 
  "green" : Fore.GREEN, 
  "blue" : Fore.BLUE, 
  "yellow" : Fore.YELLOW,
  "cyan" : Fore.CYAN,
  "white" : Fore.WHITE
}

def format_help(doc, errmsg):
    """ format_help: fix help message.
        @param doc: usage string.
        @param errmsg: error message to add.
    """
    for line in doc.split("\n"):
        if "options:" in line or "Options" in line:
            line = color("yellow", line)
        elif re.findall('<(\w+)>', line):
            value = re.findall('<(\w+)>', line)[0]
            line = line.replace('<%s>' %(value), "[%s]" %(color("cyan", value)))
            line = line.replace('=', ' ')
        print(line)
    if errmsg:
        msg_error("%s" %(errmsg), True)
    sys.stdout.write("Copyright (c) 2016-2017 Levi Sabah <x@levisabah.com>.\n")
    sys.stdout.write("Full documentation at: <http://github.com/levisabah/we-get>\n")

def printc(color, text):
    """printc: print colors
        @param color
        @param text
    """
    for x in COLORS:
        if x == color:
            sys.stdout.write("%s%s%s\n" % (COLORS[x], text, Style.RESET_ALL))

def printc_raw(color, text):
    """printc_raw: print colors without new line
        @param color
        @param text
    """
    for x in COLORS:
        if x == color:
            sys.stdout.write("%s%s%s" % (COLORS[x], text, Style.RESET_ALL))

def msg_err_trace(exit=False):
    """ msg_err_trace: print dump of error. 
        @param exit: exit on end.
    """
    msg_error("%s\n# %s\n# %s" % (sys.exc_info()[0], 
        sys.exc_info()[1], sys.exc_info()[2]), exit)
   
def msg_fetching(target):
    """ msg_fetching: Show message hen fetching data from @target."
      @param target: name
    """
    sys.stdout.write("%s#%s fetching data from %s\'%s'%s ...\r" % (Fore.YELLOW,
        Style.RESET_ALL,
        Fore.GREEN,
        target,
        Style.RESET_ALL))

def color(color, msg):
    """ color: return colored text using colorama.
        @param color: Fore.color
        @msg: string.
    """
    for x in COLORS:
        if x == color:
            return "%s%s%s" % (COLORS[x], msg, Style.RESET_ALL)

def msg_error(msg, exit):
    """ msg_error : error message.
        @param msg : string.
        @param exit  : exit?
    """
    sys.stdout.write("%s# error:%s %s\n" % (Fore.RED, Style.RESET_ALL, msg))
    if exit: sys.exit(1)

def msg_info(msg):
    """ msg_info: info message.
        @param msg: string.
    """
    sys.stdout.write("%s#%s %s\n" % (Fore.BLUE, Style.RESET_ALL, msg))

def msg_warning(msg):
    """ msg_warning: show warning msg
        @param msg: message string.
    """
    sys.stdout.write("%s# WARNING:%s %s\n" % (Fore.YELLOW, Style.RESET_ALL, msg))

def msg_item(item, items):
    """ msg_item: print item.
        @param item    : name.
        @param seeds   : number of seeds if any.
        @param leeches : number of leeches if any.
    """
    leeches = items['leeches']
    seeds = items['seeds']
    target = items['target']  

    sys.stdout.write("%s %s [%s/%s]\n" % (color("green", target), color("white", item),
        color("green", seeds), color("red", leeches)))

def mkpath(path):
    """ mkpath - create cross platfrom path.
        @path - path .
        
        by default we are using / for sep.
        mkpath() will replace the default sep with os.sep.
        this way we will create cross platfrom path.
    """
    return path.replace('/', sep)

def pkgpath():
    """ pkgpath: return the location of the installed packages.
    """
    x = p.split(sep)
    x.pop(-1) # Remove __init__.py
    return sep.join(x)

def random_user_agent():
    """ rand_user_agent - return random user agent from txt/useragents.txt
    """
    agents_path = mkpath("%s/extra/useragents.txt" % (pkgpath()))
    try: 
        data = open(agents_path, "r").readlines()
        return choice(data)[:-1]
    except IOError:
        msg_error("Cannot open: %s - to read user agents." % (agents_path), True)

def list_wg_modules():	
    """ list_wg_modules - list all modules from modules/.
    """
    modules = list()
    path = mkpath("%s/modules/*.py" % (pkgpath()))
    for module in glob("%s" %(path)):
        if not "__init__" in module:
            module = module.split("%s" %(sep))[-1].split(".")[0]
            modules.append(module)
    return modules
