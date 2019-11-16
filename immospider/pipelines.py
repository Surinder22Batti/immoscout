# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import googlemaps
import datetime
import shelve
from scrapy.exceptions import DropItem
import sqlite3
from immospider.items import ImmoscoutItem

# see https://doc.scrapy.org/en/latest/topics/item-pipeline.html#duplicates-filter
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = shelve.open("immo_items.db")

    def process_item(self, item, spider):
        immo_id = item['immo_id']

        if immo_id in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item['url'])
        else:
            self.ids_seen[immo_id] = item
            return item

class SQlitePipeline(object):
# Help in SQlite type definition
# https://www.sqlite.org/datatype3.html
# NULL. The value is a NULL value.
# INTEGER. The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
# REAL. The value is a floating point value, stored as an 8-byte IEEE floating point number.
# TEXT. The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
# BLOB. The value is a blob of data, stored exactly as it was input.

    def open_spider(self, spider):
        self.connection = sqlite3.connect("real-estate.db")
        self.c = self.connection.cursor()
        #TODO: implement the 3 values from google. They all should not be empty
        #TODO: implement better types and test. Not only the TEXT types
        #TODO: implement immo_id as key
        #TODO: dublicate key implementation
        try:
            self.c.execute('''
                CREATE TABLE immoscout(
                        immo_id INTEGER NOT NULL PRIMARY KEY,
                        url TEXT,
                        title TEXT,
                        address TEXT,
                        city TEXT,
                        zip_code INTEGER,
                        district TEXT,
                        contact_name TEXT,
                        media_count INTEGER,
                        lat REAL,
                        lng REAL,
                        sqm  REAL,
                        rent REAL,
                        rooms REAL,
                        extra_costs REAL,
                        kitchen TEXT,
                        balcony TEXT,
                        garden TEXT,
                        private TEXT,
                        area TEXT,
                        cellar TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        #TODO: implement the 3 values from google. They all should not be empty
        self.c.execute('''
            INSERT OR IGNORE INTO immoscout (immo_id, url, title, address, city, zip_code, district, contact_name, media_count, lat, lng, sqm , rent, rooms, extra_costs, kitchen, balcony, garden, private, area, cellar
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
            item['immo_id'],
            item['url'],
            item['title'],
            item['address'],
            item['city'],
            item['zip_code'],
            item['district'],
            item['contact_name'],
            item['media_count'],
            item['lat'],
            item['lng'],
            item['sqm'],
            item['rent'],
            item['rooms'],
            item['extra_costs'],
            item['kitchen'],
            item['balcony'],
            item['garden'],
            item['private'],
            item['area'],
            item['cellar'],
            #item['time_dest'],
            #item['time_dest2'],
            #item['time_dest3'],
        ))
        self.connection.commit()
        return item

class GooglemapsPipeline(object):

    # see https://stackoverflow.com/questions/14075941/how-to-access-scrapy-settings-from-item-pipeline
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        gm_key = settings.get("GM_KEY")
        return cls(gm_key)

    def __init__(self, gm_key):
        if gm_key:
            self.gm_client = googlemaps.Client(gm_key)

    def _get_destinations(self, spider):
        destinations = []

        if hasattr(spider, "dest"):
            mode = getattr(spider, "mode", "driving")
            destinations.append((spider.dest, mode))
        if hasattr(spider, "dest2"):
            mode2 = getattr(spider, "mode2", "driving")
            destinations.append((spider.dest2, mode2))
        if hasattr(spider, "dest3"):
            mode3 = getattr(spider, "mode3", "driving")
            destinations.append((spider.dest3, mode3))

        return destinations

    def _next_monday_eight_oclock(self, now):
        monday = now - datetime.timedelta(days=now.weekday())
        if monday < monday.replace(hour=8, minute=0, second=0, microsecond=0):
            return monday.replace(hour=8, minute=0, second=0, microsecond=0)
        else:
            return (monday + datetime.timedelta(weeks=1)).replace(hour=8, minute=0, second=0, microsecond=0)

    def process_item(self, item, spider):
        if hasattr(self, "gm_client"):
            # see https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime
            next_monday_at_eight = (self._next_monday_eight_oclock(datetime.datetime.now())
                                         - datetime.datetime(1970, 1, 1)).total_seconds()

            destinations = self._get_destinations(spider)
            travel_times = []
            for destination, mode in destinations:
                result = self.gm_client.distance_matrix(item["address"],
                                                              destination,
                                                              mode=mode,
                                                              departure_time = next_monday_at_eight)
                #  Extract the travel time from the result set
                travel_time = None
                if result["rows"]:
                    if result["rows"][0]:
                        elements = result["rows"][0]["elements"]
                        if elements[0] and "duration" in elements[0]:
                            duration = elements[0]["duration"]
                            if duration:
                                travel_time = duration["value"]

                if travel_time is not None:
                    print(destination, mode, travel_time/60.0)
                    travel_times.append(travel_time/60.0)

            item["time_dest"] = travel_times[0] if len(travel_times) > 0 else None
            item["time_dest2"] = travel_times[1] if len(travel_times) > 1 else None
            item["time_dest3"] = travel_times[2] if len(travel_times) > 2 else None

        return item
