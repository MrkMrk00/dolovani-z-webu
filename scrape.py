import os.path
from typing import Any
from pprint import pprint
from autoscraper import AutoScraper
from urllib.parse import urljoin, urlsplit

def scraper_related() -> AutoScraper:
    file_name = os.path.join(os.getcwd(), 'related.scraper')

    scraper = AutoScraper()
    if not os.path.exists(file_name):
        wanted_list = [
            '/inzerat/186394912/zanovni-dotykovy-hp-envy-x360-13-512gb16gb-zaruka.php'
        ]

        scraper.build(
            'https://pc.bazos.cz/inzerat/186394713/dotykovy-notebook-124-microsoftintel-i5-1235u16gb-ram.php',
            wanted_list=wanted_list,
        )

        scraper.save(file_name)
    else:
        scraper.load(file_name)

    return scraper


def bazos_related_products(product_url: str, levels: int = 2) -> list[str]:
    scraper = scraper_related()

    url = urlsplit(product_url)
    base_url = f'{url.scheme}://{url.netloc}/'

    fringe = [url.path]
    closed = []

    for l in range(levels):
        for _ in range(len(fringe)):
            link = fringe.pop()
            url = urljoin(base_url, link)
            closed.append(url)
            print(f'{url=} {base_url=}')

            results = scraper.get_result_similar(url)

            fringe.extend(results)

        if l == levels - 1:
            closed.extend([ urljoin(base_url, x) for x in fringe])

    return closed if levels > 0 else fringe 


def product_specs(url: str) -> dict[str, Any]:
    return


def try_scrape():
    products = bazos_related_products(
        'https://pc.bazos.cz/inzerat/186394713/dotykovy-notebook-124-microsoftintel-i5-1235u16gb-ram.php',
        levels=1,
    )

    pprint(products)

if __name__ == '__main__':
    try_scrape()

