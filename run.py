from colorama import init as colorama_init
from config.configurator import Configurator
from vendors.bookshops import ProtoporiaBookshop, PoliteiaBookshop
from common.helpers import print_mesage, print_error_message, PrinterQueue
from common.options_handler import OptionsHandler
from common.constants import MODE_LOCAL, MODE_AWS, PRINT_INIT

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
    printer = PrinterQueue()
    vendors = (PoliteiaBookshop(), ProtoporiaBookshop())
    books = configuration.get_books()

    for book in books:
        for vendor in vendors:
            # If there is a link for that specific vendor, visit directly the page
            try:
                if getattr(book, vendor.name):
                    #Update book instance
                    book.update_values(**vendor.get(book))
                    printer.add_to_print_queue(book, vendor)
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
                printer.add_to_error_queue(book, vendor)

    printer.show(mode=mode, email=configuration.get_user_email())


def lambda_handler(event, context):
    """Entrypoint for AWS Lambda events."""
    # Initiate and run the script in AWS mode
    init()
    crawl(mode=MODE_AWS)
    return True


# Initiate and run the script in local mode
init()
crawl(mode=MODE_LOCAL)
