from datetime import datetime


class Product:
    # Constructors
    def __init__(self):
        self.id = None
        self.name = None
        self.start_price = None
        self.current_price = None
        self.previous_price = None
        self.availability = None
        self.creation_date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
        self.last_update = self.creation_date
        self.is_lower_price = False
        self.url = None
    def __init__(self, name, price, availability, url):
        self.id = 0
        self.name = name
        self.start_price = price
        self.current_price = price
        self.previous_price = price
        self.availability = availability
        self.creation_date = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
        self.last_update = self.creation_date
        self.is_lower_price = False
        self.url = url

    def __str__(self):
        return f"\n{self.name} + {self.current_price} + {self.availability}\n"
    
    # Set methods
    def setId(self, id):
        self.id = id
    def setName(self, name):
        self.name = name
    def setStartPrice(self, price):
        self.start_price = price
    def setCurrentPrice(self, price):
        self.current_price = price
    def setPreviousPrice(self, price):
        self.previous_price = price
    def setAvailability(self, status):
        self.availability = status
    def setCreationDate(self, date):
        self.creation_date = date
    def setLastUpdate(self, date):
        self.last_update = date
    def setIsLowerPrice(self, bool):
        self.is_lower_price = bool
    def setUrl(self, url):
        self.url = url
    
    # Get methods
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getStartPrice(self):
        return self.start_price
    def getCurrentPrice(self):
        return self.current_price
    def getPreviousPrice(self):
        return self.previous_price
    def getAvailability(self):
        return self.availability
    def getCreationDate(self):
        return self.creation_date
    def getLastUpdate(self):
        return self.last_update
    def getIsLowerPrice(self):
        return self.is_lower_price
    def getUrl(self):
        return self.url
