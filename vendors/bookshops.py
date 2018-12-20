from vendors.utils import parse_discount, get_html_parser


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
        parser = get_html_parser(link)
        element = parser.findAll(
            "table", {"class": "productListing"}
        )[0].findAll("tr")[1]
        # Extract name price and discount from the page
        name = element.find("td", {"class": "txtSmallHeader"}).string
        price = element.find("span", {"class": "productpriceList"}).string
        discount = parse_discount(element.find("font", {"color": "red"}).string)
        return name, price, discount


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
        parser = get_html_parser(link)
        element = parser.findAll("tr")[0]
        name = element.find("a", {"class": "browse-product-title"}).string
        price = element.find("span", {"class": "productPrice"}).string
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
        return name, price, discount


class Book:
    """A book entity."""
    def __init__(self, **kwargs):
        """Constructor."""
        self.__dict__.update(kwargs)
