import requests
import pandas as pd

class CountryData:
    def __init__(self, url):
        self.url = url
        self.data = None

    def fetch_data(self):
        res = requests.get(self.url)
        if res.status_code == 200: self.data = res.json()
        else: raise requests.exceptions.HTTPError(f"Failed to retrieve data, status code: {res.status_code}")

    def create_dataframe(self):
        countries = []
        capitals = []
        flag_img_links = []
        for entry in self.data:
            countries.append(entry['name']['common'])
            capitals.append(entry['capital'][0] if 'capital' in entry else None)
            flag_img_links.append(entry['flags']['png'])

        return pd.DataFrame({
            'countries': countries,
            'capitals': capitals,
            'flags': flag_img_links
        })

if __name__ == '__main__':
    scrapper = CountryData('https://restcountries.com/v3.1/all')
    scrapper.fetch_data()
    df = scrapper.create_dataframe()
    print(df)