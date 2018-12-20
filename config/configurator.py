import json
from vendors.bookshops import Book


class Configurator():
    """Responsible for setting up the configuration."""

    def __init__(self):
        """"Constructor."""
        self.configuration = json.loads(open('files/library.json').read())

    def get_books(self):
        """Return all books from the configuration."""
        return [Book(**book_config) for book_config in self.configuration["books"]]

    def get_settings(self):
        """Return settings from the configuration."""
        return self.configuration["settings"]
