import json, calendar, datetime
from alchemy import Games, Bundles, Prices, Keys, Base, Platforms

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from difflib import get_close_matches

months = {"January":1, "February":2, "March":3, "April":4,
    "May":5, "June":6, "July":7, "August":8,
    "September":9, "October":10, "November":11, "December":12}
currencies = {'€':'EUR', '$':'USD'}
c = calendar.Calendar(firstweekday=calendar.SUNDAY)

with open("steamstoreindex.json") as fjson:
    index = json.load(fjson)

game_names = set(index.keys())

def check_index(game_name):
    if game_name in game_names:
        return game_name, index[game_name]
    game_name = get_close_matches(game_name, index.keys(), 1)[0]
    return game_name, index[game_name]

class SQL:
    __slots__ = ('engine', 'Session')
    def __init__(self):
        self.engine = create_engine("postgresql://postgres:postgres@r4:5432/bundles")
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    def session(self):
        session = self.Session()
        return session
    def add(self, mapping):
        s = self.session()
        s.add(mapping)
        return s.commit()
    def delete(self, mapping):
        s = self.session()
        s.delete(mapping)
        return s.commit()
db = SQL()

def game(game_name: str, bundle: str = None, platform='Steam'):
    game_name = game_name.strip()
    try:
        game_name, steam_id = check_index(game_name)
    except:
        pass

    session = db.session()
    print(game_name)
    _game = session.query(Games.Title).filter(Games.Title == game_name).first()
    if _game is None:
        db.add(Games(game_name))

    if bundle is not None:
        bundle = session.query(Bundles).filter(Bundles.Name == bundle).first()
        if bundle is not None:
            if game_name not in bundle.Games:
                games = list(bundle.Games)
                games.append(game_name)
                bundle.Games = games
    session.commit()

    key(game_name, platform)
    return game_name

def add_bundle(bundle: str, games: list, price: float = 0.0, currency: str ='EUR'):
    _games = []
    for _game, platform in games:
        a = game(_game, bundle, platform)
        #print(a)
        _games.append(a)

    session = db.session()
    if session.query(Bundles).filter(Bundles.Name == bundle).first() is None:
        if 'Choice' in bundle:
            year = int(bundle.split(' ')[-1])
            month = months.get(bundle.split(' ')[-2])
            monthcal = c.monthdatescalendar(year,month)
            date = [day for week in monthcal for day in week if day.weekday() == calendar.FRIDAY and day.month == month][-1]
        else:
            date = datetime.date.today()
        session.add(Bundles(bundle, _games, price, currency, date))
    session.commit()

def key(game_name: str, platform: str, quantity: int = 1, add: bool = True):
    session = db.session()
    stored_key = session.query(Keys).filter(Keys.Title == game_name).first()
    if stored_key is None:
        key = Keys(game_name, platform, quantity)
        session.add(key)
    else:
        if add:
            stored_key.Quantity += quantity
        elif stored_key.Quantity > 0:
            stored_key.Quantity -= quantity
        else:
            pass
        if stored_key.Quantity == 0:
            prc = session.query(Prices).filter(Prices.Title == game_name).first()
            if prc != None:
                session.delete(prc)
            session.delete(stored_key)
    session.commit()