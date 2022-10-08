from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect

from patterns.architectural_system import DomainObject
from patterns.behavioral import Subject


class User:
    def __init__(self, name):
        self.name = name


class Guest(User):
    pass


class Reader(User, DomainObject):
    def __init__(self, name):
        super().__init__(name)
        self.all_news = []


class Moderator(User):
    pass


class Admin(User):
    pass


class UserFactory:
    types = {
        'guest': Guest,
        'reader': Reader,
        'moderator': Moderator,
        'admin': Admin,
    }

    # Фабричный метод, порождающий паттерн
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# Прототип, порождающий паттерн
class NewsPrototype:
    def clone(self):
        return deepcopy(self)


class News(NewsPrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.all_news.append(self)
        self.readers = []
        super().__init__()

    def __getitem__(self, item):
        return self.readers[item]

    def add_reader(self, reader: Reader):
        self.readers.append(reader)
        reader.all_news.append(self)
        self.notify()


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
        self.guest = []
        self.readers = []
        self.moderators = []
        self.admins = []
        self.all_news = []
        self.news_copies = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
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

    def get_reader(self, name) -> Reader:
        for item in self.readers:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace('+', ' '), 'utf-8')
        value_decode_str = decodestring(value_b)
        return value_decode_str.decode('utf-8')


# # Синглтон, порождающий паттерн
# class SingletonByName(type):
#     def __init__(cls, name, bases, attrs, **kwargs):
#         super().__init__(name, bases, attrs)
#         cls.__instance = {}
#
#     def __call__(cls, *args, **kwargs):
#         if args:
#             name = args[0]
#         if kwargs:
#             name = kwargs['name']
#
#         if name in cls.__instance:
#             return cls.__instance[name]
#         else:
#             cls.__instance[name] = super().__call__(*args, **kwargs)
#             return cls.__instance[name]
#
#
# class Logger(metaclass=SingletonByName):
#     def __init__(self, name):
#         self.name = name
#
#     @staticmethod
#     def log(text):
#         print(f'[LOG] {text}')


class ReaderMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'reader'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            reader = Reader(name)
            reader.id = id
            result.append(reader)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Reader(*result)
        raise RecordNotFoundException(f'Record with ID={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('db/db_patterns.sqlite')


# Data Mapper, архитектурный системный паттерн
class MapperRegistry:
    mappers = {
        'reader': ReaderMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Reader):
            return ReaderMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
