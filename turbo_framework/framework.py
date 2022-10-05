from quopri import decodestring

from log.log_config import LOGGER
from turbo_framework.request_handler import GetRequests, PostRequests
from views import PageNotFound404


class TurboFramework:
    def __init__(self, routes_obj, fronts_obj):
        # page controller
        self.routes = routes_obj
        # front controller
        self.fronts = fronts_obj

    def __call__(self, environ, start_response):
        # Получение адреса, по которому выполнен переход
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = TurboFramework.decode_value(request_params)
            LOGGER.info(f'"GET" parameters received: {request["request_params"]}')

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = TurboFramework.decode_value(data)
            LOGGER.info(f'"POST" request received:{request["data"]}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}

        for key, val in data.items():
            value = bytes(val.replace('%', '=').replace('+', ' '), 'utf-8')
            value_decode_str = decodestring(value).decode('utf-8')
            new_data[key] = value_decode_str

        return new_data


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApp(TurboFramework):
    def __init__(self, routes_obj, fronts_obj):
        self.app = TurboFramework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, environ, start_response):
        LOGGER.debug(f'{environ=}')
        return self.app(environ, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(TurboFramework):
    def __init__(self, routes_obj, fronts_obj):
        self.app = TurboFramework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
