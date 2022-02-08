from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import Subject


# абстрактный клиент
class User:
    def __init__(self, name):
        self.name = name


# физическое лицо
class Manager(User):
    def __init__(self, name):
        self.orders = []
        super().__init__(name)


# юридическое лицо
class Operator(User):
    def __init__(self, name):
        self.orders = []
        super().__init__(name)


class UserFactory:
    user_types = {
        'manager': Manager,
        'operator': Operator,
    }

    @classmethod
    def create(cls, u_type, name):
        return cls.user_types[u_type](name)


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

    def get_user(self, name):
        for user in self.users:
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

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
