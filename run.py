from colorama import init as colorama_init
from config.configurator import Configurator
from vendors.bookshops import ProtoporiaBookshop, PoliteiaBookshop
from common.helpers import print_mesage, print_error_message, print_end_of_element
from common.options_handler import OptionsHandler

ERROR_NOT_FOUND = "Book wasn't found."
ERROR_USER_INPUT = "Invalid user input."


def crawl():
    """Iterate through a list of books, print the discount (if any) for both providers."""
    configuration = Configurator()
    vendors = (PoliteiaBookshop(), ProtoporiaBookshop())
    books = configuration.get_books()

    for book in books:
        for vendor in vendors:
            # If there is a link for that specific vendor, visit the direct page
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

            # Perform a search
            try: 
                book_choices = vendor.search(book)
                options_handler = OptionsHandler(book_choices, vendor)
                options_handler.display_choices()
                user_choice = options_handler.ask_input()
                if int(user_choice) > len(book_choices):
                    print_error_message(
                        name=book.name, vendor=vendor.name,
                        error=ERROR_USER_INPUT
                    )
                    break
                configuration.update_configuration(book_choices[int(user_choice)], vendor)
            except IndexError:
                print_error_message(
                    name=book.name, vendor=vendor.name,
                    error=ERROR_NOT_FOUND
                )
        print_end_of_element()

# Initialise colorama for terminal text
colorama_init()
# Crawl for updates
crawl()
