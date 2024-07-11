import re, json, time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
URL = 'https://www.ebay.com/itm/285946652008?itmmeta=01J2EN7NVTJ70J2DCGRF1SNYK4&hash=item4293bfa568:g:me4AAOSw10lmih5~&itmprp=enc%3AAQAJAAAAwMZ82qy%2Fk28BU%2FYuDeY1kgDLpAE1Vp3cIUppQ3j6zCDRFqBziyrfRZbyPPbQQCmOWA5ibFtd5VF7ni3Ti4PTZksbmBrS%2FtfgRji7fsp7InLQ9UDaGn1xBHJok85uiB5%2BQZldAD6hYEdZzKcKcurIsl8EPtKm5YJUnTgTIGGblebdQm1OGrkSqgGj1lngrQJXjb0nuDxhWbRzClbPmZjyK88ah3IvuAU6hvuYYP%2BLXKQZ%2Bsm4S6Di1xYcqVLdYfQIyw%3D%3D%7Ctkp%3ABk9SR_zdntWTZA'

class EBayProductScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}

    def _str_to_float(self, text):
        try: return float(text)
        except ValueError:  return None

    def fetch_data(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'html.parser')

        self.data['title'] = soup.find(class_='x-item-title__mainTitle').text.strip()
        self.data['img_link'] = soup.find('img', alt=re.compile(re.escape(self.data['title']))).get('data-zoom-src')
        self.data['link'] = self.url
        self.data['price'] = self._str_to_float(soup.find(class_='x-price-primary').text.split('$')[-1])
        self.data['seller'] = soup.find(class_='x-sellercard-atf__info__about-seller').find('span').text
        self.data['shipping_price'] = self._str_to_float(soup.find(class_='ux-labels-values__values-content').span.text.split('$')[-1])

    def save_data(self, filename):
        with open(f'{filename}.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def display_data(self):
        pprint(self.data)

if __name__ == '__main__':
    scrapper = EBayProductScraper(URL)
    scrapper.fetch_data()
    scrapper.save_data(f'eBay-{int(time.time())}')
    scrapper.display_data()
