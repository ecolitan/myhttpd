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
        self.status_code = ''
        self.status_text = ''
        
    def generate_status_code(self):
        """Generate the status code"""
        #TODO pass request errors straight along.
        status_line = '{0} {1} {2}\r\n'.format(self.HTTPVersion,
                                               self.status_code,
                                               self.status_text)
        return status_line
        
    def generate_response_headers(self):
        """Return final response header string
        Put headers in the correct order
        Put correct return status
        """
        #TODO These headers need some sorting logic
        response_headers = ''
        for _header in self.headers.keys():
            response_headers += _header + ': ' + self.headers[_header] + '\r\n'
        response_headers += '\r\n'
        
        return response_headers
        
    def generate_response_body(self):
        """Return the content of the response body according to the constraints
        set by the handler."""
        empty_body = ''
        
        if self.status_code == '404':
            return 'Error 404: Page not found.\r\n'
            
        if self.request_method == "HEAD":
            # HEAD Requests dont return any body
            return empty_body
        elif self.request_method == "GET":
            with open(self.resource) as _f:
                return _f.read()
        else:
            return empty_body
            #TODO implement other methods
        

            
        
