# -*- coding: utf-8 -*-
import os
import logging.handlers
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import yapdi
from handler import *

# '' для отключения логирования
LOG_FILE = 'var/log/tornadoCS{}.log'

# INFO (все статусы), WARNING (>=404), ERROR (>=500)
LOG_LEVEL = 'INFO'


def API():
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"(/v3/(\w+)/(\w+)/)", ApiV2Handler),
        (r"(/v3/(\w+)/(\w+))", InvalidRequestHandler)
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


COMMANDS = {'API': API}


def _setup_logger(port):
    # настраиваем логирование в файл
    log_path = LOG_FILE.format(port)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if log_path:
        try:
            os.makedirs(os.path.split(log_path)[0])
        except OSError:
            pass
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_path, mode='a+',  # имя файла
            maxBytes=10000000,  # максимально байт в файле
            backupCount=2)  # максимум файлов
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s\t%(levelname)-8s %(message)s',
                              datefmt='%d-%m-%Y %H:%M:%S'))
        logging.getLogger('').setLevel(logging.NOTSET)
        logging.getLogger('').addHandler(file_handler)
        # блокируемый файл для проверки активности сервера

if __name__ == "__main__":
    # Обработка ввода с клавиатуры
    if len(sys.argv) == 3:
        name, command, PORT = sys.argv
        _setup_logger(PORT)
        PID_FNAME = (os.path.split(os.path.abspath(__file__))[0]) + '/var/log' \
                    + (os.path.abspath(__file__).replace('/', '_')) + PORT + '.pid'

        if command in COMMANDS.keys() and PORT.isdigit():
            COMMANDS[command]()
    else:
        print 'Error: invalid command'
        print 'Usage: python tornading.py {%s}. PORT' % '|'.join(COMMANDS)

