import sys
import logging
import inspect
import traceback
import logs.config_client_log
import logs.config_server_log

if sys.argv[0].find('client') == -1:
    loggers = logging.getLogger('server')
else:
    loggers = logging.getLogger('client')

def log(logging_function):
    def logging_saver(*args, **kwargs):
        ret = logging_function(*args, **kwargs)
        loggers.debug(f'Вызов функции {logging_function.__name__} c параметрами {args}, {kwargs}. '
                      f'Вызов из модуля {logging_function.__module__}. Вызов из'
                      f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                      f'Вызов из функции {inspect.stack()[1][3]}')
        return ret
    return logging_saver

class Log:
    def __call__(self, logging_function):
        def logging_saver(*args, **kwargs):
            ret = logging_function(*args, **kwargs)
            loggers.debug(f'Вызов функции {logging_function.__name__} c параметрами {args}, {kwargs}. '
                          f'Вызов из модуля {logging_function.__module__}. Вызов из'
                          f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                          f'Вызов из функции {inspect.stack()[1][3]}')
            return ret
        return logging_saver
