import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from immospider.spiders.immoscout import ImmoscoutSpider


process = CrawlerProcess(settings=get_project_settings())
#process.crawl(ImmoscoutSpider, url="https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00")
process.crawl(ImmoscoutSpider, url="https://www.immobilienscout24.de/Suche/S-T/Wohnung-Kauf/Nordrhein-Westfalen/Dortmund/-/-/-/EURO-50000,00-150000,00?enteredFrom=result_list")
process.start()


# https://github.com/balzer82/immoscraper/blob/master/immoscraper.ipynb
# Input parameter for later
#b = 'Sachsen' # Bundesland
#s = 'Dresden' # Stadt
#k = 'Haus' # Wohnung oder Haus
#w = 'Kauf' # Miete oder Kauf
#url = 'http://www.immobilienscout24.de/Suche/S-T/P-%s/%s-%s/%s/%s?pagerReporting=true' % (page, k, w, b, s)