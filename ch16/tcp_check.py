def ip_to_bytes(ip):
    octets = ip.split('.')
    for i in range(len(octets)):
        octets[i] = int(octets[i]).to_bytes(1, "big")

    return b''.join(octets)

for i in range(10):
    with open(f'./tcp_data/tcp_addrs_{i}.txt', 'rb') as f:
        addrs_raw = f.read()
    with open(f'./tcp_data/tcp_data_{i}.dat', 'rb') as g:
        data_raw = g.read()

    addrs = addrs_raw.decode()
    src_ip, dst_ip = addrs.split()
    src_ip_bs = ip_to_bytes(src_ip)
    dst_ip_bs = ip_to_bytes(dst_ip)
    tcp_length = len(data_raw)

    ip_header = src_ip_bs + dst_ip_bs + b'\x00\x06' + tcp_length.to_bytes(2, "big")
    checksum_delivered = int.from_bytes(data_raw[16:18], "big")
    tcp_zero_cksum = data_raw[:16] + b'\x00\x00' + data_raw[18:]
    
    if len(tcp_zero_cksum) % 2 != 0:
        tcp_zero_cksum += b'\x00'

    data = ip_header + tcp_zero_cksum
    offset = 0
    total = 0
    while offset < len(data):
        word = int.from_bytes(data[offset : offset+2], "big")
        total += word
        total = (total & 0xffff) + (total >> 16)
        offset += 2
    total = (~total) & 0xffff

    if total == checksum_delivered:
        status = 'PASS'
    else:
        status = 'FAIL'
    
    print(f'Pair {i}: {status}')

print('\nDone.')