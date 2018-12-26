from common.helpers import print_mesage
from common.constants import PRINT_CHOICE


class OptionsHandler:
    """ """

    def __init__(self, book_choices, vendor):
        """Constructor."""
        self.choices = book_choices
        self.vendor = vendor

    def display_choices(self):
        """Display a list of given books to the user"""
        for counter, book in enumerate(self.choices):
            print_mesage(
                name=" {}. {} ".format(counter, book.search_name),
                type=PRINT_CHOICE,
                discount=book.discount, vendor=self.vendor.name
            )

    def ask_input(self):
        return input("Please choose one: ")
