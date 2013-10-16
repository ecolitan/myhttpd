class HttpResponse:
    
    def __init__(self):
        self.status = ''
        self.headers = {}
        self.request_headers = []
    
    def generate_response_headers(self):
        """Return final response header string
        Put headers in the correct order
        Put correct return status
        """
        
        response_headers = self.status + '\r\n'
        for _header in self.headers.keys():
            response_headers += _header + ': ' + self.headers[_header] + '\r\n'
        response_headers += '\r\n'
        
        return response_headers
        
    def generate_response_body(self):
        with open('www/index.html') as _f:
            return _f.read()
        
    def encode_body(self):
        pass


