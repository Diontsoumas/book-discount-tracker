from colorama import Fore, Back, Style
import requests
import os
from common.constants import (PRINT_DISCOUNT, PRINT_NORMAL, PRINT_HIDE,
                              PRINT_CHOICE, PRINT_INIT, PRINT_FINISHED,
                              PRINT_NEXT_ELEMENT, MODE_LOCAL, MAIL_HOSTNAME)

ERROR_NOT_FOUND = "Book wasn't found."
USER_EMAIL_NOT_FOUND = "User's email not found."
EMAIL_NOT_SENT = "Email not sent."


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
        message = " Welcome to the Book Tracker! Please wait . . . "
        print(Back.WHITE + Fore.BLACK + message + Style.RESET_ALL)
    elif type == PRINT_FINISHED:
        line = "That's all, cu soon, bye bye!"
        print(Back.WHITE + Fore.BLACK + line + Style.RESET_ALL)
    elif type == PRINT_NEXT_ELEMENT:
        line = "Next book..."
        print(Back.WHITE + Fore.BLACK + line + Style.RESET_ALL)


def print_error_message(name, vendor, error):
    """Print an error message to the user."""
    message = "{} returns an error for \"{}\": {}".format(
        vendor,
        name,
        error
    )
    print(Back.RED + message + Style.RESET_ALL)


class PrinterQueue():
    """Responsible for keeping track and showing the books to the user."""

    def __init__(self):
        """Constructor."""
        self.queue = []
        self.error_queue = []

    def add_to_print_queue(self, book, vendor):
        """Adds a book to the print queue."""
        self.queue.append({'book': book, 'vendor': vendor})

    def add_to_error_queue(self, book, vendor):
        """Adds an error to the print queue."""
        self.error_queue.append({'book': book, 'vendor': vendor})

    def show(self, mode, email=None):
        """Shows the books in the queue to the user"""
        self.print_to_console() if mode == MODE_LOCAL else self.send_email(email)

    def print_to_console(self):
        """Prints the whole queue to the user's console."""
        for msg in self.queue:
            print_mesage(type=msg.get("book").discount_type(),
                         name=msg.get("book").name,
                         vendor=msg.get("vendor").name,
                         discount=msg.get("book").discount
                         )

        for msg in self.error_queue:
            print_error_message(name=msg.get("book").name,
                                vendor=msg.get("vendor").name,
                                error=ERROR_NOT_FOUND
                                )
        print_mesage(type=PRINT_FINISHED)

    def send_email(self, email):
        """Send an email to the user with the queued books."""
        if email is False:
            raise Exception(USER_EMAIL_NOT_FOUND)

        with open("email_template.html") as f:
            email_template = f.read()

        book_msg = ""
        for msg in self.queue:
            book_msg += "- {} {}% discount in {} <br>".format(
                msg.get("book").name,
                msg.get("book").discount,
                msg.get("vendor").name
            )
        request = requests.post(os.environ.get("EMAIL_REQUEST_URL"),
                                auth=("api", os.environ.get("EMAIL_API_KEY")),
                                data={"from": MAIL_HOSTNAME,
                                      "to": email,
                                      "subject": "Your daily book tracker summary",
                                      "html": email_template.replace("{book_msg}",
                                                                     book_msg)
                                      })
        if request.status_code != 200:
            raise Exception(EMAIL_NOT_SENT)
