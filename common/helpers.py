from colorama import Fore, Back, Style
from common.constants import (PRINT_DISCOUNT, PRINT_NORMAL, PRINT_HIDE,
                              PRINT_CHOICE, PRINT_INIT, PRINT_FINISHED,
                              PRINT_NEXT_ELEMENT)


def print_mesage(type, name=None, vendor=None, discount=None, price=None):
    """Print the message to the user."""
    message = "{} {}% discount in {}".format(
        name,
        discount,
        vendor
    )
    if type == PRINT_DISCOUNT:
        print(Fore.RED + message)
        # Reset the style back to normal
        print(Style.RESET_ALL)
    elif type == PRINT_NORMAL:
        print(message)
    elif type == PRINT_HIDE:
        pass
    elif type == PRINT_CHOICE:
        print(Back.CYAN + Fore.RED + message + Style.RESET_ALL)
    elif type == PRINT_INIT:
        message = " Welcome to the Book Tracker!! "
        print(Back.WHITE + Fore.BLACK + message + Style.RESET_ALL)
    elif type == PRINT_FINISHED:
        line = "That's all, cu soon, bye bye!"
        print(Back.WHITE + Fore.BLACK + line + Style.RESET_ALL)
    elif type == PRINT_NEXT_ELEMENT:
        line = "Searching for next book..."
        print(Back.WHITE + Fore.BLACK + line + Style.RESET_ALL)


def print_error_message(name, vendor, error):
    """Print an error message to the user."""
    message = "{} returns an error for \"{}\": {}".format(
        vendor,
        name,
        error
    )
    print(Back.RED + message + Style.RESET_ALL)
