from kmp_search import kmp_search

class HttpRequestParser:
    def __init__(self, request_data):
        self.raw_request_data = request_data

    def parse_header(self):
        result = {}
        line_index_array = kmp_search('\r\n', self.raw_request_data)
        key_index_array = kmp_search(': ', self.raw_request_data)

        # 先 parse 第一行
        method = ''
        endpoint = ''
        http_version = ''
        space_counter = 0
        line_counter = 0
        for i in range(0, line_index_array[0]):
            char = self.raw_request_data[i]
            if (char == ' '):
                space_counter += 1
            if (space_counter == 0):
                method = method + char
            if (space_counter == 1 and char != ' '):
                endpoint = endpoint + char
            if (space_counter == 2 and line_counter == 0 and char != ' '):
                http_version = http_version + char
        result['method'] = method
        result['endpoint'] = endpoint
        result['http_version'] = http_version

        # parse 其他行
        for i in range(0, len(key_index_array)):
            key_start_index = line_index_array[i] + 2
            key_end_index = key_index_array[i]
            key = self.raw_request_data[key_start_index:key_end_index]
            value_start_index = key_index_array[i] + 2
            value_ended_index = line_index_array[i + 1]
            value = self.raw_request_data[value_start_index:value_ended_index]
            result[key] = value

        return result

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
