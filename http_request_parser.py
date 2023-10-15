class HttpRequestParser:
    def __init__(self, request_data):
        self.raw_request_data = request_data

    def parse_header(self):
        method = ''
        endpoint = ''
        http_version = ''
        space_counter = 0
        line_counter = 0
        for char in self.raw_request_data:
            if (char == ' '):
                space_counter += 1
            if (space_counter == 0):
                method = method + char
            if (space_counter == 1 and char != ' '):
                endpoint = endpoint + char
            if (space_counter == 2 and line_counter == 0 and char != ' '):
                http_version = http_version + char
        return {
            'method': method,
            'endpoint': endpoint,
            'http_version': http_version
        }
        # print(self.raw_request_data)

    def parse_body(self):
        print('still working')

    def get_http_version(self):
        request_first_line = self.raw_request_data.split('\r\n')[0]
        http_version = request_first_line.split(' ')[-1]
        return http_version

    def get_method(self):
        request_split_with_space = self.raw_request_data.split(' ')
        return request_split_with_space[0]

    def get_endpoint(self):
        request_split_with_space = self.raw_request_data.split(' ')
        return request_split_with_space[1]
