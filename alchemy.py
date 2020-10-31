from sqlalchemy import Column, String, Integer, JSON, ForeignKey, Boolean, BigInteger, Time, BLOB, PickleType, Date, create_engine, Table, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
Base = declarative_base()

class Games(Base):
    __tablename__ = "Games"
    Title = Column(String, primary_key=True)
    def __init__(self, title):
        self.Title = title

class Bundles(Base):
    __tablename__ = "Bundles"
    Name = Column(String, primary_key=True) 
    Games = Column(ARRAY(String, ForeignKey('Games.Title')))
    Price = Column(Numeric)
    Currency = Column(String)
    Date = Column(Date)
    def __init__(self, name, games, price, currency, date):
        self.Name = name
        self.Games = games
        self.Price = price
        self.Currency = currency
        self.Date = date

class Prices(Base):
    __tablename__ = "Prices"
    Title = Column(String, ForeignKey('Games.Title'), primary_key=True)
    Price = Column(Numeric)
    Timestamp = Column(TIMESTAMP(True))
    def __init__(self, title, price, timestamp):
        self.Title = title
        self.Price = price
        self.Timestamp = timestamp

class Keys(Base):
    __tablename__ = "Keys"
    Title = Column(String, ForeignKey("Games.Title"), primary_key=True)
    Platform = Column(String, ForeignKey("Platforms.Name"))
    Quantity = Column(Integer)
    def __init__(self, title, platform, quantity):
        self.Title = title
        self.Platform = platform
        self.Quantity = quantity

class Offers(Base):
    __tablename__ = "Offers"
    Title = Column(String, primary_key=True)
    Price = Column(Numeric)
    Timestamp = Column(TIMESTAMP(True))
    def __init__(self, title, price, timestamp):
        self.Title = title
        self.Price = price
        self.Timestamp = timestamp

#class OwnedGames(Base):
#    __tablename__ = "OwnedGames"
#    Title = Column(String, ForeignKey("Games.Title"), primary_key=True)
#    Platforms = Column(ARRAY(String, ForeignKey('Platforms.Name')))
#    Completed = Column(Boolean)

#class Wishlist(Base):
#    __tablename__ = "Wishlist"
#    Title = Column(String, ForeignKey("Games.Title"), primary_key=True)
#    AddedDate = Column(Date)

class Platforms(Base):
    __tablename__ = "Platforms"
    Name = Column(String, primary_key=True)
    def __init__(self, name):
        self.Name = name

#class Achievements(Base):
#    __tablename__ = "Achievements":
#    Title = Column(String, ForeignKey("Games.Title"), primary_key=True)
#    AchievementID = Column(String, primary_key=True)
#    Achievement = Column(String)