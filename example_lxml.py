from pprint import pprint
import lxml.html
import requests

def scrape_related_products():
    url = 'https://pc.bazos.cz/inzerat/186496336/dotykovy-notebook-124-microsoftintel-i5-1235u16gb-ram.php'

    html = requests.get(url).content
    doc = lxml.html.fromstring(html)

    anchors = doc.cssselect('.inzeraty .inzeratynadpis > a:nth-child(1)')
    pprint([ a.get('href') for a in anchors ])


if __name__ == '__main__':
    scrape_related_products()

