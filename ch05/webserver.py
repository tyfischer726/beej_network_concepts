import socket
import sys

default_port = 28333

argc = len(sys.argv)
match argc:
    case 2:
        port = int(sys.argv[1])
    case _: # no arguments provided
        port = default_port

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_params = ('', port)
s.bind(s_params)
s.listen()
print(f'Listening on port {port}...\n')

while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    new_socket.settimeout(1.0) # close the browser's pre-connect
    print(f'New connection: {new_conn}\n')
    try:
        request = b''
        while True:
            temp = new_socket.recv(4096)
            request += temp
            if (b"\r\n\r\n" in temp):
                break
        request = request.decode('ISO-8859-1')
        print(f'Request:\n{request}')


        ### Response ###
        code = 200
        status = 'OK'
        content = "Hello, world!"

        response = [f"HTTP/1.1 {code} {status}", "Content-Type: text/plain", f"Content-Length: {len(content)}", "Connection: close"]
        response = '\r\n'.join(response) + '\r\n\r\n' + content
        new_socket.sendall(response.encode("ISO-8859-1"))
        print(f'Response sent:\n{response}\n\n\n')
    except socket.timeout:
        print(f"Connection timed out.\n")
    finally:
        new_socket.close()

s.close()
print('\nDone.')