from MAIN_HANDLER import DollarNotification, \
    AliexpressNotification, \
    Handler, \
    Commands, \
    Data



Data.is_auth_users_list = Handler().is_auth_users()

while True:

    DollarNotification().control_dollar()

    AliexpressNotification().control_aliexpress()


    # range(600) is counter time in sec
    for i in range(600):
        status_chat_dict = Handler().chat_listen()

        if status_chat_dict['message'] is None:
            continue

        command = status_chat_dict['command']
        id_user = status_chat_dict['id_user']

        if command == '/start':
            Commands().command_start(id_user=id_user)

        elif command == 'али':
            Commands().hi_ali(id_user=id_user)

        elif command == 'авторизоваться':
            Commands().autorization_in_bot(user_name=status_chat_dict['user_name'], id_user=id_user)

        elif command == 'добавь товар':
            Commands().add_goods(status_chat_dict['message'], id_user=id_user)

        elif command == 'покажи все':
            Commands().display_all_goods(id_user=id_user)

        elif command == 'удалить товар':
            Commands().delete_goods(status_chat_dict['message'], id_user=id_user)

        elif command == 'доллар':
            DollarNotification().current_dollar_cost(id_user=id_user)


