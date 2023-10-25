from parser.http_request_buffer import Buffer

class HttpRequestParser:
    def __init__(self):
        self.buffer = Buffer()
        self.done_parsing_firstline = False
        self.done_parsing_header = False
        self.done_parsing_body = False
        self.expected_body_length = 0
        self.parsed_data = {}

    def feed_data(self, data):
        self.buffer.feed_data(data)
        self.parse()
        return self.parsed_data

    def parse(self):
        if not self.done_parsing_firstline:
            self.parse_firstline()

    def parse_firstline(self):
        first_line = self.buffer.pop(separator="\r\n")
        if first_line is not None:
            http_method, url, http_version = first_line.split()
            self.parsed_data.update({
                "http_method": http_method,
                "url": url,
                "http_version": http_version
            })
            self.done_parsing_firstline = True

    # def parse_header(self):

    # def parse_body(self):
