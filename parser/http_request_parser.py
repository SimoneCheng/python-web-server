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
            self.parse()
        elif not self.done_parsing_header:
            self.parse_header()
            self.parse()
        elif not self.done_parsing_body:
            self.parse_body()
            self.parse()

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

    def parse_header(self):
        line = self.buffer.pop(separator="\r\n")
        if line is not None:
            if line:
                name, value = line.split(": ", maxsplit=1)
                if name.lower() == "content-length":
                    self.expected_body_length = int(value)
                self.parsed_data.update({ name: value })
            else:
                self.done_parsing_header = True
        else:
            self.done_parsing_header = True

    def parse_body(self):
        data = self.buffer.popAll()
        self.expected_body_length = len(data)
        self.parsed_data.update({ 'body': data })
        self.done_parsing_body = True
