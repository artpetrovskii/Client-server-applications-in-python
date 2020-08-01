from common.variables import ACTION, USER, ACCOUNT_NAME, PRESENCE, \
                             TIME, DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR
from common.utils import get_message, send_message
from errors import IncorrectDataReceived
from decos import log
import socket
import sys
import argparse
import json
import logging
import logs.config_server_log


loggers = logging.getLogger('server')

@log
def process_client_message(message):
    loggers.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

@log
def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser

def main():
    parser = create_argument_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        loggers.critical(f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
                         f'Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    loggers.info(f'Запущен сервер, порт для подключений: {listen_port}, адрес,'
                 f' с которого принимаются подключения: {listen_address}. '
                 f'Если адрес не указан, принимаются соединения с любых адресов.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        loggers.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_message(client)
            loggers.debug(f'Получено сообщение {message_from_client}')
            print(message_from_client)
            response = process_client_message(message_from_client)
            loggers.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            loggers.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            loggers.error(f'Не удалось декодировать Json строку, '
                          f'полученную от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataReceived:
            loggers.error(f'От клиента {client_address} приняты некорректные данные. '
                          f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
