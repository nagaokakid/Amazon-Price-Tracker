class NoProductPriceFound(Exception):
    "Raised when the price of a product could not be found."
    pass

class NoProductNameFound(Exception):
    "Raised when the name of a product could not be found."
    pass

class InvalidUrl(Exception):
    "Raised when a given URL is not a valid web page."
    pass

class DatabaseError(Exception):
    "Raised when a CRUD attempt fails with products database."