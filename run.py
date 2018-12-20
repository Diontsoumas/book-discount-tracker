import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Back, Style, init as coloramaInit
from common.constants import MINIMUM_THRESHOLD
from config.configurator import Configurator

ERROR_NOT_FOUND = "Book not found."


def printMesage(name, vendor, discount=None):
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


def printErrorMesage(name, vendor, error):
    """Print an error message to the user."""
    message = "{} returns an error for \"{}\": {}".format(
        vendor,
        name,
        error
    )
    print(Back.RED + message + Style.RESET_ALL)


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


def searchInProtoporia(book):
    """Given a book name, make a search in Protoporia and return info for the first match."""
    link = "https://www.protoporia.gr/advanced_search_result.php?keywords={}".format(
        book["name"].replace(" ", "+")
    )
    parser = getParser(link)
    element = parser.findAll(
        "table", {"class": "productListing"}
    )[0].findAll("tr")[1]
    name = element.find("td", {"class": "txtSmallHeader"}).string
    price = element.find("span", {"class": "productpriceList"}).string
    discount = parseDiscount(element.find("font", {"color": "red"}).string)
    return name, price, discount


def searchInPoliteia(book):
    """Given a book name, make a search in Politeia and return info for the first match."""
    link = "https://www.politeianet.gr/index.php?option=com_virtuemart&Itemid=89&keyword={}".format(
        book["name"].replace(" ", "+")
    )
    parser = getParser(link)
    element = parser.findAll("tr")[0]
    name = element.find("a", {"class": "browse-product-title"}).string
    price = element.find("span", {"class": "productPrice"}).string
    discountElement = element.find("td", {"class": "priceDiscount"})

    if not discountElement:
        # Politeia seems to have multiple discount elements, probably based on the level
        # of discount
        discountElement = element.find("td", {"class": "pricediscount2"})

    if not discountElement:
        discount = 0
    else:
        discount = parseDiscount(discountElement.string)
    return name, price, discount


def getFromProtoporia(book):
    """Given a book, get its data form Protoporia."""
    parser = getParser(book["protoporia"])
    # Extract HTML element info from the DOM
    element = parser.find(
        "td", {"class": "productSpecialPrice"}
    ).findAll("span")[1].string
    discount = parseDiscount(element)
    return book["name"], discount


def getFromPoliteia(book):
    """Given a book, get its data form Politeia."""
    parser = getParser(book["politeia"])
    # Extract HTML element info from the DOM
    element = parser.find("td", {"class": "pricediscount2"}).string
    discount = parseDiscount(element)
    return book["name"], discount


def crawl():
    """Iterate through a list of books, print the discount (if any) for both providers."""
    configuration = Configurator()
    books = configuration.get_books()
    for book in books:
        if not book.get("protoporia") and not book.get("politeia"):
            # Only the book name is given, so apply a search first
            try:
                vendor = "protoporia"
                name, price, discount = searchInProtoporia(book)
                printMesage(name=name, discount=discount, vendor="Protoporia")
                vendor = "politeia"
                name, price, discount = searchInPoliteia(book)
                printMesage(name=name, discount=discount, vendor="Politeia")
            except IndexError:
                printErrorMesage(name=book.get("name"), vendor=vendor, error=ERROR_NOT_FOUND)
        # Search in Protoporia
        if book.get("protoporia"):
            name, discount = getFromProtoporia(book)
            printMesage(name=name, discount=discount, vendor="Protoporia")
        # Search in Politeia
        if book.get("politeia"):
            name, discount = getFromPoliteia(book)
            printMesage(name=name, discount=discount, vendor="Politeia")
        print("<---------------------------------------------------->")


# Initialise colorama for terminal text
coloramaInit()
# Crawl for updates
crawl()
