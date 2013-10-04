class HttpRequest:
    REQUEST_METHODS = ['GET', 'HEAD']
    HEADERS = ['Accept', 'Accept-Encoding', 'Accept-Language', 'Connection',
        'Host', 'User-Agent']
    #TODO add rest of methods and headers
    
    def __init__(self, request):
        self.request = request
        self.errors = []
        self.request_method = ''
        self.request_uri = ''
        self.request_version = ''
        self.headers = {}
        
        self.parse_request()
        
    def __str__(self):
        return str(self.request)
        
    def __repr__(self):
        return self.__str__()
        
    def print_complete(self):
        print repr(self.request)
        return None
        
    def print_method_string(self):
        print self.request_method + ' ' + self.request_uri + ' ' + self.request_version
        return None
        
    def print_headers(self):
        print str(self.headers)
        return None
        
    def parse_request(self):
        '''Split request into individual headers'''
        
        split_request = self.request.split('\r\n')
        
        if len(split_request) < 2:
            self.error.append((400, 'Bad Request'))
            
        try:
            self.request_method  = split_request[0].split(' ')[0]
            self.request_uri     = split_request[0].split(' ')[1]
            self.request_version = split_request[0].split(' ')[2]
            
        except IndexError:
            self.errors.append((400, 'Bad Request'))
            
        if split_request[0] not in self.REQUEST_METHODS:
            self.errors.append((501, 'Not Implemented'))
            
        for header_item in split_request[1:]:
            try:
                header_label = header_item.split(': ')[0]
                header_content = header_item.split(': ')[1]
            except IndexError:
                continue
                
            if header_label not in self.HEADERS:
                self.errors.append(
                    (400, 'Bad Request - Header {0} unknown'.format(header_label)))
            else:
                self.headers[header_label] = header_content
