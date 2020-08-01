from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, \
                             DEFAULT_IP_ADDRESS, DEFAULT_PORT, ERROR, PRESENCE
from common.utils import get_message, send_message
from errors import MissingRequiredField
from decos import log
import sys
import json
import socket
import time
import argparse
import logging
import logs.config_client_log


loggers = logging.getLogger('client')

@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    loggers.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out

@log
def process_answer(message):
    loggers.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise MissingRequiredField(RESPONSE)

@log
def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser

def main():
    parser = create_argument_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    if not 1023 < server_port < 65536:
        loggers.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    loggers.info(f'Запущен клиент с парамертами: адрес сервера: '
                 f'{server_address}, порт: {server_port}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_answer(get_message(transport))
        loggers.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        loggers.error('Не удалось декодировать полученную Json строку.')
    except MissingRequiredField as missing_error:
        loggers.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        loggers.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                         f'конечный компьютер отверг запрос на подключение.')

if __name__ == '__main__':
    main()
