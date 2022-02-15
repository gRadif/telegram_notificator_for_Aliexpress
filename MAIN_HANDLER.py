from DB.Tables import User, Goods, session
from Bot.Telebot import Bot
from BANK import AkBarsBank
from aliexpress import Ali
import time
import config
import re

class Data:
    is_auth_users_list = []



class DollarNotification:
    def control_dollar(self, id_user: int):
        dollar_cost = AkBarsBank().dollar_price()

        if type(dollar_cost) is str:
            Bot().send_message(id_user, f'{dollar_cost}')

        elif dollar_cost > 77.54:
            Bot().send_message(id_user, f' Доллар вырос ---> {dollar_cost} рублей')

    def current_dollar_cost(self, id_user: int):
        dollar_cost = AkBarsBank().dollar_price()

        if type(dollar_cost) is str:
            Bot().send_message(id_user, f'{dollar_cost}')
        else:
            Bot().send_message(id_user, f' Доллар ---> {dollar_cost} рублей')


class AliexpressNotification:

    def get_goods_all_data_all_users(self):
        goods_all_data_list = []
        goods_all = session.query(Goods)
        for goods in goods_all:
            temp_dict = {}
            temp_dict['id'] = goods.id
            temp_dict['link'] = goods.link
            temp_dict['price'] = goods.price
            temp_dict['user_id'] = goods.user_id

            goods_all_data_list.append(temp_dict)

        return goods_all_data_list

    def control_aliexpress(self):
        goods_all_data = self.get_goods_all_data_all_users()
        for goods in goods_all_data:
            id_user = goods['user_id']
            id_goods_in_db = goods['id']
            data_goods_in_ali = Ali(goods['link']).get_info()
            url_goods = data_goods_in_ali['url']
            price_in_ali = data_goods_in_ali['price_product']
            price_in_db = goods['price']

            if price_in_ali != price_in_db:
                update_price = session.query(Goods).filter_by(id=id_goods_in_db).update({'price': price_in_ali})
                session.commit()

                Bot().send_message(id_user, f'ЦЕНА НА ТОВАР ИЗМЕНИЛАСЬ!!!\n'
                                          f' БЫЛО = {price_in_db}, СТАЛО = {price_in_ali}\n'
                                          f'id товара = {id_goods_in_db}\n'
                                          f'{url_goods}\n')


class Handler:
    def chat_listen(self) -> dict:
        time.sleep(1)
        message = Bot().listen_chat()
        status_chat_dict = {"message": '',
                            "id_user": '',
                            'status_user': '',
                            'command': '',
                            'user_name': ''}

        # if in chat message None, return of the start cycle
        if message is None:
            status_chat_dict['message'] == None
            return status_chat_dict


        try:
            if message[0].get('edited_message') is not None:
                status_chat_dict['id_user'] = message[0]['edited_message']['chat']['id']

            else:
                status_chat_dict['id_user'] = message[0]['message']['chat']['id']
        except:
            Bot().send_message(id_dev, 'Ошибка в json при прослушивании чата ')

        # check if sended gif or photo and video, them bot don't work
        try:
            text_message = message[0]['message']['text']
        except KeyError:
            return status_chat_dict['message'] == None

        status_chat_dict['status_user'] = self.check_user_db(status_chat_dict['id_user'])
        status_chat_dict['command'] = self.check_command(text_message)
        status_chat_dict['user_name'] = message[0]['message']['chat']['first_name']
        status_chat_dict['message'] = text_message

        return status_chat_dict

    def check_user_db(self, id_user):
        query = session.query(User).filter_by(id=id_user)
        query = list(query)

        if query == []:
            return 'unauthenticated'

        elif query != []:
            return 'is_authenticated'

    def check_command(self, text_message):
        command_dict = {'/start': '/start',
                        '[аА]ли': 'али',
                        '[аА]вторизоваться': 'авторизоваться',
                        '[дД]обавь товар': 'добавь товар',
                        '[пП]окажи все': 'покажи все',
                        '[уУ]далить товар': 'удалить товар',
                        '[дД]оллар': 'доллар'}

        for command, value in command_dict.items():
            pattern = f'{command}'
            result = re.match(pattern=pattern, string=text_message)
            if result is not None:
                return value

    def is_auth_users(self):
        query = session.query(User)
        users = list(query)
        users_list = []
        for user in users:
            users_list.append(user.id)

        print(users_list)
        return users_list

