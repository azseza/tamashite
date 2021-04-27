"""
@author: azseza
Python helper file that contains all the validator classes.
"""
import ipaddress
try:
    from PyInquirer import (Token, ValidationError, Validator,
                            print_json, prompt, style_from_dict)
except ImportError:
    try:
        from prompt_toolkit.token import Token
    except ImportError:
        from pygments.token import Token
try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

#Style of the form in the terminal
style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


class IntValidator(Validator):
    """
    Validator for int and non empty argument
    """

    def validate(self, value):
        try:
            if len(value) == 0:
                raise Exception
            assert type(value) is int
            return True
        except AssertionError:
            return False
        except Exception:
            return False


class PortValidator(Validator):
    """
    Validates wheather or not its a valid port number
    """
    def validate(self, value):
        if value == 80 or value == 443:
            return True
        else:
            return False


class TargetValidator(Validator):
    """
    Validator for host target adress
    same as Ip Validator
    """

    def validate(self, value):
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False


class IpValidator(Validator):
    """
    Validator for IP input
    """
    def validate(self, value):
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False


class PathValidator(Validator):
    def validate(self, value):
        a = str(value)
        if a[0] == '/':
            return True
        else:
            return False


class EmptyValidator(Validator):
    """
    Validator for empty input values
    """
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))
