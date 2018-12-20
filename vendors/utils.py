import re
import requests
from bs4 import BeautifulSoup


def parse_discount(element):
    """Given an HTML element, parse and return the discount."""
    try:
        # Remove any non integer characters from the HTML element
        discount = re.sub("\D", "", element)
    except AttributeError:
        discount = "0"
    return discount


def get_html_parser(link):
    """Given a link,return the html parser."""
    code = requests.get(link)
    plain = code.text
    return BeautifulSoup(plain, "html.parser")
