from quopri import decodestring
# from request import get_request_params, post_request_params
from .request import post_request_params, get_request_params


def decoding_data(data):
    new_data = {}
    for key, value in data.items():
        val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val).decode('UTF-8')
        new_data[key] = val_decode_str
    return new_data


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # получаем метод запроса
        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = post_request_params(environ)
            request['data'] = decoding_data(data)
            print(f'Получен POST: {decoding_data(data)}')
        if method == 'GET':
            request_params = get_request_params(environ)
            request['request_params'] = decoding_data(request_params)
            print(f'Получен GET: {decoding_data(request_params)}')

        # page controller
        view = self.routes_lst[path] if path in self.routes_lst else PageNotFound404()

        # front controller
        for front in self.fronts_lst:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
