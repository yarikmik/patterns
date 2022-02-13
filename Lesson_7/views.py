from my_framework.templator import render
from my_patterns.structur_patterns import UrlRoute, Debug
from my_patterns.creational_patterns import Engine, Logger, MapperRegistry
from my_patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer, CreateView, FileWriter
from my_patterns.architectural_patterns import UnitOfWork

logger = Logger('views', FileWriter())
site = Engine()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes_dec = {}


@UrlRoute(routes=routes_dec, url='/')
class Index:
    @Debug()
    def __call__(self, request):
        logger.log('основная страница')
        return '200 OK', render('index.html', current_path=request['context_data'].get('current_path', None),
                                date=request['context_data'].get('date', None))


@UrlRoute(routes=routes_dec, url='/contact/')
class Contact:
    @Debug()
    def __call__(self, request):
        logger.log('контакты')
        return '200 OK', render('contact.html', current_path=request['context_data'].get('current_path', None),
                                date=request['context_data'].get('date', None))


@UrlRoute(routes=routes_dec, url='/about/')
class About:
    @Debug()
    def __call__(self, request):
        logger.log('страница About')
        return '200 OK', render('about.html', current_path=request['context_data'].get('current_path', None),
                                date=request['context_data'].get('date', None))


@UrlRoute(routes=routes_dec, url='/orders/')
class CreateOrders(CreateView):
    queryset = site.orders
    template_name = 'orders.html'

    @Debug()
    def create_obj(self, data: dict):
        if data['order_name']:
            new_order = site.create_order(data['order_name'], data['description'])
            site.orders.append(new_order)


@UrlRoute(routes=routes_dec, url='/operators/')
class CreateOperators(CreateView):
    template_name = 'operators.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('User')
        return mapper.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['user_types'] = site.user_types
        return context

    @Debug()
    def create_obj(self, data: dict):
        if data['user_name']:
            new_user = site.create_user(data['user_type'], data['user_name'])
            site.users.append(new_user)
            new_user.mark_new()
            UnitOfWork.get_current().commit()


@UrlRoute(routes=routes_dec, url='/order_edit/')
class OrderEdit(CreateView):
    queryset = site.orders
    template_name = 'order_edit.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['service_types'] = site.service_types
        # context['user_types'] = site.user_types
        mapper = MapperRegistry.get_current_mapper('User')
        context['users'] = mapper.all()
        return context

    @Debug()
    def create_obj(self, data: dict):
        try:
            order = site.get_order_by_id(int(data['request_params']['id']))
        except KeyError:
            return '200 OK', 'Ошибка, нет такого заказа'

        if data['button'] == 'add service' and data['service_name'] != '':
            new_service = site.create_service(data['ServiceType'], data['service_name'], order)
            site.services.append(new_service)
        if data['button'] == 'add employee' and data['user_name'] != '':
            mapper = MapperRegistry.get_current_mapper('User')
            new_user = mapper.find_by_id(int(data['id']))
            site.users.append(new_user)

            order.observers.append(email_notifier)
            order.observers.append(sms_notifier)

            order.add_user(new_user)


@UrlRoute(routes=routes_dec, url='/copy-service/')
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


@UrlRoute(routes=routes_dec, url='/api/')
class UserApi:
    @Debug()
    def __call__(self, request):
        user = site.get_user(request['request_params']['name'])
        print(user)
        return '200 OK', BaseSerializer(user).save()
