import requests, csv, time
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool

from base import *
bazar = "https://bazar.lowcygier.pl/?type=&title="

import re
sanitizer = re.compile(r"\w+")
def sanitize(string):
    s = sanitizer.findall(string)
    return ' '.join(s).lower()

def getprc(game):
    link = bazar+sanitize(game)#.strip('™®')
    try:
        getdata = requests.get(link, timeout=10)
    except requests.exceptions.ReadTimeout:
        return "00.00"
    if getdata.status_code == "404":
        return "00.00"
    soup = BeautifulSoup(getdata.text, "html.parser")
    try:
        if link[8] == "b":
            lis = soup.find("div", id="w0", class_="list-view")
            sel = lis.find_all("div", class_="col-md-7 col-sm-4 col-xs-6 nopadding")
            for each in sel:
                if sanitize(each.find("h4", class_="media-heading").a.text) == sanitize(game):
                    prc = (
                        each.find("p", class_="prc")
                        .text.replace(" zł", "")
                        .replace(",", ".")
                    )
                    try:
                        print(prc + game)
                    except:
                        print(prc)
                    break
                prc = "00.00"
    except AttributeError:
        return "00.00"
    try:
        if float(prc) <= 9.99 and not float(prc) == 00.0:
            prc = "0" + prc
    except UnboundLocalError:
        return "00.00"
    return prc

session = db.session()
def get_games():
    #session = db.session()
    keys = session.query(Keys).filter(Keys.Quantity >= 1).all()
    return [i.Title for i in keys]
from datetime import datetime
from influx import Influx
_infux = Influx()
def add_prc(game, s):
    _prc = getprc(game)
    s.merge(Prices(game, _prc, datetime.now()))
    _infux.Prices(game, float(_prc))

pool = Pool(2)
s = db.session()


g = get_games()

from queue import Queue
from threading import Thread
q = Queue(maxsize=0)
n_t = min(2, len(g))

for i in range(len(g)):
    q.put((g[i], s if i % 2 == 0 else session))
queued = time.time()

def crawl(q,i):
    while not q.empty():
        work = q.get()
        try:
            add_prc(work[0], work[1])
        except Exception as ex:
            print('Exception:', ex)
        q.task_done()
    return True
    
for i in range(n_t):
    worker = Thread(target=crawl, args=(q, i))
    worker.setDaemon(False)
    worker.start()
q.join()

#results = pool.map(add_prc, get_games(), [s, session])
session.commit()
s.commit()
_infux.influx.close()