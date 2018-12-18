import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style, init as coloramaInit

MINIMUM_THRESHOLD = 20
books = [
    {
        "name": "Η αλγοριθμική τέχνη των αποφάσεων",
        "protoporia": "https://www.protoporia.gr/i-algorithmiki-techni-ton-apofaseon-p-491259.html",
        "politeia": "https://www.politeianet.gr/index.php?option=com_virtuemart&Itemid=89&keyword=%CE%97+%CE%B1%CE%BB%CE%B3%CE%BF%CF%81%CE%B9%CE%B8%CE%BC%CE%B9%CE%BA%CE%AE+%CF%84%CE%AD%CF%87%CE%BD%CE%B7+%CF%84%CF%89%CE%BD+%CE%B1%CF%80%CE%BF%CF%86%CE%AC%CF%83%CE%B5%CF%89%CE%BD&limitstart=0"
    },
    {
        "name": "Αγριοτρενο",
        "protoporia": "https://www.protoporia.gr/to-agriotreno-p-490623.html",
        "politeia": "https://www.politeianet.gr/index.php?option=com_virtuemart&Itemid=89&keyword=%09+%CE%A4%CE%BF+%CE%91%CE%B3%CF%81%CE%B9%CF%8C%CF%84%CF%81%CE%B5%CE%BD%CE%BF&limitstart=0"
    },
]


def printMesage(name, discount, vendor):
    """Print the message to the user."""
    message = "{} {}% discount in {}".format(
        name,
        discount,
        vendor
    )
    if int(discount) >= MINIMUM_THRESHOLD:
        print(Fore.RED + message)
        # Reset the style back to normal
        print(Style.RESET_ALL)
    else:
        print(message)


def getParser(link):
    """Return the html parser."""
    code = requests.get(link)
    plain = code.text
    return BeautifulSoup(plain, "html.parser")


def parseDiscount(element):
    """Given an HTML element, parse and return the discount."""
    try:
        # Remove any non integer characters from the HTML element
        discount = re.sub("\D", "", element)
    except AttributeError:
        discount = "0"
    return discount


def crawl():
    """Iterate through a list of books, print the discount (if any) for both providers."""
    for book in books:
        if book.get("protoporia"):
            parser = getParser(book["protoporia"])
            # Extract HTML element info from the DOM
            element = parser.find(
                "td", {"class": "productSpecialPrice"}
            ).findAll("span")[1].string
            discount = parseDiscount(element)
            printMesage(book["name"], discount, "Protoporia")

        if book.get("politeia"):
            parser = getParser(book["politeia"])
            # Extract HTML element info from the DOM
            element = parser.find("td", {"class": "pricediscount2"}).string
            discount = parseDiscount(element)
            printMesage(book["name"], discount, "Politeia")
        print("<---------------------------------------------------->")


# Initialise colorama for terminal text
coloramaInit()
# Crawl for updates
crawl()
