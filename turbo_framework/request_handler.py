from log.log_config import LOGGER


def parse_input_data(data: str):
    result = {}

    if data:
        params = data.split('&')
        for item in params:
            key, value = item.split('=')
            result[key] = value

    return result


class GetRequests:
    @staticmethod
    def get_request_params(environ):
        # получаем параметр запроса
        query_str = environ['QUERY_STRING']
        # параметры -> словарь
        request_params = parse_input_data(query_str)
        return request_params


class PostRequests:
    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        # получаем длину тела
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        # print(content_length)

        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes) -> dict:
        result = {}

        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            LOGGER.info(f'Line after decoding: {data_str}')
            # данные -> словарь
            result = parse_input_data(data_str)

        return result

    def get_request_params(self, environ):
        # получаем данные
        data = self.get_wsgi_input_data(environ)
        # данные -> словарь
        data = self.parse_wsgi_input_data(data)
        return data
