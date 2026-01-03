import socket
import time

s = socket.socket()
s_params = ('time.nist.gov', 37)
print('Connecting to NIST...')
s.connect(s_params)
print('Connected.')

try:
    response = b''
    while (len(temp := s.recv(20)) > 0):
        response += temp
except Exception as e:
    print(f'\nSomething went wrong: {e}\n')
finally:
    s.close()

nist_time = int.from_bytes(response, "big")
system_time = int(time.time()) + 2208988800 # number of seconds from 1900 to 1970
print(f'\nNIST time:\t{nist_time}')
print(f'System time:\t{system_time}')
print(f'Delta:\t\t{nist_time - system_time}')
print('\nDone.\n')