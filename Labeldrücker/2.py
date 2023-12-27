import socket
#list = [
#'|CCB|A1|', '|CCB|A2|', '|CCB|A3|', '|CCB|A4|', '|CCB|A5|', '|CCB|A6|',	'|CCB|A7|',	'|CCB|A8|',	'|CCB|A9|',	'|CCB|A10|', '|CCB|A11|', '|CCB|A12|',
#'|CCB|B1|', '|CCB|B2|', '|CCB|B3|', '|CCB|B4|', '|CCB|B5|', '|CCB|B6|',	'|CCB|B7|',	'|CCB|B8|',	'|CCB|B9|',	'|CCB|B10|', '|CCB|B11|', '|CCB|B12|',
#'|CCB|C1|', '|CCB|C2|', '|CCB|C3|', '|CCB|C4|', '|CCB|C5|', '|CCB|C6|',	'|CCB|C7|',	'|CCB|C8|',	'|CCB|C9|',	'|CCB|C10|', '|CCB|C11|', '|CCB|C12|',
#'|CCB|D1|', '|CCB|D2|', '|CCB|D3|', '|CCB|D4|', '|CCB|D5|', '|CCB|D6|',	'|CCB|D7|',	'|CCB|D8|',	'|CCB|D9|',	'|CCB|D10|', '|CCB|D11|', '|CCB|D12|',
#'|CCB|E1|', '|CCB|E2|', '|CCB|E3|', '|CCB|E4|', '|CCB|E5|', '|CCB|E6|',	'|CCB|E7|',	'|CCB|E8|',	'|CCB|E9|',	'|CCB|E10|', '|CCB|E11|', '|CCB|E12|',
#'|CCB|F1|', '|CCB|F2|', '|CCB|F3|', '|CCB|F4|', '|CCB|F5|', '|CCB|F6|',	'|CCB|F7|',	'|CCB|F8|',	'|CCB|F9|',	'|CCB|F10|', '|CCB|F11|', '|CCB|F12|',
#'|CCB|G1|', '|CCB|G2|', '|CCB|G3|', '|CCB|G4|', '|CCB|G5|', '|CCB|G6|',	'|CCB|G7|',	'|CCB|G8|',	'|CCB|G9|',	'|CCB|G10|', '|CCB|G11|', '|CCB|G12|'
#'|CCB|H1|', '|CCB|H2|', '|CCB|H3|', '|CCB|H4|', '|CCB|H5|', '|CCB|H6|',	'|CCB|H7|',	'|CCB|H8|',	'|CCB|H9|',	'|CCB|H10|', '|CCB|H11|', '|CCB|H12|']



list = [
'|CCB|I1|', '|CCB|I2|', '|CCB|I3|', '|CCB|I4|', '|CCB|I5|', '|CCB|I6|',	'|CCB|I7|',	'|CCB|I8|',	'|CCB|I9|',	'|CCB|I10|', '|CCB|I11|', '|CCB|I12|'
'|CCB|J1|', '|CCB|J2|', '|CCB|J3|', '|CCB|J4|', '|CCB|J5|', '|CCB|J6|',	'|CCB|J7|',	'|CCB|J8|',	'|CCB|J9|',	'|CCB|J10|', '|CCB|J11|', '|CCB|J12|'
]

for i in range(len(list)):
    if len(list[i]) == 8:
        test = f"""
                ^XA
                ^POI 
                ^LL400 
        
                ^FO120,150
                ^A0N,250,250
                ^FD{list[i][5:7]} 
                ^FS
        
                ^FO700,155
                ^BXN,10,800
                ^FD{list[i]}
                ^FS 
        
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
                ^POI
                ^LL400 

                ^FO120,150
                ^A0N,250,250
                ^FD{list[i][5:8]} 
                ^FS

                ^FO700,155
                ^BXN,10,800
                ^FD{list[i]}
                ^FS 

                ^XZ
                """

        test_b = test.encode('utf-8')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "10.1.13.210"
        port = 9100
        s.connect((host, port))
        s.send(test_b)
        s.close()
