x = [72, 73]

x_bytearr = bytearray(x)
x_bytes = bytes(x)
x_list1 = list(x_bytearr)
x_list2 = list(x_bytes)

print('\n')
print(f'x:\t\t{x}')
print(f'x_barr:\t\t{x_bytearr}')
print(f'x_bytes:\t{x_bytes}')
print(f'x_list1:\t{x_list1}')
print(f'x_list2:\t{x_list2}')
print('\n\n\n')

msg = 'Hello'
msg_bytes = bytes(msg, "UTF-8")
decoded = msg_bytes.decode("UTF-8")
byte_list = list(msg_bytes)
hex_bytes = [hex(B) for B in byte_list]
msg_int = int.from_bytes(msg_bytes)

print(f'msg:\t\t{msg}')
print(f'bytes:\t\t{msg_bytes}')
print(f'decoded:\t{decoded}')
print(f'byte list:\t{byte_list}')
print(f'byte hex:\t{hex_bytes}')
print(f'int:\t\t{msg_int}')
print('\n')