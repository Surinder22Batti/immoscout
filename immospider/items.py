# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImmoscoutItem(scrapy.Item):
    # define the fields for your item here like:
    #  name = scrapy.Field()
    immo_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    retype = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    street = scrapy.Field()
    housenumber = scrapy.Field()
    precisehousenumber = scrapy.Field()
    zip_code = scrapy.Field()
    district = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    balcony = scrapy.Field()
    kitchen = scrapy.Field()
    cellar = scrapy.Field()
    companywidecustomerid = scrapy.Field()
    contcompany = scrapy.Field()
    contname = scrapy.Field()
    contfirstname = scrapy.Field()
    contlastname = scrapy.Field()
    contphonenumber = scrapy.Field()
    contsalutation = scrapy.Field()
    hascourtage = scrapy.Field()
    floorplan = scrapy.Field()
    garden = scrapy.Field()
    guesttoilet = scrapy.Field()
    isbarrierfree = scrapy.Field()
    lift = scrapy.Field()
    listingtype = scrapy.Field()
    livingspace  = scrapy.Field()
    numberofrooms = scrapy.Field()
    currency = scrapy.Field()
    marketingtype = scrapy.Field()
    priceintervaltype = scrapy.Field()
    value = scrapy.Field()
    privateoffer = scrapy.Field()
    realtorcompanyname = scrapy.Field()
    realtorlogo = scrapy.Field()
    spotlightlisting = scrapy.Field()
    streamingvideo = scrapy.Field()
    creation = scrapy.Field()
    media_count = scrapy.Field()
    time_dest = scrapy.Field()  # time to destination using transit or driving
    time_dest2 = scrapy.Field()
    time_dest3 = scrapy.Field()

    provision1 = scrapy.Field()
    provision2 = scrapy.Field()
    land_transfer1 = scrapy.Field()
    land_transfer2 = scrapy.Field()
    notary1 = scrapy.Field()
    notary2 = scrapy.Field()
    entry_land1 = scrapy.Field()
    entry_land2 = scrapy.Field()

    criteriagroup = scrapy.Field()
    objektbeschreibung = scrapy.Field()
    sonstiges = scrapy.Field()

