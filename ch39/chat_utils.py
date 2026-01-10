import json

def get_json(type, nick, message):
    data_dict = {}
    data_dict["type"] = type
    data_dict["nick"] = nick
    data_dict["message"] = message

    if type == "hello":
        del data_dict["message"]
    elif type == "chat":
        del data_dict["nick"]
    
    return json.dumps(data_dict)

def send_msg(s, msg):
    msg_bytes = msg.encode()
    size = len(msg_bytes).to_bytes(2, "big")
    data = size + msg_bytes
    s.sendall(data)

def get_server_response(data_dict, nn):
    response = data_dict
    if response["type"] == "hello":
        response["type"] = "join"
    elif response["type"] == "chat":
        msg_tmp = response.pop("message")
        response["nick"] = nn
        response["message"] = msg_tmp

    return json.dumps(response)