from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import requests
import datetime


class UTSCDates:
    """A scraper for important dates at UTSC. Data is retrieved from
    https://www.utsc.utoronto.ca/registrar/dates-and-deadlines."""

    link = 'https://www.utsc.utoronto.ca/registrar/dates-and-deadlines'

    @staticmethod
    def scrape(location='.', year=None, save=True):
        Scraper.logger.info('UTSCDates initialized.')

        docs = OrderedDict()

        if save:
            for date, doc in docs.items():
                Scraper.save_json(doc, location, date)

        Scraper.logger.info('UTSC completed.')
        return docs if not save else None
