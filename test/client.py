from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
                             ACTION, TIME, USER, ACCOUNT_NAME, \
                             SENDER, PRESENCE, RESPONSE, ERROR, \
                             MESSAGE, MESSAGE_TEXT
from common.utils import get_message, send_message
from errors import MissingRequiredField, ServerError
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
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        loggers.info(f'Получено сообщение от пользователя '
                     f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        loggers.error(f'Получено некорректное сообщение с сервера: {message}')

@log
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        loggers.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    loggers.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict

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
    loggers.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise MissingRequiredField(RESPONSE)

@log
def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        loggers.critical(f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
                         f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        loggers.critical(f'Указан недопустимый режим работы {client_mode}, '
                         f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode

def main():
    server_address, server_port, client_mode = create_argument_parser()
    loggers.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
                 f'порт: {server_port}, режим работы: {client_mode}')
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_answer(get_message(transport))
        loggers.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        loggers.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        loggers.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except MissingRequiredField as missing_error:
        loggers.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        loggers.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                         f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    loggers.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    loggers.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
