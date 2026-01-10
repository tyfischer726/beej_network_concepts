# Example usage:
#
# python chat_client.py alice localhost 3490
# python chat_client.py bob localhost 3490
# python chat_client.py chris localhost 3490

import sys
import socket
from chatui.chatui import init_windows, read_command, print_message, end_windows
import threading
import json
from chat_utils import get_json, send_msg

def usage():
    print("usage: chat_client.py nickname host port", file=sys.stderr)

def runner_listen(s):
    while True:
        try:
            server_response = s.recv(1024)
        except Exception:
            break
        server_response = json.loads(server_response.decode())
        type = server_response["type"]
        nick = server_response["nick"]
        if type == "chat":
            msg = server_response["message"]
            print_msg = f"{nick}: {msg}"
        elif type == "join":
            print_msg = f"*** {nick} has joined the chat"
        elif type == "leave":
            print_msg = f"*** {nick} has left the chat"
        print_message(print_msg)

def runner_client(s, nickname):
    type = "hello"
    nick = nickname
    message = ""
    msg = get_json(type, nick, message)
    send_msg(s, msg)
    while True:
        msg = read_command(f'{nickname}> ')
        if msg == '/q':
            s.close()
            break
        type = "chat"
        msg = get_json(type, nick, msg)
        send_msg(s, msg)

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))
    
    init_windows()
    listener = threading.Thread(target=runner_listen, args = (s,), daemon=True)
    client_t = threading.Thread(target=runner_client, args = (s, nickname))
    threads = [listener, client_t]

    listener.start()
    client_t.start()

    for t in threads:
        t.join()

    print('\nProgram exited.')

if __name__ == "__main__":
    sys.exit(main(sys.argv))
