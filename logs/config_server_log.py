from common.variables import LEVEL_LOGGING
import sys
import os
import logging.handlers
sys.path.append('../')

formatting_server = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

file_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(file_path, 'server.log')

handling_stream = logging.StreamHandler(sys.stderr)
handling_stream.setFormatter(formatting_server)
handling_stream.setLevel(logging.ERROR)
file_logs = logging.handlers.TimedRotatingFileHandler(file_path, encoding='utf8', interval=1, when='D')
file_logs.setFormatter(formatting_server)

loggers = logging.getLogger('server')
loggers.addHandler(handling_stream)
loggers.addHandler(file_logs)
loggers.setLevel(LEVEL_LOGGING)

if __name__ == '__main__':
    loggers.critical('Критическая ошибка')
    loggers.error('Ошибка')
    loggers.debug('Информация по отладке')
    loggers.info('Сообщение с информацией')
