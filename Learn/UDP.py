import socket

UDP_IP = '10.1.10.118'
UDP_PORT = 8088
MESSAGE = b'WASISTUDP'


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))