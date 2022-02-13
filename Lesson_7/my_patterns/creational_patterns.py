from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import Subject
from sqlite3 import connect
from .architectural_patterns import DomainObject


# абстрактный клиент
class User:
    def __init__(self, name, u_type):
        self.name = name
        self.type = u_type


# физическое лицо
class Manager(User, DomainObject):
    def __init__(self, name, u_type):
        self.orders = []
        super().__init__(name, u_type)


# юридическое лицо
class Operator(User, DomainObject):
    def __init__(self, name, u_type):
        self.orders = []
        super().__init__(name, u_type)


class UserFactory:
    user_types = {
        'manager': Manager,
        'operator': Operator,
    }

    @classmethod
    def create(cls, u_type, name):
        return cls.user_types[u_type](name, u_type)


class Prototype:
    def clone(self):
        return deepcopy(self)


class Service(Prototype):
    def __init__(self, s_type, name, order):
        self.type = s_type
        self.name = name
        self.order = order
        self.order.services.append(self)


class InternetService(Service):
    pass


class MobileService(Service):
    pass


class TVService(Service):
    pass


class ServiceFactory:
    service_types = {
        'internet': InternetService,
        'mobile': MobileService,
        'tv': TVService,
    }

    @classmethod
    def create(cls, s_type, name, order):
        return cls.service_types[s_type](s_type, name, order)


# заказ
class Order(Prototype, Subject):
    auto_id = 0

    def __init__(self, name, description, order):
        # добавил типы, что бы к ним можно было обращатся через заказ в order_edit
        # self.service_types = ServiceFactory.service_types
        # self.user_types = UserFactory.user_types

        self.name = name
        self.description = description
        self.order = order
        self.services = []
        self.users = []
        self.id = Order.auto_id
        Order.auto_id += 1
        super().__init__()

    # def __getitem__(self, item):
    #     return self.users[item]

    def add_user(self, user):
        self.users.append(user)
        user.orders.append(self)
        self.notify()

    def services_count(self):
        result = len(self.services)
        # if self.services:
        #     result += self.services.services_count()
        return result


class Engine:
    def __init__(self):
        self.service_types = ServiceFactory.service_types
        self.user_types = UserFactory.user_types
        self.entity = []
        self.individual = []
        self.services = []
        self.orders = []
        self.users = []

    @staticmethod
    def create_user(u_type, name):
        return UserFactory.create(u_type, name)

    @staticmethod
    def create_service(service_type, name, order):
        return ServiceFactory.create(service_type, name, order)

    @staticmethod
    def create_order(name, description, order=None):
        return Order(name, description, order)

    def get_order_by_id(self, id):
        for item in self.orders:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет заказа с id = {id}')

    def get_service(self, name):
        for service in self.services:
            if service.name == name:
                return service
        return None

    @staticmethod
    def get_user(name):
        mapper = MapperRegistry.get_current_mapper('User')
        users = mapper.all()
        for user in users:
            if user.name == name:
                return user

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Logger(metaclass=Singleton):

    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class UserMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'users'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, type, orders = item
            user = User(name, type)
            user.id = id
            user.orders = orders
            result.append(user)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return User(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, type) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.type,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id,))
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


connection = connect('database.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'User': UserMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, User):
            return UserMapper(connection)

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
