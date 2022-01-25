def parse_input_data(data):
    """Преобразует стоку запроса в словарь"""
    result = {}
    if data:
        params = data.split('&')
        for item in params:
            k, v = item.split('=')
            result[k] = v
    return result


def post_request_params(environ):
    """парсинг и обработка POST, возвращает словарь"""
    content_length_data = environ.get('CONTENT_LENGTH')
    content_length = int(content_length_data) if content_length_data else 0
    data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
    result = {}
    if data:
        # декодируем данные
        data_str = data.decode(encoding='utf-8')
        # print('POST: ', data_str)
        result = parse_input_data(data_str)
    return result


def get_request_params(environ):
    """обрабатывает get, возвращает словарь"""
    query_string = environ['QUERY_STRING']
    request_params = parse_input_data(query_string)
    # print('GET: ', query_string)
    return request_params



