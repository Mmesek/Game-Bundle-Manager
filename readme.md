A simple DB manager for bundles/games & scraping bazar

# Usage



## Manager
Manages Adding/Removing bundles/games from db
```sh
python manage2.0.py
```

- game [NAME] - adds game to context 
- bundle [NAME] - sets bundle name
- price [PRICE] - sets bundle price
- cc [CURRENCY] - sets price's currency
- add - commits to database games in a bundle
- remove - removes from database provided games

Batching:
- games - initializes batching games
- commit - ends batching games

## Spider
Scraps bazar for current prices
```sh
python spidey2.py
```

## Search
Searches for game in bundles
```sh
python search.py Game Title
```

## Retrieve
Retrieves games in bundle & their prices
```sh
python retrieve.py Bundle Name
```