#/usr/bin/env python

import sys
from httprequest import HttpRequest
from requesthandler import RequestHandler
from vhostconfig import VhostConfig
from httpresponse import HttpResponse
from connectionhandler import ConnectionHandler

def main():
    g_config = VhostConfig()
    g_config.HOST = 'localhost'
    g_config.PORT = 8080
    g_config.document_root = "www"
    g_config.directory_index = "index.html"
    g_config.request_max_length = 4096
    g_config.connection_timeout = 5
    g_config.connection_buffer_size = 4

    connection_handler = ConnectionHandler(g_config)

    while connection_handler.queue_contains_request():
        next_request = connection_handler.pop_next_request()
        request_object = HttpRequest(next_request)
        request_handler = RequestHandler(g_config, request_object)
        test_response = request_handler.generate_test_response()
        
        connection_handler.send_reply(test_response)
        with open('www/index.html') as _f:
            for line in _f:
                connection_handler.send_reply(line)
        conn.close()

if __name__ == "__main__":
    main()
