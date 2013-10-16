import socket
import threading

# http://ilab.cs.byu.edu/python/threadingmodule.html
# http://ilab.cs.byu.edu/python/code/echoclient-select.py

class ConnectionHandler:
    """
    Create socket.
    listen for incoming connections
    create requesthandler and pass it connection
    cleanup connection at end
    """
    
    request_terminator = '\r\n\r\n'
    
    def __init__(self, config):
        """Create sockets"""
        
        self.config = config
        self.request_queue = ''
        self.create_listener_socket()
        print "we got here"
        self.conn = self.listen()
        print "we got there"
        
    def create_listener_socket(self):
        """Create basic socket object"""
        
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.setblocking(1)
        self.listener.bind((self.config.HOST, self.config.PORT))
        self.listener.listen(5)
        return None
        
    def listen(self):
        """Listen on socket for data
        write all data to self.request_queue
        """
        
        conn, addr = self.listener.accept()
        
        while len(self.request_queue) < self.config.request_max_length:
            data = conn.recv(self.config.connection_buffer_size)
            self.request_queue += data
            
            if not data:
                break
        return conn
        
    def print_request_queue(self):
        """Print whole request queue"""
        
        print self.request_queue
        return None
        
    def pop_next_request(self):
        """Return first request in request queue
        request is removed from the queue
        return None if no valid request
        """
        
        request_end = self.request_queue.find(self.request_terminator)
        if request_end == -1:
            next_request = None
        else:
            next_request = self.request_queue[:request_end + len(self.request_terminator)]
            self.request_queue = self.request_queue[request_end + len(self.request_terminator):]
            
        return next_request
        
    def queue_contains_request(self):
        """return True if queue contains a request"""
        
        request_end = self.request_queue.find(self.request_terminator)
        if request_end == -1:
            request_exists = False
        else:
            request_exists = True
            
        return request_exists
        
    def send_reply(self, message):
        """send message back over connection"""
        
        self.conn.send(message)
        return None
