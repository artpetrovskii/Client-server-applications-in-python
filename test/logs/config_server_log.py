from common.variables import LEVEL_LOGGING
import sys
import os
import logging.handlers
sys.path.append('../')

formatting_server = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

file_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_path, 'server.log')

handling_stream = logging.StreamHandler(sys.stderr)
handling_stream.setLevel(logging.ERROR)
handling_stream.setFormatter(formatting_server)

file_logs = logging.handlers.TimedRotatingFileHandler(file_path, encoding='utf8', interval=1, when='D')
file_logs.setFormatter(formatting_server)

loggers = logging.getLogger('server')
loggers.setLevel(LEVEL_LOGGING)
loggers.addHandler(file_logs)
loggers.addHandler(handling_stream)

if __name__ == '__main__':
    loggers.error('Ошибка')
    loggers.critical('Критическая ошибка')
    loggers.info('Сообщение с информацией')
    loggers.debug('Информация по отладке')
