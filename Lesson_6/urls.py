from datetime import date
from views import Index, About, Contact, CreateOrders, OrderEdit, CopyService, routes_dec


# front controller
def secret_front(request):
    request['date'] = date.today().strftime("%B %d, %Y")


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    # '/': Index(),
    # '/about/': About(),
    # '/contact/': Contact(),
    # '/orders/': CreateOrders(),
    '/order_edit/': OrderEdit(),
    '/copy-service/': CopyService(),
}

routes.update(routes_dec)
