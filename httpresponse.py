class HttpResponse:
    
    def __init__(self):
        self.status = ''
        self.headers = {}
        
    def generate_response_headers(self):
        """Return final response header string"""
        
        response_headers = self.status + '\r\n'
        for _header in self.headers.keys():
            response_headers += _header + ': ' + self.headers[_header] + '\r\n'
        response_headers += '\r\n'
        
        return response_headers
        
    def generate_response_body(self):
        pass
        
    def encode_body(self):
        pass


