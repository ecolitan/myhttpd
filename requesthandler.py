import os
import sys
from time import strftime, gmtime
from httpresponse import HttpResponse

class RequestHandler:
    def __init__(self, config, request):
        """Take a VhostConfig and HttpRequest object"""
        self.config = config
        self.request = request
        self.response = HttpResponse()
        
        self.full_request_path = os.path.join(self.config.document_root,
            self.request.request_uri[1:])
        
    def path_lookup(self):
        """Return list of files in request path
        Check file exists if specififed.
        """
        
        if os.path.isfile(self.full_request_path):
            files = [self.full_request_path]
        elif os.path.isdir(self.full_request_path):
            files = os.listdir(self.full_request_path)
        else:
            print "what kind of file is that!?"
            raise Exception
        
        return files
        
    def find_index(self, files):
        """Return the correct index from a list of files
        files: absolute paths
        return file
        """
        if len(files) == 1:
            index = files[0]
        else:
            for _file in files:
                if os.path.split(_file)[-1] == self.config.directory_index:
                    index = _file
                else:
                    print "No index found!"
                    #TODO show dir listing maybe?
                    raise Exception
                
        return index
    
    def stat_file(self, _file):
        """Return information about a file"""
        
        file_info = os.stat(_file)
        return file_info
        
    def construct_response(self):
        """look at request and constraints and build the response."""
        pass
        
        
###############################################################################
    def generate_test_response(self):
        test_index = 'www/index.html'
        file_info = self.stat_file(test_index)
        complete_response = 'www/index.html'
        
        self.response.status = 'HTTP/1.1 200 OK'
        self.response.headers['Date'] = strftime(
            "%a, %d %b %Y %H:%M:%S +0200 GMT", gmtime())
        self.response.headers['Server'] = 'myhttpd/0.01'
        self.response.headers['Last-Modified'] = strftime(
            "%a, %d %b %Y %H:%M:%S +0200 GMT", gmtime(file_info.st_mtime))
        self.response.headers['ETag'] = '1'
        self.response.headers['Accept-Ranges'] = 'bytes'
        self.response.headers['Content-Length'] = str(file_info.st_size)
        self.response.headers['Vary'] = 'Accept-Encoding'
        self.response.headers['Connection'] = 'close'        
        self.response.headers['Content-Type'] = 'text/html'        
        
        test_response = self.response.generate_response_headers()
        
        return test_response
        
    def generate_test_body(self, conn):
        with open('www/index.html') as _f:
            for line in _f:
                conn.send(line)
###############################################################################
