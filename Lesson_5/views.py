from my_framework.templator import render
from my_patterns.structur_patterns import UrlRoute, Debug
from my_patterns.creational_patterns import Engine, Logger

logger = Logger('views')
site = Engine()

routes_dec = {}


@UrlRoute(routes=routes_dec, url='/')
class Index:
    @Debug()
    def __call__(self, request):
        logger.log('основная страница')
        return '200 OK', render('index.html', current_path=request.get('path_info', None),
                                date=request.get('date', None))


@UrlRoute(routes=routes_dec, url='/contact/')
class Contact:
    @Debug()
    def __call__(self, request):
        logger.log('контакты')
        return '200 OK', render('contact.html', current_path=request.get('path_info', None),
                                date=request.get('date', None))


@UrlRoute(routes=routes_dec, url='/about/')
class About:
    @Debug()
    def __call__(self, request):
        logger.log('страница About')
        return '200 OK', render('about.html', current_path=request.get('path_info', None),
                                date=request.get('date', None))


@UrlRoute(routes=routes_dec, url='/orders/')
class CreateOrders:
    @Debug()
    def __call__(self, request):
        logger.log('страница создания заказов')
        if request['method'] == 'POST':
            data = request['data']
            # создаем новый заказ
            if data['order_name']:
                new_order = site.create_order(data['order_name'], data['description'])
                site.orders.append(new_order)  # добавляем в список заказов

                #  в этом месте не нашел как правильно передать параметры в рендер
                #  как контекст в джанге, поэтому ретерн дублируется так полно
                return '200 OK', render('orders.html', current_path=request.get('path_info', None),
                                        date=request.get('date', None),
                                        object_list=site.orders, )

        return '200 OK', render('orders.html', current_path=request.get('path_info', None),
                                date=request.get('date', None),
                                object_list=site.orders, )


class OrderEdit:
    @Debug()
    def __call__(self, request):
        logger.log('редактирование заказов')
        try:
            order = site.get_order_by_id(int(request['request_params']['id']))
        except KeyError:
            return '200 OK', 'Ошибка, нет такого заказа'

        if request['method'] == 'POST':
            data = request['data']
            if data['service_name']:
                new_service = site.create_service(data['ServiceType'], data['service_name'], order)
                site.services.append(new_service)
                return '200 OK', render('order_edit.html', services_list=order.services,
                                        services_type_list=site.service_types,
                                        name=order.name, id=order.id, description=order.description)

        return '200 OK', render('order_edit.html', services_list=order.services,
                                services_type_list=site.service_types,
                                name=order.name, id=order.id, description=order.description)


class CopyService:
    @Debug()
    def __call__(self, request):
        request_params = request['request_params']
        order = site.get_order_by_id(int(request['request_params']['id']))

        try:
            name = request_params['name']

            old_service = site.get_service(name)
            if old_service:
                new_service = old_service.clone()
                new_service.name = f'copy_{name}'
                site.services.append(new_service)

                return '200 OK', render('order_edit.html', services_list=order.services,
                                        services_type_list=site.service_types,
                                        name=order.name, id=order.id, description=order.description)
        except KeyError:
            return '200 OK', 'Ошибка, нет такого сервиса'
