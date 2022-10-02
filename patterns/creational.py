from copy import deepcopy
from quopri import decodestring


class User:
    pass


class Moderator(User):
    pass


class Admin(User):
    pass


class UserFactory:
    user_types = {
        'moderator': Moderator,
        'admin': Admin,
    }

    # Фабричный метод, порождающий паттерн
    @classmethod
    def create(cls, type_):
        return cls.user_types[type_]()


# Прототип, порождающий паттерн
class NewsPrototype:
    def clone(self):
        return deepcopy(self)


class News(NewsPrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.all_news.append(self)


class GamesNews(News):
    pass


class HiTechNews(News):
    pass


class EconomicsNews(News):
    pass


class PoliticsNews(News):
    pass


class NewsFactory:
    types = {
        'games': GamesNews,
        'hi-tech': HiTechNews,
        'economics': EconomicsNews,
        'politics': PoliticsNews,
    }

    # Фабричный метод, порождающий паттерн
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    id_auto_increment = 1

    def __init__(self, name, category):
        self.id = Category.id_auto_increment
        Category.id_auto_increment += 1
        self.name = name
        self.category = category
        self.all_news = []

    def news_count(self):
        result = len(self.all_news)
        if self.category:
            result += self.category.news_count()
        return result


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.moderators = []
        self.admins = []
        self.all_news = []
        self.news_copies = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print(f'item = {item.id}')
            if item.id == id:
                return item
        raise Exception(f'No category with ID = {id}')

    @staticmethod
    def create_news(type_, name, category):
        return NewsFactory.create(type_, name, category)

    def get_news(self, name):
        for item in self.all_news:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace('+', ' '), 'utf-8')
        value_decode_str = decodestring(value_b)
        return value_decode_str.decode('utf-8')


# Синглтон, порождающий паттерн
class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print(f'[LOG] {text}')
