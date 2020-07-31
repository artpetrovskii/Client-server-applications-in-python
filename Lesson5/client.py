from errors import RequiredFieldMissingError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
                            RESPONSE, DEFAULT_PORT, ERROR, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
import sys
import json
import socket
import time
import argparse
import logging
import logs.config_client_log


logging_client = logging.getLogger('client')

def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logging_client.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def process_answer(message):
    logging_client.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise RequiredFieldMissingError(RESPONSE)


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
        logging_client.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    logging_client.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_answer(get_message(transport))
        logging_client.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        logging_client.error('Не удалось декодировать полученную Json строку.')
    except RequiredFieldMissingError as missing_error:
        logging_client.error(f'В ответе сервера отсутствует необходимое поле '
                             f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        logging_client.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                                f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
