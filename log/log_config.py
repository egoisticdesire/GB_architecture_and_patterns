import logging
import sys
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_file.log')
LOGGER = logging.getLogger('TurboFramework')
FORMATTER = logging.Formatter(
    '{asctime} :: {levelname:8s} :: {name} :: {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M'
)

FILE_HANDLER = logging.FileHandler(PATH, encoding='utf-8')
FILE_HANDLER.setFormatter(FORMATTER)

STREAM_HANDLER = logging.StreamHandler(sys.stdout)
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
    LOGGER.warning('Предупреждение')
    LOGGER.error('Ошибка')
    LOGGER.critical('Критическая ошибка')
