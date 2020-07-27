from common.variables import LEVEL_LOGGING
import sys
import os
import logging
sys.path.append('../')

formatting_client = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

file_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_path, 'client.log')

handling_stream = logging.StreamHandler(sys.stderr)
handling_stream.setFormatter(formatting_client)
handling_stream.setLevel(logging.ERROR)
file_logs = logging.FileHandler(file_path, encoding='utf8')
file_logs.setFormatter(formatting_client)

loggers = logging.getLogger('client')
loggers.addHandler(handling_stream)
loggers.addHandler(file_logs)
loggers.setLevel(LEVEL_LOGGING)

if __name__ == '__main__':
    loggers.critical('Критическая ошибка')
    loggers.error('Ошибка')
    loggers.debug('Информация по отладке')
    loggers.info('Сообщение с информацией')
