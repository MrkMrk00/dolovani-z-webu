from pprint import pprint
from autoscraper import AutoScraper

def scrape_related_products():
    url = 'https://pc.bazos.cz/inzerat/186496336/dotykovy-notebook-124-microsoftintel-i5-1235u16gb-ram.php'
    scraper = AutoScraper()

    links = scraper.build(url=url, wanted_list=[
        '/inzerat/186524051/notebook-lenovo-thinkpad-l13-yoga-gen-novysleva.php',
    ])

    pprint(scraper.get_result_similar(url=url, grouped=True))


if __name__ == '__main__':
    scrape_related_products()

