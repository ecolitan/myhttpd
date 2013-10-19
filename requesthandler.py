import os
import sys
import mimetypes
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
            
        # testing
        #~ self.generate_test_response()
        
        self.construct_response()
        
    def return_response(self):
        """Return the response object"""
        return self.response
        
    def path_lookup(self):
        """Return list of files in request path"""
        if os.path.isfile(self.full_request_path):
            #TODO when file doesnt exist, set return code
            files = [self.full_request_path]
        elif os.path.isdir(self.full_request_path):
            files= [os.path.join(self.full_request_path, _file) for _file in os.listdir(self.full_request_path)]
        else:
            print "what kind of file is that!?"
            raise Exception
            #TODO proper error here. 5xx Server misconfigured
        
        return files
        
    def find_index(self, files):
        """Return the correct index from a list of files
        files: list of absolute paths
        return str index
        """
        if len(files) == 1:
            index = files[0]
        else:
            for _file in files:
                if os.path.split(_file)[-1] == self.config.directory_index:
                    index = _file
                    break
                else:
                    print "No index found!"
                    #TODO show dir listing maybe?
                    raise Exception
                
        return index
    
    def stat_file(self, _file):
        """Return information about resource
        st_size - size of file, in bytes,
        st_mtime - time of most recent content modification,
        """
        file_info = os.stat(_file)
        return file_info      
        
    def construct_response(self):
        """Look at request and constraints and build the response."""

        # here write complete logic before implementing!
        # unittests for this method!!
        # http://www.foss-sourcebook.org/parsing-http-headers-in-python/
        """
        if method == GET:
            handle any errors already in request
                return early if it doesnt make sense to continue working
            find specific resource URI is pointing at.
            get all info about the resource
                -> path to file
                -> size
                -> Content-type
                -> ETag
                -> Date
            foreach header in request:
                handle header appropriately
        elif method == HEAD:
            identical headers to GET, but NO body.
        elif method == POST:
            pass
        else
            didnt we already check for methods we dont support?
        """
        if self.handle_request_errors() == 'fatal':
            return None
            
        self.response.request_method = self.request.request_method

        if self.request.request_method == 'GET':
            self.process_get_method()
            
    def process_get_method(self):
        """Processing for GET Reqest Method"""
        files_in_uri_path = self.path_lookup()
        resource = self.find_index(files_in_uri_path)
        resource_info = self.stat_file(resource)
        resource_content_type, resource_content_encoding = mimetypes.guess_type(resource, strict=True)
        
        print "assign resource", resource
        self.response.resource = resource
        self.response.status = 'HTTP/1.1 200 OK'
        #TODO generate correctly.
        if self.check_content_type(resource_content_type):
            self.response.headers['Content-Type'] = resource_content_type
        self.response.headers['Date'] = self.generate_date_header()
        self.response.headers['Content-Length'] = self.generate_content_length_header(resource_info)
        self.response.headers['Last-Modified'] = self.generate_last_modififed_header(resource_info)
        self.response.headers['Connection'] = 'close' 
        self.response.print_response_headers()
        return True
        
    def handle_request_errors(self):
        """Handle errors in request object
        set error flags in response object.
        return request_status
        """
        for error, text in self.request.errors:
            # Errors in the request where processing should immediately stop
            if error in [500, 501, 505, 400, 403, 404, 405, 408, 414]:
                self.response.request_error = error
                request_status = 'fatal'
                return request_status
            #~ elif error in []:
            
    def check_content_type(self, resource_content_type):
        """Check if Client content type matches resource
        
        return True if client will accept content type
        """
        try:
            request_accept_string = self.request.headers['Accept']
        except KeyError:
            return True
            
        if len(request_accept_string) == 0:
            return True
            
        accepted_types = []
        type_list = request_accept_string.split(',')
        for _type in type_list:
            if _type.find(';') != -1:
                type_t = _type.split(';')[0]
                type_w = float(_type.split(';')[1][2:])
                type_with_weight = (type_t, type_w)
            else:
                type_with_weight = (_type, 1)
            accepted_types.append(type_with_weight)
            
        if resource_content_type in [i[0] for i in accepted_types]:
            return True
        else:
            return False
                
    def check_content_encoding(self, resource_content_type):
        """Check if Client Accept-encoding matches resource
        return True if client will accept encoding"""
        resource_encoding = resource_content_type[1]
        
        
    def set_resp_header_content_length(self):
        """Set response header Content-length"""
        pass
        
    def generate_etag_header(self):
        """Generate Etag string."""
        pass
        #TODO Optional, implement later. 
        
    def generate_date_header(self):
        """Return Date response header"""
        return strftime("%a, %d %b %Y %H:%M:%S +0200 GMT", gmtime())
        
    def generate_last_modififed_header(self, resource_info):
        """Return Last-Modified response header"""
        return strftime("%a, %d %b %Y %H:%M:%S +0200 GMT",
                        gmtime(resource_info.st_mtime))
        
    def generate_content_length_header(self, resource_info):
        """Return Content-Length response header"""
        return str(resource_info.st_size)
    
    
    
    
    
    
    
        
        
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
        self.response.headers['ETag'] = '2'
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
