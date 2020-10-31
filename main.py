from alchemy import Games, Bundles, Prices, Keys, Base, Platforms

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from difflib import get_close_matches
with open("steamstoreindex.json") as fjson:
    index = json.load(fjson)
game_names = set(index.keys())
def check_index(game):
    if game in game_names:
        return game, index[game]
    game = get_close_matches(game, index.keys(), 1)[0]
    appid = index[game]
    return game, appid

class SQL:
    __slots__ = ('engine', 'Session')
    def __init__(self):
        #self.engine = create_engine("sqlite:///mbot.db", echo=False)#f'{db}://{user}:{password}@{location}:{port}/{name}', echo={echo})
        self.engine = create_engine("postgresql://postgres:postgres@r4:5432/bundles")
        #self.engine = create_engine(f'{db}://{user}:{password}@{location}:{port}/{name}', echo=echo)
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
#db.create_tables()
session = db.Session()

#session.add(Platforms("Steam"))
#session.add(Platforms("Uplay"))
#session.add(Platforms("Origin"))
bundles = {}
games = []
current_bundle = ''
dates = {}
prices = {}
months = {
    "January":1, "February":2, "March":3, "April":4,
    "May":5, "June":6, "July":7, "August":8,
    "September":9, "October":10, "November":11, "December":12
}
currencies = {
    '€':'EUR', '$':'USD'
}
non_steam = []
import calendar
import datetime
c = calendar.Calendar(firstweekday=calendar.SUNDAY)
with open('gam_2020.txt','r',encoding='utf-8', newline='') as file:
    for line in file:
        line = line.strip('\r\n')
        if line[0] == '-':
            current_bundle = line[1:].strip('\r\n')
            if 'Monthly' in current_bundle:
                year = current_bundle.split(' ')[1]
                month = current_bundle.split(' ')[0]
            elif 'Choice' in current_bundle:
                year = current_bundle.split(' ')[-1]
                month = current_bundle.split(' ')[-2]
            if 'Monthly' in current_bundle or 'Choice' in current_bundle:
                month = months.get(month)
                year = int(year)
                monthcal = c.monthdatescalendar(year,month)
                friday = [day for week in monthcal for day in week if day.weekday() == calendar.FRIDAY and day.month == month]
                if 'Monthly' in current_bundle:
                    friday= friday[0]
                else:
                    friday = friday[-1]
                dates[current_bundle] = friday
            bundles[current_bundle] = []
        elif line[0] == '|':
            prices[current_bundle] = (line[1:-1], currencies.get(line[-1], ''))
        elif line[0] == '/':
            year, month, day = line[1:].split('-')
            dates[current_bundle] = datetime.date(int(year), int(month), int(day))
        else:
            game = line
            try:
                game, steam_id = check_index(game)
            except:
                non_steam.append(game)
            bundles[current_bundle].append(game)
            games.append(game)

known_games = session.query(Games.Title).all()
known_games = [game.Title for game in known_games]
for game in set(games):
    if game not in known_games:
        _game = Games(game)
        session.add(_game)
session.commit()


known_bundles = session.query(Bundles.Name).all()
known_bundles = [bundle.Name for bundle in known_bundles]
for bundle in bundles:
    if bundle not in known_bundles:
        _prc, _currency = prices.get(bundle, (0,''))
        prc = '12' if 'Monthly' in bundle or 'Choice' in bundle else _prc
        currency = 'USD' if 'Monthly' in bundle or 'Choice' in bundle else _currency
        _bundle = Bundles(bundle, bundles[bundle], prc, currency, dates.get(bundle, datetime.date(2020, 9, 15)))
        session.add(_bundle)
session.commit()


for game in set(games):
    platform = "Steam" if game not in non_steam else "Uplay"
    key = Keys(game, platform, games.count(game))
    session.merge(key)
session.commit()