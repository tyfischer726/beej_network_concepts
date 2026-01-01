import socket
import sys

default_address = 'example.com'
default_port = 80

argc = len(sys.argv)
match argc:
    case 3:
        address = sys.argv[1]
        port = int(sys.argv[2])
    case 2: # no port provided
        address = sys.argv[1]
        port = default_port
    case _: # no arguments provided
        address = default_address
        port = default_port

s = socket.socket()
s_params = (address, port)
print(f"Connecting to {address} on port {port}...")
s.connect(s_params)
print("Connected.\n")

req = ["GET / HTTP/1.1", f"Host: {address}", "Connection: close"]
req = '\r\n'.join(req) + '\r\n\r\n'
s.sendall(req.encode('ISO-8859-1'))
print(f'Request sent:\n{req}')

response = b''
while (len(temp := s.recv(4096)) > 0):
    response += temp
response = response.decode('ISO-8859-1')
print(f'Response:\n{response}')

s.close()
print('\nDone.')