class HttpResponse:
    
    #TODO this should come from config
    HTTPVersion = 'HTTP/1.1'
    
    def __init__(self):
        self.request_method = ''
        self.request_error = None
        self.status = ''
        self.headers = {}
        self.request_headers = []
        self.resource = None
        
    def print_response_headers(self):
        print self.generate_response_headers()
        print self.generate_response_body()
    
    def generate_response_headers(self):
        """Return final response header string
        Put headers in the correct order
        Put correct return status
        """
        
        # First line is the status code
        response_headers = self.status + '\r\n'
        
        # These headers need some sorting logic
        for _header in self.headers.keys():
            response_headers += _header + ': ' + self.headers[_header] + '\r\n'
        response_headers += '\r\n'
        
        return response_headers
        
    def generate_response_body(self):
        """Return the content of the response body according to the constraints
        set by the handler."""
        
        if self.request_method == "HEAD":
            # HEAD Requests dont return any body
            return None
        elif self.request_method == "GET":
            with open(self.resource) as _f:
                return _f.read()
        else:
            return None
            #TODO implement other methods
        
    def generate_status_code(self):
        """Generate the status code"""
        
        # pass request errors straight along.
        if self.request_error:
            return self.HTTPVersion + ' ' + str(self.request_error) + '\r\n'
            
        
