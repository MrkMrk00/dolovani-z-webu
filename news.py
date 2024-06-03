from autoscraper import AutoScraper
from pprint import pprint
import sys

LEARN_RULESET = [
    ('https://www.ceskenoviny.cz/cr/', 'ctk', {
        'title': [' Za navýšení peněz na vysoké školství demonstrovalo v Praze několik set lidí'],
        'url': ['/zpravy/hasici-na-jihu-moravy-dnes-odcerpavali-po-bourkach-vodu-ze-sklepu-i-garazi-/2526872'],
        'datetime': ['3.06.2024 18:18'],
    }),
    ('https://ct24.ceskatelevize.cz/tema/hlavni-udalosti-90196', 'ct-main', {
        'title': ['Schodek rozpočtu se prohloubil na 210 miliard korun'],
        'url': ['/clanek/ekonomika/rozpocet-skoncil-na-konci-kvetna-se-schodkem-210-miliard-korun-349875'],
        'datetime': ['14:01'],
    }),
    ('https://ct24.ceskatelevize.cz/tema/ruska-invaze-na-ukrajinu-58', 'ct-ua', {
        'title': ['Rusko vypálilo desítky dronů a raket na ukrajinskou energetickou síť'],
        'url': ['/clanek/svet/rusko-vypalilo-desitky-dronu-a-raket-na-ukrajinske-energeticke-site-349827'],
        'datetime': [], # není
    }),
    ('https://www.seznamzpravy.cz/sekce/domaci-13', 'seznam', {
        'title': ['ANO chtělo vydat inzerát s migranty na člunu. Nakonec vyšel jiný'],
        'url': ['https://www.seznamzpravy.cz/clanek/volby-eurovolby-ano-chtelo-vydat-inzerat-s-migranty-na-clunu-na-posledni-chvili-couvlo-253046'],
        'datetime': ['2024-06-03 17:30:00'],
    }),
]

SOURCES = [
    'https://www.ceskenoviny.cz/cr/',
    'https://www.ceskenoviny.cz/svet/',
    'https://www.ceskenoviny.cz/kultura/',
    'https://ct24.ceskatelevize.cz/tema/hlavni-udalosti-90196',
    'https://ct24.ceskatelevize.cz/tema/volby-do-evropskeho-parlamentu-2681',
    'https://ct24.ceskatelevize.cz/tema/ruska-invaze-na-ukrajinu-58',
    'https://ct24.ceskatelevize.cz/rubrika/ekonomika-17',
    'https://www.seznamzpravy.cz/sekce/volby-eurovolby-234',
    'https://www.seznamzpravy.cz/sekce/domaci-kauzy-7',
    'https://www.seznamzpravy.cz/sekce/nazory-komentare-246',
]

SCRAPER_CACHE: AutoScraper | None = None

def build_scraper() -> AutoScraper:
    global SCRAPER_CACHE

    if SCRAPER_CACHE is None:
        scraper = AutoScraper()

        for url, source, rule_list in LEARN_RULESET:
            for alias, wanted_list in rule_list.items():
                scraper.build(url=url, wanted_dict={f'{source}.{alias}': wanted_list}, update=True)

        SCRAPER_CACHE = scraper

    return SCRAPER_CACHE


def prepare_results(scraped_raw: dict) -> list[dict]:
    keys = [ k for k, v in scraped_raw.items() if len(v) > 0 ]
    if len(keys) == 0:
        return []

    results = []
    for i in range(len(scraped_raw[keys[0]])):
        values = []
        for k in keys:
            key_str = k.split('.')[1]
            if len(scraped_raw[k]) <= i:
                values.append((key_str, ''))
            else:
                values.append((key_str, scraped_raw[k][i]))

            results.append(dict(values))

    return results


def scrape():
    results = []
    scraper = build_scraper()

    for url in SOURCES:
        scraped_raw = scraper.get_result_similar(url, group_by_alias=True, grouped=True, keep_order=True)
        scraped = prepare_results(scraped_raw)

        if len(scraped) == 0:
            print(f'Nepodařilo se scrapovat z {url}')

        results.append(scraped)


    if '--noprint' not in sys.argv:
        pprint(results)

if __name__ == '__main__':
    scrape()

