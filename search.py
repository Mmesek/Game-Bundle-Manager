from base import db, Bundles, Prices
from decimal import Decimal

session = db.session()
def get_bundle(searched_game):
    bundles = session.query(Bundles).all()
    for bundle in bundles:
        if searched_game in bundle.Games:
            yield bundle

def get_price(games):
    return session.query(Prices).filter(Prices.Title == game).first()

from sys import argv
name = []
past_file_name = False
for arg in argv:
    if arg == __file__:
        past_file_name = True
    elif past_file_name:
        name.append(arg)


game_name = ' '.join(name)

bundles = get_bundle(game_name)
for bundle in bundles:
    print('Bundle: ', bundle.Name)
    b_prc = Decimal(0.0)
    for game in bundle.Games:
        g = get_price(game)
        print('-', game, g.Price)
        b_prc += g.Price
    print('Bundle worth:',b_prc)
    print('-------------------------------------')
