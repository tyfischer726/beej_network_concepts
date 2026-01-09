# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    listener_port = port
    listener_socket = socket.socket()
    listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener_socket_params = ('', listener_port)
    listener_socket.bind(listener_socket_params)
    listener_socket.listen()
    print(f'Listening on port {listener_port}...\n')

    my_sockets = {listener_socket}
    ready_to_read = {}

    while True:
        ready_to_read, _, _ = select.select(my_sockets, {}, {})

        for s in ready_to_read:
            if s == listener_socket:
                new_conn = s.accept()
                new_socket = new_conn[0]
                my_sockets.add(new_socket)

                print(f'{new_conn[1]}: connected')
            else:
                data = s.recv(4096)
                peer = s.getpeername()
                if len(data) == 0:
                    my_sockets.remove(s)
                    print(f'{peer}: disconnected')
                else:
                    print(f'{peer} {len(data)} bytes: {data}')

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
