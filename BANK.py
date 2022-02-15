import requests
import re
from bs4 import BeautifulSoup




class AkBarsBank:

    def dollar_price(self):
        url = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=%D0%BA%D1%83&aqs=edge.1.69i57j0i131i433i512l4j0i131i433j0i131i433i512j69i61l2.4337j0j1&sourceid=chrome&ie=UTF-8'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty'
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            return 'Страница с ценой на доллар отвечает не корректно'

        response = response.text

        soup = BeautifulSoup(response, "html.parser")


        try:
            dollar_price = soup.find("span", class_="DFlfde SwHCTb").get_text()
            dollar_price = dollar_price.replace(',', '.')
            dollar_price = float(dollar_price)
        except:
            return 'Не могу найти цену за доллар'

        return dollar_price

