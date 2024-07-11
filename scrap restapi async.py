# Сенсу від асинхронного методу немає, адже ми робимо всього один запит, але зайвим не буде

import pandas as pd
import asyncio, aiohttp

class CountryData:https://github.com/yaGeey/scrap-test/blob/main/scrap%20restapi%20async.py#L1C0
    def __init__(self, url):
        self.url = url
        self.data = None

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as res:
                if res.status == 200: self.data = await res.json()
                else: raise aiohttp.ClientResponseError(
                        request_info=res.request_info,
                        history=res.history,
                        status=res.status,
                        message=f"Failed to retrieve data",
                        headers=res.headers
                    )

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

async def main():
    scrapper = CountryData('https://restcountries.com/v3.1/all')
    await scrapper.fetch_data()
    df = scrapper.create_dataframe()
    print(df)

if __name__ == '__main__':
    asyncio.run(main())
