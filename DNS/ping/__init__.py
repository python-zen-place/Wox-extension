import time
import struct
import socket
import select


def checksum(source):
    sum = 0
    source_len = len(source)
    count_to = len(source) & 0xfffe
    for i in range(0, count_to, 2):
        cur = source[i + 1] * 256 + source[i]
        sum += cur
    if count_to < source_len:
        sum += source[count_to]
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    res = ~sum & 0xffff
    res = res >> 8 | (res << 8 & 0xff00)
    return res


def raw_socket(dst_addr, icmp_packet):
    rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    send_request_ping_time = time.time()
    rawsocket.sendto(icmp_packet, (dst_addr, 80))
    return send_request_ping_time, rawsocket, dst_addr


def send_ping(data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body):
    icmp_packet = struct.pack('>BBHHH32s', data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body)
    icmp_checksum = checksum(icmp_packet)
    icmp_packet = struct.pack('>BBHHH32s', data_type, data_code, icmp_checksum, data_ID, data_Sequence, payload_body)
    return icmp_packet


def reply_ping(send_request_ping_time, rawsocket, data_Sequence, timeout=10):
    while True:

        started_select = time.time()
        what_ready = select.select([rawsocket], [], [], timeout)
        wait_for_time = (time.time() - started_select)
        if not what_ready[0]:  # Timeout
            return -1
        time_received = time.time()
        received_packet, addr = rawsocket.recvfrom(1024)
        icmpHeader = received_packet[20:28]
        type, code, checksum, packet_id, sequence = struct.unpack(
            ">BBHHH", icmpHeader
        )
        if type == 0 and sequence == data_Sequence:
            return time_received - send_request_ping_time
        timeout = timeout - wait_for_time
        if timeout <= 0:
            return -1


def ping(host, data_type=8, data_code=0, data_checksum=0, data_ID=0, data_Sequence=1, payload_body=b'114514'):
    dst_addr = socket.gethostbyname(host)
    sum = 0
    for i in range(0, 4):
        icmp_packet = send_ping(data_type, data_code, data_checksum, data_ID, data_Sequence + i, payload_body)
        send_request_ping_time, rawsocket, addr = raw_socket(dst_addr, icmp_packet)
        times = reply_ping(send_request_ping_time, rawsocket, data_Sequence + i)
        if times > 0:
            sum += int(times*1000)
        else:
            return '超时'
    return '{}ms'.format(sum/4)