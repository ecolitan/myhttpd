import socket
import sys

host = 'localhost'
port = 8080
size = 2048
test_request = "GET / HTTP:1/1\r\nHost: localhost\r\n\r\nGET /index.html HTTP:1/1\r\nHost: localhost\r\n\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send(test_request)
data = s.recv(size)
sys.stdout.write(data)
a = raw_input('\nwaiting...')
sys.stdout.write(a)
s.close()
