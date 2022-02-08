from jsonpickle import dumps, loads
from my_framework.templator import render


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print(f'SMS-> К заказу {subject.name}(id={subject.id}) '
              f'прикреплен новый работник: {subject.users[-1].name}')


class EmailNotifier(Observer):

    def update(self, subject):
        print(f'EMAIL-> К заказу {subject.name}(id={subject.id}) '
              f'прикреплен новый работник: {subject.users[-1].name}')


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)