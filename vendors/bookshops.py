from vendors.utils import parse_discount, get_html_parser
from common.constants import MINIMUM_THRESHOLD, PRINT_DISCOUNT, PRINT_NORMAL, PRINT_HIDE


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

    """Protoporia bookshop"""
    def get(self, book):
        """Given a book, get its data from Protoporia."""
        parser = get_html_parser(book.protoporia)
        # Extract HTML element info from the DOM
        element = parser.find(
            "td", {"class": "productSpecialPrice"}
        ).findAll("span")[1].string
        discount = parse_discount(element)
        return book.name, discount

    def search(self, book):
        """Given a book name, make a search in Protoporia and return info for the first match."""
        link = "{}{}".format(
            self.SEARCH_LINK,
            book.name.replace(" ", "+")
        )
        book_list = []
        parser = get_html_parser(link)
        book_search = parser.findAll(
            "table", {"class": "productListing"}
        )
        for book in book_search:
            element = book.findAll("tr")[1]
            # Extract name price and discount from the page
            name = element.find("td", {"class": "txtSmallHeader"}).string
            price = element.find("span", {"class": "productpriceList"}).string
            discount = parse_discount(element.find("font", {"color": "red"}).string)
            book_list.append(
                Book(**{'name': name, 'price': price, 'discount': discount})
            )
        return book_list


class PoliteiaBookshop(BaseBookshop):
    """Politeia bookshop."""

    SHOP_NAME = "politeia"
    SEARCH_LINK = "https://www.politeianet.gr/index.php?option=com_virtuemart&Itemid=89&keyword="

    def get(self, book):
        """Given a book, get its data form Politeia."""
        parser = get_html_parser(book.politeia)
        # Extract HTML element info from the DOM
        element = parser.find("td", {"class": "pricediscount2"}).string
        discount = parse_discount(element)
        return book.name, discount

    def search(self, book):
        """Given a book name, make a search in Politeia and return info for the first match."""
        link = "{}{}".format(
            self.SEARCH_LINK,
            book.name.replace(" ", "+")
        )
        book_list = []
        parser = get_html_parser(link)
        book_search = parser.findAll("div", {"class": "browse-page-block"})
        for element in book_search:
            name = element.find("a", {"class": "browse-product-title"}).string
            try:
                price = element.find("span", {"class": "productPrice"}).string
            except AttributeError:
                price = None

            discountElement = element.find("td", {"class": "priceDiscount"})

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
                Book(**{'name': name, 'price': price, 'discount': discount})
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

    def discount_type(self, discount):
        """Depending on the settings of each book, determine about the notification type
        that will be displayed to the user.
        """
        try:
            # Check for custom threshold limit
            if int(discount) >= self.settings['MINIMUM_THRESHOLD']:
                return PRINT_DISCOUNT
            return self.get_visibility()
        except AttributeError:
            pass
        # Check for the default limit
        if int(discount) >= MINIMUM_THRESHOLD:
            return PRINT_DISCOUNT

        return self.get_visibility()
