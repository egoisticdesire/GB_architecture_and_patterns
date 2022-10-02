from datetime import date
from views import (Index, Examples, Contacts, PageNotFound404, NewsList, CategoriesList, CreateNews, CreateCategory,
                   CopyNews)


# front controller
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
    '/examples/news/': NewsList(),
    '/examples/news/create-news/': CreateNews(),
    '/examples/news/copy-news/': CopyNews(),
    '/examples/categories/': CategoriesList(),
    '/examples/categories/create-category/': CreateCategory(),
    '/contacts/': Contacts(),
    'error-page': PageNotFound404(),
}
