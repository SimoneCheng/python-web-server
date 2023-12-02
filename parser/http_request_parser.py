from parser.buffer import Buffer
from parser.form_data_parser import FormDataParser
from parser.json_parser import JsonParser

class HttpRequestParser:
    def __init__(self):
        self.buffer = Buffer()
        self.done_parsing_firstline = False
        self.done_parsing_header = False
        self.done_parsing_body = False
        self.parsed_data = {}

    def feed_data(self, data):
        self.buffer.feed_data(data)
        return self.parse()

    def parse(self):
        self.parse_firstline()
        self.parse_header()
        self.parse_body()
        return self.parsed_data

    def parse_firstline(self):
        if not self.done_parsing_firstline:
            first_line = self.buffer.pop(separator="\r\n")
            if first_line is not None:
                http_method, url, http_version = first_line.split()
                self.parsed_data.update({
                    "http-method": http_method,
                    "url": url,
                    "http-version": http_version
                })
                self.done_parsing_firstline = True

    def parse_header(self):
        while not self.done_parsing_header:
            line = self.buffer.pop(separator="\r\n")
            if line is not None and line:
                name, value = line.split(": ", maxsplit=1)
                self.parsed_data.update({ name.lower(): value })
            else:
                self.done_parsing_header = True

    def parse_body(self):
        if 'content-type' not in self.parsed_data:
            self.done_parsing_body = True
        if not self.done_parsing_body:
            data = self.buffer.popAll()
            content_type_arr = self.parsed_data['content-type'].split('; ')
            if content_type_arr[0] == 'multipart/form-data':
                form_data_parser = FormDataParser()
                boundary = '--' + content_type_arr[1][9:] # 感覺不是一個好方法
                body = form_data_parser.feed_data(data[len(boundary):], boundary)
                self.parsed_data.update({ 'body': body })
            if content_type_arr[0] == 'application/json':
                json_parser = JsonParser()
                body = json_parser.feed_data(data)
                self.parsed_data.update({ 'body': body })
            else:
                self.parsed_data.update({ 'body': data })
            self.done_parsing_body = True
