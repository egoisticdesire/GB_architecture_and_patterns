class TurboFramework:
    def __init__(self, routes_obj, fronts_obj):
        # page controller
        self.routes = routes_obj
        # front controller
        self.fronts = fronts_obj

    def __call__(self, environ, start_response, *args, **kwargs):
        # Получение адреса, по которому выполнен переход
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.routes['error_page']

        requests = {}

        for front in self.fronts:
            front(requests)

        code, body = view(requests)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
