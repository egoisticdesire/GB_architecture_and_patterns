from log.log_config import LOGGER
from patterns.architectural_system import UnitOfWork
from patterns.behavioral import BaseSerializer, CreateView, EmailNotifier, ListView, SmsNotifier
from patterns.creational import Engine, MapperRegistry
from patterns.structural import Debug, Router
from turbo_framework.templator import render

site = Engine()
sms_notifier = SmsNotifier()
email_notifier = EmailNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
routes = {}


@Router(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render(template_name='index.html')


@Router(routes=routes, url='/examples/')
class Examples:
    @Debug(name='Examples')
    def __call__(self, request):
        return '200 OK', render(
            template_name='examples.html',
            objects_list=site.categories,
        )


@Router(routes=routes, url='/examples/news/')
class NewsList:
    @Debug(name='NewsList')
    def __call__(self, request):
        LOGGER.info('List of news')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render(
                template_name='news.html',
                objects_list=category.all_news,
                name=category.name,
                id=category.id,
            )
        except KeyError:
            return '200 OK', 'No news have been added yet'


@Router(routes=routes, url='/examples/categories/')
class CategoriesList:
    @Debug(name='CategoriesList')
    def __call__(self, request):
        LOGGER.info('List of categories')
        return '200 OK', render(
            template_name='categories.html',
            objects_list=site.categories,
        )


@Router(routes=routes, url='/examples/news/create-news/')
class CreateNews:
    category_id = -1

    @Debug(name='CreateNews')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                news = site.create_news('games', name, category)

                news.observers.append(sms_notifier)
                news.observers.append(email_notifier)

                site.all_news.append(news)

            return '200 OK', render(
                template_name='news.html',
                objects_list=category.all_news,
                name=category.name,
                id=category.id,
            )
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render(
                    template_name='create-news.html',
                    name=category.name,
                    id=category.id,
                )
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@Router(routes=routes, url='/examples/categories/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render(
                template_name='examples.html',
                objects_list=site.categories,
            )
        else:
            return '200 OK', render(
                template_name='create-category.html',
                categories=site.categories,
            )


@Router(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render(template_name='contacts.html')


class PageNotFound404:
    @Debug(name='PageNotFound404')
    def __call__(self, request):
        return '404 not found', '404 Page not found'


@Router(routes=routes, url='/examples/news/copy-news/')
class CopyNews:
    @Debug(name='CopyNews')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_news = site.get_news(name)

            if old_news:
                new_name = f'copy {name}'

                new_news = old_news.clone()
                new_news.name = new_name

                site.news_copies.append(new_news)

            return '200 OK', render(
                template_name='copy-data.html',
                objects_list=site.news_copies,
            )
        except KeyError:
            return '200 OK', render(
                template_name='copy-data.html',
                objects_list=site.news_copies,
            )


@Router(routes=routes, url='/readers/')
class ReadersListView(ListView):
    template_name = 'readers.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('reader')
        return mapper.all()


@Router(routes=routes, url='/readers/create-reader/')
class ReaderCreateView(CreateView):
    template_name = 'create-reader.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('reader', name)
        site.readers.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@Router(routes=routes, url='/readers/add-reader/')
class AddReaderCreateView(CreateView):
    template_name = 'add-reader.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['all_news'] = site.all_news
        context['readers'] = site.readers
        return context

    def create_obj(self, data: dict):
        news_name = data['news_name']
        news_name = site.decode_value(news_name)
        news = site.get_news(news_name)

        reader_name = data['reader_name']
        reader_name = site.decode_value(reader_name)
        reader = site.get_reader(reader_name)

        news.add_reader(reader)


@Router(routes=routes, url='/api/')
class NewsApi:
    @Debug(name='NewsApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.all_news).save()
