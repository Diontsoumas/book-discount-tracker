import json


class Configurator():
    """Responsible for setting up the configuration."""

    def __init__(self):
        """"Constructor."""
        self.configuration = json.loads(open('files/library.json').read())

    def get_books(self):
        """Return all books from the configuration."""
        return self.configuration["books"]

    def get_settings(self):
        """Return settings from the configuration."""
        return self.configuration["settings"]