class Commands:
    def hi_ali(self,id_user: int):
        Bot().send_message(id_user, 'я здесь')

    def command_start(self, id_user):
        Bot().send_message(f'{id_user}', 'Приветствую Вас!\n\n'
                                       'Мой функционал:\n\n'
                                       '- али = проверка что бот активен\n\n'
                                       '- покажи все = показывает все ваши товары в базе и проверяет их наличие на aliexpress\n\n'
                                       '- добавь товар [вместо скобок вставляем ссылку на товар] - добавить товар в базу\n\n'
                                       '- авторизоваться = добавляет Вас в базу пользователей (Без авторизации '
                                       'Вы не сможете пользоваться ботом) \n\n'
                                         '- Удалить товар [id товара] - Удаляет товар из вашего списка\n\n'
                                         '- Доллар - Показывает стоимость доллара на текущий момент')

    def autorization_in_bot(self, user_name: str, id_user: int):
        if config.access_authentication is False:
            Bot().send_message(id_user, 'Разработчик закрыл возможность авторизации')



        elif id_user not in Data.is_auth_users_list:
            Data.is_auth_users_list.append(id_user)
            reg_query = User(id=id_user, name=user_name)
            session.add(reg_query)
            session.commit()
            Bot().send_message(id_user, 'Вы авторизованы')

        elif id_user in Data.is_auth_users_list:
            Bot().send_message(id_user, 'Вы авторизованы')

    def add_goods(self, text_message: str, id_user: int):


            if id_user in Data.is_auth_users_list:
                try:
                    text_message = text_message.split()
                    print(text_message)

                    link_goods = text_message[2]  ### [2] <--  element always must have link goods
                    print(link_goods)
                except IndexError:
                    Bot().send_message(id_user, 'Не правильная команда')

                try:
                    price_goods = Ali(link_goods).get_info()
                    print(price_goods)
                    price_goods = price_goods['price_product']
                    query_add = Goods(link=link_goods, user_id=id_user, price=price_goods)
                    session.add(query_add)
                    session.commit()
                    Bot().send_message(f'{id_user}', 'Товар добавлен')
                except Exception as error:
                    print(error)
                    Bot().send_message(id_user, 'Не удалось добавить товар!')

            elif id_user not in Data.is_auth_users_list:
                Bot().send_message(id_user, 'Вы не аутентифицированы')

    def display_all_goods(self, id_user):
        user_goods_all = session.query(Goods).filter_by(user_id=id_user)

        for goods in user_goods_all:
            link = goods.link
            price_goods = goods.price
            id_goods = goods.id
            try:
                data_dict = Ali(link).get_info()
                price_goods_in_ali = data_dict['price_product']

                if price_goods < price_goods_in_ali:
                    update_price = session.query(Goods).filter_by(id=id_goods).update({'price': price_goods_in_ali})
                    session.commit()

                    Bot().send_message(id_user,
                                     f'ЦЕНА УВЕЛИЧИЛОСЬ !!!\n'
                                     f' БЫЛО = {price_goods}, СТАЛО = {price_goods_in_ali}\n'
                                     f'id товара = {goods.id}\n'
                                     f'<a href="{data_dict["url"]}"><img src="{data_dict["link_photo"]}"\n')

                elif price_goods > price_goods_in_ali:
                    update_price = session.query(Goods).filter_by(id=id_goods).update({'price': price_goods_in_ali})
                    session.commit()

                    Bot().send_message(id_user,
                                     f'ЦЕНА УМЕНЬШИЛОСЬ !!!\n'
                                     f'ОБРАТИ ВНИМАНИЕ\n'
                                     f' БЫЛО = {price_goods}, СТАЛО = {price_goods_in_ali}\n'
                                     f'id товара = {goods.id}\n'
                                     f'{data_dict["url"]}\n')


                else:
                    Bot().send_message(id_user, f'''<b> id товара = {goods.id}</b>\n
                                                          <i>цена товара = {price_goods_in_ali}</i>\n
                                                          <a href="{data_dict['url']}">ссылка</a>\n''')
            except:
                Bot().send_message(id_user, f'С ОБЪЯВЛЕНИЕМ ЧТО ТО НЕ ТАК !!! ПРОВЕРЬТЕ ССЫЛКУ \n\n'
                                          f'{link}\n')

    def delete_goods(self, text_message, id_user):
        id_goods = text_message.split()[-1]
        id_goods = int(id_goods)
        try:
            query = session.query(Goods).filter_by(id=id_goods)
            print(list(query))
            good_data = list(query)
            user_id_goods = good_data[0].user_id

            if user_id_goods == id_user:
                query = session.query(Goods).filter_by(id=id_goods).delete()
                session.commit()
                Bot().send_message(id_user, "Товар удален")

            elif user_id_goods != id_user:
                Bot().send_message(id_user, "Вы не можете удалить чужой товар")
        except IndexError:
            Bot().send_message(id_user, "Увы такого товара не существует")













