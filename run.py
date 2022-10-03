from wsgiref.simple_server import make_server

from turbo_framework.framework import DebugApp, FakeApplication, TurboFramework
from urls import fronts
from views import routes

app = DebugApp(routes, fronts)

with make_server('', 8080, app) as server:
    print(
        '[INFO] Server running on port 8080...\n\t'
        'http://127.0.0.1:8080/'
    )
    server.serve_forever()
