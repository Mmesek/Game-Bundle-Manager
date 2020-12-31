from base import db, Bundles, Prices
from decimal import Decimal
from alchemy import Offers
session = db.session()
def get_bundle(bundle_name):
    return session.query(Bundles).filter(Bundles.Name == bundle_name).first()

def get_last_bundle():
    return session.query(Bundles).order_by(Bundles.Date.desc()).first()

def get_prices():
    return session.query(Prices).all()

def get_offers():
    return session.query(Offers).all()
from sys import argv
bundle_name = []
past_file_name = False
for arg in argv:
    if arg == __file__:
        past_file_name = True
    elif past_file_name:
        bundle_name.append(arg)

bundle_name = ' '.join(bundle_name)
if bundle_name == '':
    bundle = get_last_bundle()
else:
    bundle = get_bundle(bundle_name)
bundle_prc = Decimal(0.0)
above_prc = Decimal(0.0)
above_games = {}
below_prc = Decimal(0.0)
below_games = {}
total_prc = Decimal(0.0)
bundled_games = {}
rest = {}
no_prc = []
games = [(i.Title, i.Price) for i in get_prices()]
games.sort(key=lambda i: i[1], reverse=True)
for game in games:
    print(game[0], game[1])
    if bundle is not None and game[0] in bundle.Games:
        bundle_prc += game[1]
        bundled_games[game[0]] = game[1]
    elif game[1] > Decimal(40.00):
        above_prc += game[1]
        above_games[game[0]] = game[1]
    elif game[1] == Decimal(0.00):
        no_prc.append(game[0])
    elif game[1] < Decimal(1.00):
        below_prc += game[1]
        below_games[game[0]] = game[1]
    else:
        total_prc += game[1]
        rest[game[0]] = game[1]

print("Bundle:", bundle_prc)
print(f"Bundled games ({len(bundled_games)}):", bundled_games)
print("Above 40:", above_prc)
print(f"Above games ({len(above_games)}):", above_games)
print("Below 1:", below_prc)
print(f"Below games ({len(below_games)}):", below_games)
print(f"No price games ({len(no_prc)}):", no_prc)
print(f"Total ({len(rest)}):", total_prc)
o_prc = Decimal(0.0)
o_games = []
for offer in get_offers():
    o_prc += offer.Price
    o_games.append(offer.Title)
print("Offers:", o_prc)
print(f"Games ({len(o_games)}):", o_games)