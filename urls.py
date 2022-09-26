from datetime import date
from views import Index, Examples, Contacts, PageNotFound404


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [
    secret_front,
    other_front,
]

routes = {
    '/': Index(),
    '/examples/': Examples(),
    '/contacts/': Contacts(),
    'error_page': PageNotFound404(),
}
