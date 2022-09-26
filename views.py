from turbo_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html')


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')


class PageNotFound404:
    def __call__(self, request):
        return '404 not found', '404 Page not found'
