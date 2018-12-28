from colorama import init as colorama_init
from config.configurator import Configurator
from vendors.bookshops import ProtoporiaBookshop, PoliteiaBookshop
from common.helpers import print_mesage, print_error_message
from common.options_handler import OptionsHandler
from common.constants import (PRINT_INIT, PRINT_FINISHED,
                              PRINT_NEXT_ELEMENT, MODE_LOCAL, MODE_AWS)

ERROR_NOT_FOUND = "Book wasn't found."
ERROR_USER_INPUT = "Invalid user input."


def init():
    """Initialize the colorama library and output some initial text."""
    # Initialise colorama for terminal text
    colorama_init()
    print_mesage(type=PRINT_INIT)


def perform_search(vendor, book, configuration):
    """Perform a search on a specific book on a specific vendor."""
    book_choices = vendor.search(book)
    options_handler = OptionsHandler(book_choices, vendor)
    # Show options to the user
    options_handler.display_choices()
    # Ask for user's input
    user_choice = options_handler.ask_input()
    if int(user_choice) > len(book_choices):
        print_error_message(
            name=book.name, vendor=vendor.name,
            error=ERROR_USER_INPUT
        )
        return False
    return book_choices[int(user_choice)]


def crawl(mode):
    """Iterate through a list of books, print the discount (if any) for both providers."""
    configuration = Configurator()
    vendors = (PoliteiaBookshop(), ProtoporiaBookshop())
    books = configuration.get_books()

    for book in books:
        for vendor in vendors:
            # If there is a link for that specific vendor, visit directly the page
            try:
                if getattr(book, vendor.name):
                    name, discount = vendor.get(book)
                    print_mesage(
                        name=name, type=book.discount_type(discount), discount=discount,
                        vendor=vendor.name
                    )
                    continue
            except AttributeError:
                # Vendor link not found
                pass

            # If direct link not found, perform a search
            try:
                book_found = perform_search(
                    vendor=vendor, book=book, configuration=configuration
                )
                if book_found:
                    # Update the configuration with user's choice
                    configuration.update_configuration(
                        book_to_update=book_found, vendor=vendor
                    )
            except IndexError:
                print_error_message(
                    name=book.name, vendor=vendor.name,
                    error=ERROR_NOT_FOUND
                )

        print_mesage(type=PRINT_FINISHED) if book == books[-1] else print_mesage(type=PRINT_NEXT_ELEMENT)


def lambda_handler(event, context):
    """Entrypoint for AWS Lambda events."""
    # Initiate and run the script in AWS mode
    init()
    crawl(mode=MODE_AWS)
    return True


# Initiate and run the script in local mode
init()
crawl(mode=MODE_LOCAL)
