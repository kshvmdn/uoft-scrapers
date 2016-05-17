from ..utils import Scraper
from .utsg import UTSGDates
from .utm import UTMDates
from .dates_helpers import *


class Dates:

    @staticmethod
    def scrape(location='.', year=None):
        Scraper.logger.info('Dates initialized.')

        docs = merge_events([UTSGDates, UTMDates], location, year)

        for date, doc in docs.items():
            Scraper.save_json(doc, location, date)

        Scraper.logger.info('Dates completed.')
