from common.variables import LEVEL_LOGGING
import sys
import os
import logging
sys.path.append('../')

formatting_client = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

file_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_path, 'client.log')

handling_stream = logging.StreamHandler(sys.stderr)
handling_stream.setLevel(logging.ERROR)
handling_stream.setFormatter(formatting_client)

file_logs = logging.FileHandler(file_path, encoding='utf8')
file_logs.setFormatter(formatting_client)

loggers = logging.getLogger('client')
loggers.setLevel(LEVEL_LOGGING)
loggers.addHandler(file_logs)
loggers.addHandler(handling_stream)

if __name__ == '__main__':
    loggers.error('Ошибка')
    loggers.critical('Критическая ошибка')
    loggers.info('Сообщение с информацией')
    loggers.debug('Информация по отладке')
