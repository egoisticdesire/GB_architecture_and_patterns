from wsgiref.simple_server import make_server

from turbo_framework.framework import TurboFramework
from urls import routes, fronts

app = TurboFramework(routes, fronts)

with make_server('', 8080, app) as server:
    print(
        '[INFO] Server running on port 8080...\n\t'
        'http://127.0.0.1:8080/'
    )
    server.serve_forever()
