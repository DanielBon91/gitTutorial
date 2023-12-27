import socket

test = """
^XA

^FO10,45
^A0N,36,50
^FDDisc:
^FS

^FO140,45
^A0N,40,60
^FD10001
^FS

^FO320,45
^A0N,36,45
^FDArgenZ esthetic 98x14 2S
^FS

^FO850,25
^BXN,5,200
^FD|D|10001|
^FS

^XZ
"""

test_b = test.encode('utf-8')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.1.13.211"
port = 9100
s.connect((host, port))
s.send(test_b)
s.close()