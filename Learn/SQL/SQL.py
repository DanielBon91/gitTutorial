import customtkinter
import pyodbc as odbc

conn = odbc.connect("Driver={SQL Server};"
                    "Server=NB-DBO-01\SQLEXPRESS;"
                    "Database=ARGEN;"
                    "Trusted_Connection=yes;")

cur = conn.cursor()

def input_update():
    Name = input('Name ')
    Artikel = input('Artikel ')
    Firma = input('Firma ')
    count = int(input("Menge "))
    anfrage = f"UPDATE Argen SET Artikel = '{Artikel}', Firma = '{Firma}', Menge = '{count}' WHERE Name = '{Name}'"
    cur.execute(anfrage)
    conn.commit()

def select():
    cur_sel = cur.execute("SELECT * FROM Mitarbeiter")
    list = []
    for row in cur_sel:
        list.append(row)
    print(l)

def select_name():
    cur_sel = cur.execute(f"SELECT * FROM Mitarbeiter")
    records = cur_sel.fetchall()

    string_rec = ''
    for record in records:

        string_rec += str(record[0]) + " " + str(record[1]) + "\n"

    print(string_rec)

    #for row in cur_sel:
    #    print(*row)

def insert():
    anfrage = f"INSERT INTO Argen (Name, Artikel, Firma, Menge) " \
              f"VALUES ('{input('Name ')}', '{input('Artikel ')}', '{input('Firma ')}', {int(input('Menge '))})"
    cur.execute(anfrage)
    conn.commit()

select_name()

"""
import pyodbc as odbc

print(en1)
conn = odbc.connect("Driver={SQL Server};"
                    "Server=NB-DBO-01\SQLEXPRESS;"
                    "Database=ARGEN;"
                    "Trusted_Connection=yes;")
cur = conn.cursor()

class Mitarbeiter:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def write_name(self):
        cur.execute(f"INSERT INTO Mitarbeiter (Name, Vorname) VALUES ('{self.name}', '{self.surname}')")
        conn.commit()

    def row_delete(self):
        cur.execute(f"DELETE FROM Mitarbeiter WHERE Name='{input()}'")
        conn.commit()

start = Mitarbeiter()
print(start.name, start.surname)
"""