import json
import sys
import os
from vendors.bookshops import Book


class Configurator():
    """Responsible for setting up the configuration."""

    def __init__(self):
        """"Constructor."""
        self.configuration = json.loads(
            open(self.get_config_path()).read()
        )

    def get_config_path(self):
        """Return the path of the configuration file."""
        relative_path = "library.json"
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_books(self):
        """Return all books from the configuration."""
        return [Book(**book_config) for book_config in self.configuration["books"]]

    def get_settings(self):
        """Return settings from the configuration."""
        return self.configuration["settings"]

    def update_configuration(self, book_to_update, vendor):
        """Update the link for a specific vendor, for a specific book."""
        for pos, book in enumerate(self.configuration["books"]):
            if book_to_update.name == book["name"]:
                self.configuration["books"][pos][vendor.name] = book_to_update.link
                break

        self.save()
        return True

    def save(self):
        """Save the configuration back to the json file."""
        file = open(self.get_config_path(), "w+")
        file.write(json.dumps(self.configuration, indent=4, ensure_ascii=False))
        file.close()
