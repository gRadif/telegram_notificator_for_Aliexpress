import re


def check_command(text_message):
    command_dict = {'/start': '/start',
                    '[аА]ли': 'али',
                    '[аА]вторизоваться': 'авторизоваться',
                    '[дД]обавь товар': 'добавь товар',
                    '[пП]окажи все': 'покажи все'}
    for command, value in command_dict.items():
        pattern = f'{command}'
        result = re.match(pattern=pattern, string=text_message)
        if result is not None:
            return value



