class HttpRequest:
    """HttpRequest object."""
    
    # Supported Methods
    SAFE_METHODS = ['GET', 'HEAD']
    UNSAFE_METHODS = ['POST']
    SUPPORTED_METHODS = set(SAFE_METHODS + UNSAFE_METHODS)
    
    # Limits
    MAX_HEADERS = 100
    MAX_HEADER_SIZE = 8192
    
    # Supported Request Headers
    GENERAL_HEADERS = ['Cache-Control', 'Connection', 'Date', 'Pragma',
        'Trailer', 'Transfer-Encoding', 'Upgrade', 'Via', 'Warning']
    REQUEST_HEADERS = ['Accept', 'Accept-Charset', 'Accept-Encoding',
        'Accept-Language', 'Authorization', 'Expect', 'From', 'Host',
        'If-Match', 'If-Modified-Since', 'If-None-Match', 'If-Range',
        'If-Unmodified-Since', 'Max-Forwards', 'Proxy-Authorization',
        'Range', 'Referer', 'TE', 'User-Agent']
    ENTITY_HEADERS = ['Allow', 'Content-Encoding', 'Content-Language',
        'Content-Length', 'Content-Location', 'Content-MD5', 'Content-Range',
        'Content-Type', 'Expires', 'Last-Modified', 'extension-header']
    SUPPORTED_HEADERS = set(GENERAL_HEADERS + REQUEST_HEADERS + ENTITY_HEADERS)
    
    def __init__(self, request):
        """Accept a single request as a string, ended by \n\r\n\r
        Parse string and set method and header flags.
        If request is found to be invalid during parsing, set error flags
        """
        self.request = request
        self.errors = []
        self.request_method = ''
        self.request_uri = ''
        self.request_version = ''
        self.headers = {}
        self.warnings = []
        
        self.parse_request()
        
    def __str__(self):
        return str(self.request)
        
    def __repr__(self):
        return self.__str__()
        
    def parse_request(self):
        '''Determine request method and request headers'''
        
        split_request = self.request.split('\r\n')
        if len(split_request) < 2:
            self.error.append((400, 'Bad Request'))
            return None
            
        try:
            self.request_method  = split_request[0].split(' ')[0]
            self.request_uri     = split_request[0].split(' ')[1]
            self.request_version = split_request[0].split(' ')[2]
        except IndexError:
            self.errors.append((400, 'Bad Request'))
            print "Error parsing method string"
            
        if self.request_method not in self.SUPPORTED_METHODS:
            self.errors.append((501, 'Not Implemented'))
            print "Unsupported method: ", split_request[0]
            
        for header_item in split_request[1:]:
            try:
                header_label = header_item.split(': ')[0]
                header_content = header_item.split(': ')[1]
            except IndexError:
                continue
                
            if header_label not in self.SUPPORTED_HEADERS:
                self.errors.append(
                    (400, 'Bad Request - Header {0} unknown'.format(header_label)))
            else:
                self.headers[header_label] = header_content
        
