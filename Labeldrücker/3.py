import socket

list = ['|CCB|G9|',	'|CCB|G10|']

for i in range(len(list)):
    if len(list[i]) == 8:
        test = f"""
        ^XA
        ^POI  ; Установка вертикальной ориентации (Portrait)
        ^LL400 ; Установка высоты этикетки

        ^FO120,150
        ^A0N,250,250
        ^FD {list[i][5:7]} 
        ^FS

        ^FO700,155
        ^BXN,12,800
        ^FD{list[i]}
        ^FS  ; Генерация и вывод QR-кода

        ^XZ
        """

        test_b = test.encode('utf-8')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "10.1.13.210"
        port = 9100
        s.connect((host, port))
        s.send(test_b)
        s.close()
    else:
        test = f"""
                ^XA
                ^POI  ; Установка вертикальной ориентации (Portrait)
                ^LL400 ; Установка высоты этикетки

                ^FO120,150
                ^A0N,250,250
                ^FD {list[i][5:8]} 
                ^FS

                ^FO700,155
                ^BXN,10,800
                ^FD{list[i]}
                ^FS  ; Генерация и вывод QR-кода

                ^XZ
                """

        test_b = test.encode('utf-8')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "10.1.13.210"
        port = 9100
        s.connect((host, port))
        s.send(test_b)
        s.close()
