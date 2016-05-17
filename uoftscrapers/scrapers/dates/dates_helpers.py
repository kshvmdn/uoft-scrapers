from collections import OrderedDict


def merge_events(scrapers, location, year):
    docs = OrderedDict()

    for scraper in scrapers:
        dates = scraper.scrape(location=location, year=year, save=False)

        if dates is None:
            continue

        for date, doc in dates.items():
            if date not in docs:
                docs[date] = OrderedDict([
                    ('date', date),
                    ('events', [])
                ])
            docs[date]['events'].extend(doc['events'])

    return docs
