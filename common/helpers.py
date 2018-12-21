from colorama import Fore, Back, Style
from common.constants import PRINT_DISCOUNT, PRINT_NORMAL, PRINT_HIDE, PRINT_CHOICE


def print_mesage(name, vendor, type, discount=None, price=None):
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


def print_error_message(name, vendor, error):
    """Print an error message to the user."""
    message = "{} returns an error for \"{}\": {}".format(
        vendor,
        name,
        error
    )
    print(Back.RED + message + Style.RESET_ALL)


def print_end_of_element():
    """Print a straight line after each book."""
    print("<---------------------------------------------------->")
