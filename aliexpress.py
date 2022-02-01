import requests
from bs4 import BeautifulSoup


class Ali:

    def __init__(self, url):
        self.url = url

    def get_info(self):
        '''
        Available 2 options get price
        :param url: full url of the link product from Aliexpress
        :return: dict{ 'name_product' : !, 'price: !}
        '''
        res = ''
        ALI_data_info_dict = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty'
        }

        params = {
            # 'targetUrl': 'BP'
        }

        response = requests.get( self.url, headers=headers, params=params)
        # print(response.content)
        soup = BeautifulSoup(response.text, 'html.parser')

        # get product name
        name_product = soup.find('div', class_= 'Product_Name__container__hntp3').find_next().get_text()
        print(name_product)


        # get price product
        try:
            # option number 1
            price_product = soup.find('div', class_='Product_UniformBanner__uniformBannerBox__o5qwb').find('div').find('span', class_='Product_UniformBanner__uniformBannerBoxPrice__o5qwb').get_text()
            # print(price_product)
        except:
            res = 0

        # option number 2
        if res == 0:
            res = 1
            price_product = soup.find('div', class_='Product_Price__container__1uqb8 product-price').find_next().get_text()

        price_product = self.serializater_price(price_product)

        # get photo product

        link_photo = soup.find('div', class_='Product_Gallery__imgWrapper__9bm18').find_next().get('src')

        ALI_data_info_dict['link_photo'] = link_photo
        ALI_data_info_dict['name_product'] = name_product
        ALI_data_info_dict['price_product'] = price_product
        ALI_data_info_dict['url'] = self.url

        return ALI_data_info_dict

    def serializater_price(self, price):
        price = price.replace(' ', '')
        price = price.replace('\xa0', '')

        type_int_price_list = []
        char_list = [',']  # need add character if there is new character
        for char in price:
            try:
                char = int(char)
            except:
                if char == ',':
                    char_list.remove(char)
                    type_int_price_list.append('.')

                else:
                    break

            if type(char) == int:
                char = str(char)
                type_int_price_list.append(char)


        right_price = ''.join(type_int_price_list)

        try:
            right_price = int(right_price)
        except:
            right_price = float(right_price)

        print(right_price)
        return right_price


