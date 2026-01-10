# Example usage:
#
# python chat_server.py 3490

import sys
import socket
import select
from chat_utils import get_server_response
import json

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
    buffers = {}
    nicks = {}
    clients = {}

    while True:
        ready_to_read, _, _ = select.select(my_sockets, {}, {})

        for s in ready_to_read:
            if s == listener_socket:
                new_conn = s.accept()
                new_socket = new_conn[0]
                my_sockets.add(new_socket)
                buffers[new_socket] = b''

                clients[new_socket] = new_conn[1]
                print(f'{clients[new_socket]}: connected')
            else:
                while len(buffers[s]) < 2:
                    temp = s.recv(128)
                    buffers[s] += temp
                    if len(temp) == 0:
                        break
                if len(temp) == 0:
                    data_dict = {"type" : "leave", "nick": nicks[s]}
                    my_sockets.discard(s)
                    print(f"{clients[s]}: disconnected")
                else:
                    size = int().from_bytes(buffers[s][0:2], 'big')
                    while len(buffers[s][2:]) < size:
                        temp = s.recv(1024)
                        buffers[s] += temp
                    if len(buffers[s][2:]) == size:
                        data = buffers[s][2:]
                        data_dict = json.loads(data.decode())
                        if data_dict["type"] == "hello":
                            nn = data_dict["nick"]
                            nicks[s] = nn

                msg = get_server_response(data_dict, nicks[s])
                for sock in my_sockets:
                    if sock != listener_socket:
                        sock.sendall(msg.encode())
                buffers[s] = b''

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
