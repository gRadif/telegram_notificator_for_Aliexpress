from DB.Tables import User, Goods, session
from DB.Manage import check_user_db

import telebot
from aliexpress import Ali
import config


tok = config.token
bot = telebot.TeleBot(tok, parse_mode=None)


### handler command 'START'
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую Вас!\n'
                                      'Мой функционал:\n'
                                      '- али = проверка что бот активен\n'
                                      '- покажи все = показывает все ваши товары в базе и проверяет их наличие на aliexpress\n'
                                      '- добавь товар [вместо скобок вставляем ссылку на товар] - добавить товар в базу\n'
                                      '- авторизоваться = добавляет Вас в базу пользователей (Без авторизации Вы не сможете пользоваться ботом) \n')

### handler command 'АЛИ'
@bot.message_handler(regexp='али')
def check_bot(message):
    bot.send_message(message.chat.id, 'Я здесь')


### handler command 'ПОКАЖИ ВСЕ'
@bot.message_handler(regexp='покажи все')
def show_all(message):
    id_user = message.chat.id
    # test_url = 'https://aliexpress.ru/item/4000809053108.html?spm=a2g2w.productlist.0.0.3be85568aXHQYS&sku_id=12000025091114231'
    goods_all = session.query(Goods).filter_by(user_id=id_user)

    for item in goods_all:
        link = item.link
        data_dict = Ali(link).get_info()
        bot.send_message(message.chat.id, f'id товара = {item.id}\n'
                                          f'цена товара = {data_dict["price_product"]}\n'
                                          f'{data_dict["name_product"]}\n'                                          
                                          f'{data_dict["url"]}\n')


### handler command 'ДОБАВЬ ТОВАР [ссылка на товар]'
@bot.message_handler(regexp='добавь товар')
def add_goods(message):
    id_user = message.chat.id
    check_bool = check_user_db(id_user)

    if check_bool is True:
        text_message = message.html_text.split()
        link_goods = text_message[2] ### [2] <--  element always must have link goods

        query_add = Goods(link=link_goods, user_id = id_user)
        session.add(query_add)
        session.commit()

        bot.send_message(message.chat.id, 'Добавил')

    elif check_bool is False:
        bot.send_message(message.chat.id, 'Вы не авторизованы')


### handler command 'АВТОРИЗОВАТЬСЯ '
@bot.message_handler(regexp='авторизоваться')
def bot_login(message):
    id_user = message.chat.id
    check_bool = check_user_db(id_user)
    name_user = message.chat.first_name

    if check_bool is False:
        reg_query = User(id = id_user, name=name_user)
        session.add(reg_query)
        session.commit()
        bot.send_message(message.chat.id, 'Вы авторизованы')

    elif check_bool is True:
        bot.send_message(message.chat.id, 'Пользователь с такими данными авторизован')



bot.polling()







# TODO add table Goods column 'price' for check price

# TODO :
def check_price_goods():
    pass

# TODO :
def delete_goods():
    pass


