import json
import sys
import os
import boto3
from vendors.bookshops import Book
from common.constants import LIBRARY_FILE_NAME, BUCKET_NAME


class Configurator():
    """Responsible for setting up the configuration."""

    def __init__(self, s3_key=None):
        """"Constructor."""
        if(s3_key):
            s3 = boto3.resource('s3')
            obj = s3.Object(BUCKET_NAME, s3_key)
            self.configuration = json.loads(
                obj.get()['Body'].read().decode('utf-8')
            )
        else:
            self.configuration = json.loads(
                open(self.get_config_path()).read()
            )

    def get_config_path(self):
        """Return the path of the configuration file."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # PyInstaller is not used, so use the absolute path instead
            base_path = os.path.abspath(".")
        return os.path.join(base_path, LIBRARY_FILE_NAME)

    def get_books(self):
        """Return all books from the configuration."""
        return [Book(**book_config) for book_config in self.configuration["books"]]

    def get_user_email(self):
        """Return the user's email"""
        try:
            return self.configuration["settings"]["email"]
        except AttributeError:
            return False

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
        """Save the configuration back to the JSON file."""
        file = open(self.get_config_path(), "w+")
        file.write(json.dumps(self.configuration, indent=4, ensure_ascii=False))
        file.close()
