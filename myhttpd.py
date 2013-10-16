#/usr/bin/env python

import sys

from vhostconfig import VhostConfig
from connectionmanager import HttpdServer, ClientThread

def main():
    
    # Set up g_config object (global config)
    g_config = VhostConfig()
    #~ g_config.host = 'localhost'
    g_config.host = ''
    g_config.port = 8080
    g_config.document_root = "www"
    g_config.directory_index = "index.html"
    g_config.request_max_length = 4096
    g_config.connection_timeout = 5
    g_config.connection_buffer_size = 2048
    g_config.connection_backlog = 5

    s = HttpdServer(g_config)
    s.run()
    sys.exit(3)
    
if __name__ == "__main__":
    main()
