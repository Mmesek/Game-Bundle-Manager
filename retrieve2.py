import base
from decimal import Decimal
from alchemy import Keys, Bundles, Prices, Offers
from difflib import get_close_matches

import re
sanitizer = re.compile(r"\w+")
def sanitize(string):
    s = sanitizer.findall(string)
    return ' '.join(s).lower()

session = base.db.session()
prices = session.query(Prices).all()
keys = session.query(Keys).all()
bundles = session.query(Bundles).order_by(Bundles.Date.desc()).all()
_bundles = []
games = {sanitize(i.Title):i.Quantity for i in keys}
offers = session.query(Offers).all()
_offers = {sanitize(i.Title):i.Price for i in offers}
#_offers = {sanitize(i.Title):[] for i in offers}
#for i in offers:
#    _offers[sanitize(i.Title)].append(i.Price)
_prices = {sanitize(i.Title):i.Price for i in prices}
wl = [sanitize(i.strip()) for i in open('db/wl.txt')]
_wl = []
_wl_prices = []
print('Games:',len(games), 'Prices:',len(_prices), 'Offers:',len(offers))   
print('Offers',sum(_offers.values()))
print('Prices',sum(_prices.values()))
for bundle in bundles:
    _bundle = []
    _iwl = []
    _bundle_prc = []
    _offers_prc = []
    for game in bundle.Games:
        sanitized = sanitize(game)
        if sanitized in games:
            g = [_prices.get(sanitized, Decimal(0.0)), game]
            if sanitized in _offers:
                g.append(str(_offers.get(sanitized, Decimal(0.0))))
                _offers_prc.append(_offers.get(sanitized, Decimal(0.0)))
                #_offers[sanitized] = None
            else:
                try:
                    close_match = get_close_matches(sanitized, _offers.keys(), 1, cutoff=0.75)[0]
                    g.append(str(_offers.get(close_match, Decimal(0.0))))
                    g.append(close_match)
                    _offers_prc.append(_offers.get(close_match, Decimal(0.0)))
                    #_offers[close_match] = None
                except:
                    pass
                #g.append(str(_offers.get(sanitized, [Decimal(0.0)]).pop(0)))
            if sanitized not in wl:
                _bundle.append(g)
                _bundle_prc.append(g[0])
            else:
                _iwl.append(g)
                _wl_prices.append(g[0])
            games[sanitized] -= 1
    _bundle.sort(key=lambda i: i[0], reverse=True)
    #_bundle = '\n'.join([str(i[1]) for i in _bundle])
    _bundle = '\n- '.join([' - '.join([str(s) if s != Decimal(0.0) else '0' for s in i]) for i in _bundle])
    _iwl = '\n- '.join([' - '.join([str(s) if s != Decimal(0.0) else '0' for s in i]) for i in _iwl])
    if _bundle != '':
        #print("\n\nBundle", bundle.Name)
        _bundle = "Bundle " + bundle.Name + ': '+ str(sum(_bundle_prc)) +'. Offers: '+ str(sum(_offers_prc)) + '\n- '+_bundle
        _bundles.append(_bundle)
    if _iwl != '':
        _wl.append(_iwl)
print('Bundles:',len(_bundles), '/', len(bundles))
left = ['Left']
with open('db/gam2.txt','r',newline='',encoding='utf-8') as file:
    for line in file:
        if line.strip() not in games:
            left.append(line.strip())
print(sum(_wl_prices))
games = ["\nRemaining games:"] + [i for i in games if games[i] != 0]
with open('games_in_bundles.txt','w',newline='',encoding='utf-8') as file:
    file.writelines('\n\n'.join(_bundles))
    file.writelines('\n'.join(games))
    file.writelines('\n'.join(['\n']+[i +' - '+ str(_offers[i]) for i in _offers if _offers[i] is not None]))
    file.writelines('\n'.join(['\n']+_wl))

with open('not_found_games.txt','w',newline='',encoding='utf-8') as file:
    file.writelines('\n'.join(left))
