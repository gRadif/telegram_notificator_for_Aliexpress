import os


access_authentication = os.getenv("ACCESS", 'False')
token = os.getenv("token", '')
id_dev = os.getenv('id_dev', '')

try:
    from config_local import *
except ImportError:
    pass
#
# from DB.Tables import User, Goods, session
# from Bot.Telebot import Bot
# from BANK import AkBarsBank
# from aliexpress import Ali
# import time
# import config
# import re
#
#
# class DollarNotification:
#     def control_dollar(self):
#         dollar_cost = AkBarsBank.dollar_price()
#
#         if type(dollar_cost) is str:
#             bot.send_message(id_user, f'{dollar_cost}')
#
#         elif dollar_cost > 77.54:
#             bot.send_message(id_user, f' Доллар вырос ---> {dollar_cost} рублей')
#
#     def current_dollar_cost(self):
#         dollar_cost = AkBarsBank.dollar_price()
#
#         if type(dollar_cost) is str:
#             bot.send_message(id_user, f'{dollar_cost}')
#         else:
#             bot.send_message(id_user, f' Доллар ---> {dollar_cost} рублей')
#
#
# class AliexpressNotification:
#     def control_aliexpress(self):
#         goods_all_data = get_goods_all_data_all_users()
#         for goods in goods_all_data:
#             id_user = goods['user_id']
#             id_goods_in_db = goods['id']
#             data_goods_in_ali = Ali(goods['link']).get_info()
#             url_goods = data_goods_in_ali['url']
#             price_in_ali = data_goods_in_ali['price_product']
#             price_in_db = goods['price']
#
#             if price_in_ali != price_in_db:
#                 update_price = session.query(Goods).filter_by(id=id_goods_in_db).update({'price': price_in_ali})
#                 session.commit()
#
#                 Bot().send_message(id_user, f'ЦЕНА НА ТОВАР ИЗМЕНИЛАСЬ!!!\n'
#                                             f' БЫЛО = {price_in_db}, СТАЛО = {price_in_ali}\n'
#                                             f'id товара = {id_goods_in_db}\n'
#                                             f'{url_goods}\n')
#
#
# class Handler:
#     def chat_listen(self) -> Dict:
#         time.sleep(1)
#         message = Bot().listen_chat()
#         status_chat_dict = {"message": '',
#                             "id_user": '',
#                             'status_user': '',
#                             'command': ''}
#
#         # if in chat message None, return of the start cycle
#         if message is None:
#             status_chat_dict['message'] == None
#             return status_chat_dict
#
#         try:
#             if message[0].get('edited_message') is not None:
#                 status_chat_dict['id_user'] = message[0]['edited_message']['chat']['id']
#
#             else:
#                 status_chat_dict['id_user'] = message[0]['message']['chat']['id']
#         except:
#             Bot().send_message(id_dev, 'Ошибка в json при прослушивании чата ')
#
#         # check if sended gif or photo and video, them bot don't work
#         try:
#             text_message = message[0]['message']['text']
#         except KeyError:
#             return status_chat_dict['message'] == None
#
#         status_chat_dict['status_user'] = check_user_db(status_chat_dict['id_user'])
#         status_chat_dict['command'] = self.check_command(text_message)
#
#         return status_chat_dict
#
#     def check_user_db(self, id_user):
#         query = session.query(User).filter_by(id=id_user)
#         query = list(query)
#
#         if query == []:
#             return 'unauthenticated'
#
#         elif query != []:
#             return 'is_authenticated'
#
#     def check_command(self, text_message):
#         command_dict = {'/start': '/start',
#                         '[аА]ли': 'али',
#                         '[аА]вторизоваться': 'авторизоваться',
#                         '[дД]обавь товар': 'добавь товар',
#                         '[пП]окажи все': 'покажи все'}
#         for command, value in command_dict.items():
#             pattern = f'{command}'
#             result = re.match(pattern=pattern, string=text_message)
#             if result is not None:
#                 return value
#
#
# class Commands:
#     pass
#
#
# def get_goods_all_data_all_users():
#     goods_all_data_list = []
#     goods_all = session.query(Goods)
#     for goods in goods_all:
#         temp_dict = {}
#         temp_dict['id'] = goods.id
#         temp_dict['link'] = goods.link
#         temp_dict['price'] = goods.price
#         temp_dict['user_id'] = goods.user_id
#
#         goods_all_data_list.append(temp_dict)
#
#     return goods_all_data_list
#
