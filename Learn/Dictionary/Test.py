import re
import socket
from select import select
TCP_TIMEOUT = 4

class EthernetKontroller(socket.socket):
    def __init__(self, ip: str = '10.1.13.213', port: int = 19227):
        """
        Class to connect to Ethernet to CAN converter
        :param ip: IP-Address of host to connect to
        :param port: Port of host to connect to
        """
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        super().connect((ip, port))

        self.init_state = False

        self.initiate_server()

    # Encoder to transform 4bit integer to the binary ascii representation of their hex-value
    hex_encoder_4bit = {
        0: b'0',
        1: b'1',
        2: b'2',
        3: b'3',
        4: b'4',
        5: b'5',
        6: b'6',
        7: b'7',
        8: b'8',
        9: b'9',
        10: b'A',
        11: b'B',
        12: b'C',
        13: b'D',
        14: b'E',
        15: b'F'
    }

    # List of regex patterns to categorise received messages
    regex_patterns = {
        'NOT INIT':     re.compile(rb'^R CAN 1 [-BEOT]{4}I [0-9]+$'),                   # Expected: R CAN 1 ----I XXX
        'READY':        re.compile(rb'^R CAN 1 ---[-T]- [0-9]+$'),                      # Expected: R CAN 1 ----- XXX
        'ERROR STATE':  re.compile(rb'(?=.*[BEO])^R CAN 1 [-BEOTI]{5} [0-9]+$'),        # Expected: R CAN 1 BEO-- XXX
        'RESPONSE':     re.compile(rb'^(R ERR|R ok|R CAN)')                             # Start of answers to commands
    }

    def get_hex_encode(self, to_encode: int) -> bytes:
        """
        Function to transform one Byte integers to a format the receiver can interpret
        :param to_encode: One Byte integer to convert into the ascii byte representation of its hex value
        :return: returns bytestring ascii representation of given integers hex value
        """
        return self.hex_encoder_4bit[(to_encode >> 4) & 0x0F] + self.hex_encoder_4bit[to_encode & 0x0F]

    def initiate_server(self) -> None:
        """
        Connect to Ethernet to CAN converter und initialise it if needed
        :return: None
        """
        self.init_state = True
        self.command(b'CAN 1 STOP')
        self.command(b'CAN 1 RESET')
        if not self.can_is_in_error_state():
            if self.can_is_not_initialised():
                print('Initialising!')
                if not (self.command(b'CAN 1 INIT STD 500') and self.command(b'CAN 1 FILTER ADD STD 0 0') and self.command(b'CAN 1 FILTER ADD EXT 0 0') and self.command(b'CAN 1 START')):
                    self.close()
                    raise EOFError('System not Initialised!')

                print('System successfully initialised!')

        else:
            raise EOFError('CAN is in ERROR state!')

        self.init_state = False

    def __call__(self, kontroller_id: int, led_pos: int = 0, color: int = 0) -> bool:
        """
        Function to send LED command to Ethernet to CAN converter
        :param kontroller_id: Row/ID of called LED-Conroller starting with 0
        :param led_pos: Number of called LED starting with 0
        :param color: Caller to use for called LED (index from list)
        :return: Success of failure of operation (True/False)
        """
        result = False
        self.stream_cache = b'M 1 CSD 0 ' +\
                            self.get_hex_encode(kontroller_id >> 8) +\
                            b' ' +\
                            self.get_hex_encode(kontroller_id) +\
                            b' ' +\
                            self.get_hex_encode(led_pos >> 8) +\
                            b' ' +\
                            self.get_hex_encode(led_pos) +\
                            b' ' +\
                            self.get_hex_encode(color) +\
                            b' 00 00 10\r\n'

        if self.send_stream(self.stream_cache):
            data = self.recv()
            if data and data[:7] == b'M 1 CSD':
                data = data.split(b' ')
                if (int(data[4]) << 8) + int(data[5]) == kontroller_id:
                    if int(data[6]) != 1:
                        if int(data[6]) != 2:
                            print('Settings Error!')

                    else:
                        result = True

        else:
            print('Timeout Error!')

        return result

    def recv(self, buffsize: int = 1024, command: bool = False) -> bytes:
        """
        Function to receive and filter Data from Ethernet to Can converter
        :param buffsize: size of recive buffer
        :param command: ignore normal CAN Messages (True)/ ignore Status answers (False)
        :return: recieved data that matches expectations or empty bytestring if no match was found
        """
        ans = super().recv(buffsize)
        print(ans)
        ans = ans.split(b'\r\n')
        print(ans)
        for data in ans:
            if data != '':
                print(self.regex_patterns['RESPONSE'].match(data) is not None, command == (self.regex_patterns['RESPONSE'].match(data) is not None))
                if command == (self.regex_patterns['RESPONSE'].match(data) is not None):
                    return data

        return b''

    def command(self, cmd: bytes, match: bool = False, match_pattern: str = '') -> bool:
        """
        Funcion to send command sequnce to Ethernet to CAN converter
        :param cmd: Command sequence to send
        :param match: if answer needs to match pattern otherwise matches against b'R ok'
        :param match_pattern: Pattern the answer needs to match to be a valid response
        :return: If command was successful (True)
        """
        if self.send_stream(cmd + b'\r\n'):
            if not match:
                return self.recv(command=True) == b'R ok'

            else:
                return self.regex_patterns[match_pattern].match(self.recv(command=True)) is not None
                # t = self.recv(command=True)
                # print(t, self.regex_patterns[match_pattern].match(t))
                # return self.regex_patterns[match_pattern].match(t) is not None

        else:
            return False

    def send_stream(self, stream: bytes) -> bool:
        """
        Function to directly send Data to Ethernet
        :param stream: bytestring to send
        :return: if an answer is available
        """
        super().sendall(stream)
        response = False
        timer = select([self], [], [], TCP_TIMEOUT)
        if timer[0]:
            response = True

        elif not self.init_state and not self.can_is_ready():
            self.initiate_server()

        return response

    def can_is_not_initialised(self) -> bool:
        return self.command(b'CAN 1 STATUS', match=True, match_pattern='NOT INIT')

    def can_is_ready(self) -> bool:
        return self.command(b'CAN 1 STATUS', match=True, match_pattern='READY')

    def can_is_in_error_state(self) -> bool:
        return self.command(b'CAN 1 STATUS', match=True, match_pattern='ERROR STATE')

    def close(self) -> None:
        super().close()