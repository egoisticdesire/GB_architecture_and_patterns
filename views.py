from turbo_framework.templator import render
from patterns.creational import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render(template_name='index.html')


class Examples:
    def __call__(self, request):
        return '200 OK', render(
            template_name='examples.html',
            objects_list=site.categories,
        )


class NewsList:
    def __call__(self, request):
        logger.log('List of news')
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


class CategoriesList:
    def __call__(self, request):
        logger.log('List of categories')
        return '200 OK', render(
            template_name='categories.html',
            objects_list=site.categories,
        )


class CreateNews:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                news = site.create_news('games', name, category)
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


class CreateCategory:
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


class Contacts:
    def __call__(self, request):
        return '200 OK', render(template_name='contacts.html')


class PageNotFound404:
    def __call__(self, request):
        return '404 not found', '404 Page not found'


class CopyNews:
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
