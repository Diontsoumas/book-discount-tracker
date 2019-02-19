from vendors.utils import parse_discount, get_html_parser
from common.constants import (MINIMUM_THRESHOLD, PRINT_DISCOUNT, PRINT_NORMAL, PRINT_HIDE,
                              BOOK_NOT_FOUND)


class BaseBookshop:
    """Base bookshop class."""

    def __init__(self):
        """Constructor."""
        self.name = self.SHOP_NAME

    def search(self, book):
        """Make a search."""
        raise NotImplementedError()

    def get(self, book):
        """Get a specific book."""
        raise NotImplementedError()


class ProtoporiaBookshop(BaseBookshop):
    SHOP_NAME = "protoporia"
    SEARCH_LINK = "https://www.protoporia.gr/advanced_search_result.php?keywords="
    BOOK_NOT_FOUNT_COPY = "Δεν υπάρχει βιβλίο που ταιριάζει στα κριτήρια αναζήτησης."

    """Protoporia bookshop"""
    def get(self, book):
        """Given a book, get its data from Protoporia."""
        # If the book couldn't be found, early return
        if book.protoporia == BOOK_NOT_FOUND:
            return False

        parser = get_html_parser(book.protoporia)
        # Extract HTML element info from the DOM
        element = parser.find(
            "td", {"class": "productSpecialPrice"}
        ).findAll("span")[1].string
        discount = parse_discount(element)
        return {"discount": discount}

    def no_search_results(self, elements):
        """Determine if the returning element of a search has any results or not"""
        if (len(elements) == 1 and
                elements[0].find("td", {"class": "productListing-data"}) and
                elements[0].find("td", {"class": "productListing-data"}).string ==
                self.BOOK_NOT_FOUNT_COPY):
            return True
        return False

    def search(self, book):
        """Given a book name, make a search in Protoporia and return info for the first match."""
        link = "{}{}".format(
            self.SEARCH_LINK,
            book.name.replace(" ", "+")
        )
        book_list = []
        parser = get_html_parser(link)
        book_search = parser.find(
            "table", {"class": "productListing"}
        )

        elements = book_search.findAll("tr", recursive=False)
        # If nothing got found
        if self.no_search_results(elements):
            return book_list

        for element in elements:
            # First element is the table header, continue
            if(element.find("td", {"class": "productListing-heading"})):
                continue
            # Extract name price and discount from the page
            name = element.find("td", {"class": "txtSmallHeader"}).string
            try:
                price = element.find("span", {"class": "productpriceList"}).string
                discount = parse_discount(element.find("font", {"color": "red"}).string)
            except AttributeError:
                # Price or discount not found, probably book is not available from the
                # publisher
                price = 0
                discount = 0
            link = element.find("a", {"class": "txtSmallHeader"}).attrs["href"]
            book_list.append(
                Book(**{"name": book.name, "search_name": name, "price": price, "discount": discount, "link": link})
            )
        return book_list


class PoliteiaBookshop(BaseBookshop):
    """Politeia bookshop."""

    SHOP_NAME = "politeia"
    SEARCH_LINK = "https://www.politeianet.gr/index.php?option=com_virtuemart&Itemid=89&keyword="

    def get(self, book):
        """Given a book, get its data from Politeia."""
        # If the book couldn't be found, early return
        if book.politeia == BOOK_NOT_FOUND:
            return False

        parser = get_html_parser(book.politeia)
        # Extract HTML element info from the DOM
        try:
            element = parser.find("td", {"class": "pricediscount2"}).string
            discount = parse_discount(element)
        except AttributeError:
            # Discount element can be found in two different HTML elements
            try:
                element = parser.find("td", {"class": "pricediscount"}).string
                discount = parse_discount(element)
            except AttributeError:
                discount = 0

        return {"discount": discount}

    def search(self, book):
        """Given a book name, make a search in Politeia and return info for the first match."""
        link = "{}{}".format(
            self.SEARCH_LINK,
            book.name.replace(" ", "+")
        )
        book_list = []
        parser = get_html_parser(link)
        book_search = parser.findAll("div", {"class": "browse-page-block"})

        # If nothing got found
        if not len(book_search):
            return book_list

        for element in book_search:
            name = element.find("a", {"class": "browse-product-title"}).string
            link = element.find("a", {"class": "browse-product-title"}).attrs["href"]
            try:
                price = element.find("span", {"class": "productPrice"}).string
            except AttributeError:
                price = None

            discountElement = element.find("td", {"class": "pricediscount"})

            if not discountElement:
                # Politeia seems to have multiple discount elements, probably based on the
                # level of discount
                discountElement = element.find("td", {"class": "pricediscount2"})

            if not discountElement:
                discount = 0
            else:
                discount = parse_discount(discountElement.string)
            # Extract name price and discount from the page
            book_list.append(
                Book(**{"name": book.name, "search_name": name, "price": price, "discount": discount, "link": link})
            )
        return book_list


class Book:
    """A book entity."""
    def __init__(self, **kwargs):
        """Constructor."""
        self.__dict__.update(kwargs)

    def get_visibility(self):
        """A book may have an option to be hidden if there is not a valid discount for
        it. In this case, return the appropriate print type."""
        try:
            # Check if it needs to be hidden since there is no discount
            if self.settings['HIDE_UNLESS_HAS_VALID_DISCOUNT']:
                return PRINT_HIDE
        except AttributeError:
            pass
        return PRINT_NORMAL

    def discount_type(self):
        """Depending on the settings of each book, determine about the notification type
        that will be displayed to the user.
        """
        try:
            # Check for custom threshold limit
            if int(self.discount) >= self.settings['MINIMUM_THRESHOLD']:
                return PRINT_DISCOUNT
            return self.get_visibility()
        except AttributeError:
            pass
        # Check for the default limit
        if int(self.discount) >= MINIMUM_THRESHOLD:
            return PRINT_DISCOUNT

        return self.get_visibility()

    def update_values(self, **kwargs):
        """Update the attributes for a book."""
        self.discount = kwargs.get("discount") or 0
