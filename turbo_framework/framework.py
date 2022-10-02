from quopri import decodestring

from turbo_framework.request_handler import GetRequests, PostRequests


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
            print(f'[INFO] "GET" parameters received: {request["request_params"]}')

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = TurboFramework.decode_value(data)
            print(f'[INFO] "POST" request received:{request["data"]}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.routes['error-page']

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
