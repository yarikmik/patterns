from copy import deepcopy
from quopri import decodestring


# абстрактный клиент
class Client:
    pass


# физическое лицо
class Entity(Client):
    pass


# юридическое лицо
class Individual(Client):
    pass


class ClientFactory:
    client_types = {
        'entity': Entity,
        'individual': Individual,
    }

    @classmethod
    def create(cls, c_type):
        return cls.client_types[c_type]()


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
class Order(Prototype):
    auto_id = 0

    def __init__(self, name, description, order):
        self.name = name
        self.description = description
        self.order = order
        self.services = []
        self.id = Order.auto_id
        Order.auto_id += 1

    def services_count(self):
        result = len(self.services)
        # if self.services:
        #     result += self.services.services_count()
        return result


class Engine:
    def __init__(self):
        self.service_types = ServiceFactory.service_types
        self.entity = []
        self.individual = []
        self.services = []
        self.orders = []

    @staticmethod
    def create_client(c_type):
        return ClientFactory.create(c_type)

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
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')
