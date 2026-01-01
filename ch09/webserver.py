import socket
import sys
import os

default_port = 28333
server_root = os.path.abspath('.')

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
        lines = request.split('\r\n')
        path = lines[0].split()[1]
        path = os.path.abspath(path)
        if path == '/':
            file = '/'
        else:
            file = os.path.split(path)[1]
            path = os.path.split(path)[0]
        print(f'Request:\n{request}')


        ### Response ###
        if file != '/':
            try:
                with open(f'{server_root}{path}/{file}', 'rb') as f:
                    content = f.read()
                    f.close()
                code = 200
                status = 'OK'

                # determine content type
                ext = os.path.splitext(file)[1]
                match ext:
                    case '.html':
                        content_type = 'text/html'
                    case '.txt':
                        content_type = 'text/plain'
                    case _: # default content "Hello, world!"
                        content_type = 'text/plain'
            except Exception:
                code = 404
                status = 'Not Found'
                content = b"404 not found"
                content_type = 'text/plain'
        else: # default path '/'
                code = 200
                status = 'OK'
                content = b"Hello, world!"
                content_type = 'text/plain'

        response = [f"HTTP/1.1 {code} {status}", f"Content-Type: {content_type}", f"Content-Length: {len(content)}", "Connection: close"]
        response = '\r\n'.join(response) + '\r\n\r\n'
        new_socket.sendall(response.encode("ISO-8859-1") + content)
        print(f'Response sent:\n{response}\n\n\n')
    except socket.timeout:
        print(f"Connection timed out.\n")
    finally:
        new_socket.close()

s.close()
print('\nDone.')