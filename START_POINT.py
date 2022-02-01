from DB.Tables import User, Goods, session
from DB.Manage import check_user_db, get_goods_all_data_all_users
from Handlers import Commands
from aliexpress import Ali
import config
from Bot.Telebot import Bot
import time


bot = Bot()



while True:
    # goods_all_data = get_goods_all_data_all_users()
    # for goods in goods_all_data:
    #     id_user = goods['user_id']
    #     id_goods_in_db = goods['id']
    #     data_goods_in_ali = Ali(goods['link']).get_info()
    #     url_goods = data_goods_in_ali['url']
    #     price_in_ali = data_goods_in_ali['price_product']
    #     price_in_db = goods['price']
    #
    #     if price_in_ali != price_in_db:
    #         update_price = session.query(Goods).filter_by(id=id_goods_in_db).update({'price': price_in_ali})
    #         session.commit()
    #
    #         bot.send_message(id_user, f'ЦЕНА ИЗМЕНИЛАСЬ БЫЛО = {price_in_db}, СТАЛО = {price_in_ali}\n'
    #                                   f'id товара = {id_goods_in_db}\n'
    #                                   f'{url_goods}\n')


    # range(600) is counter time in sec
    for i in range(600):

        time.sleep(1)
        message = bot.listen_chat()

        # if in chat message None return of the start cycle
        if message is None:
            continue

        id_user = message[0]['message']['chat']['id']
        text_message = message[0]['message']['text']
        status_user = check_user_db(id_user)
        message_command = commands.check_command(text_message)

        if message_command == '/start':
            bot.send_message(f'{id_user}', 'Приветствую Вас!\n'
                                      'Мой функционал:\n'
                                      '- али = проверка что бот активен\n'
                                      '- покажи все = показывает все ваши товары в базе и проверяет их наличие на aliexpress\n'
                                      '- добавь товар [вместо скобок вставляем ссылку на товар] - добавить товар в базу\n'
                                      '- авторизоваться = добавляет Вас в базу пользователей (Без авторизации '
                                      'Вы не сможете пользоваться ботом) \n')

        elif message_command == 'али':
            bot.send_message(f'{id_user}', 'я здесь')

        elif message_command == 'авторизоваться':

            if config.access_authentication  is False:
                bot.send_message(id_user, 'Разработчик закрыл возможность авторизации')

            elif status_user == 'unauthenticated':
                name_user = message[0]['message']['chat']['first_name']

                reg_query = User(id=id_user, name=name_user)
                session.add(reg_query)
                session.commit()
                bot.send_message(id_user, 'Вы авторизованы')

            elif status_user == 'is_authenticated':
                bot.send_message(id_user, 'Пользователь с такими данными авторизован')

        elif message_command == 'добавь товар':

            if status_user == 'is_authenticated':

                text_message = text_message.split()
                print(text_message)

                link_goods = text_message[2]  ### [2] <--  element always must have link goods
                print(link_goods)

                try:
                    price_goods = Ali(link_goods).get_info()
                    price_goods = price_goods['price_product']
                    query_add = Goods(link=link_goods, user_id=id_user, price=price_goods)
                    session.add(query_add)
                    session.commit()
                    bot.send_message(f'{id_user}', 'Товар добавлен')
                except:
                    bot.send_message(id_user, 'Не удалось добавить товар!')

            elif status_user == 'unauthenticated':
                bot.send_message(id_user, 'Вы не аутентифицированы')

        elif message_command == 'покажи все':

            user_goods_all = session.query(Goods).filter_by(user_id=id_user)

            for goods in user_goods_all:
                link = goods.link
                price_goods = goods.price
                id_goods = goods.id

                data_dict = Ali(link).get_info()
                price_goods_in_ali = data_dict['price_product']

                if price_goods != price_goods_in_ali:
                    update_price = session.query(Goods).filter_by(id=id_goods).update({'price': price_goods_in_ali})
                    session.commit()

                    bot.send_message(id_user, f'ЦЕНА ИЗМЕНИЛАСЬ БЫЛО = {price_goods}, СТАЛО = {price_goods_in_ali}\n'
                                              f'id товара = {goods.id}\n'
                                              f'{data_dict["url"]}\n')

                else:
                    bot.send_message(id_user, f'id товара = {goods.id}\n'
                                                      f'цена товара = {price_goods_in_ali}\n'
                                                      f'{data_dict["name_product"]}\n'
                                                      f'{data_dict["url"]}\n')
