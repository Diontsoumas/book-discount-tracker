from colorama import Fore, Back, Style
from common.constants import MINIMUM_THRESHOLD


def print_mesage(name, vendor, discount=None):
    """Print the message to the user."""
    message = "{} {}% discount in {}".format(
        name,
        discount,
        vendor
    )
    if int(discount) >= MINIMUM_THRESHOLD:
        print(Fore.RED + message)
        # Reset the style back to normal
        print(Style.RESET_ALL)
    else:
        print(message)


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
