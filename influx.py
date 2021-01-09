from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS 
import datetime

class Influx:
    __slots__ = ('influx', 'write_api', 'query_api')
    def __init__(self):
        self.influx = InfluxDBClient(url="http://r4:8086", token="root:root", org='-')
        self.write_api = self.influx.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.influx.query_api()

    def Prices(self, game, price):
        self.write_api.write(bucket="Prices/autogen", record=(
            Point("Prices")
            .tag("game", game)
            .field("price", price))
        )
