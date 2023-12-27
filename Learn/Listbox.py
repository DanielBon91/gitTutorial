from tkinter import ttk
from tkinter import *
import pyodbc as odbc

connection = odbc.connect("Driver={SQL Server};"
                          "Server=NB-DBO-01\SQLEXPRESS;"
                          "Database=ARGEN;"
                          "Trusted_Connection=yes;")

cursor_position = connection.cursor()
cursor_position.execute("SELECT Vorname, Nachname, Artikel, Hersteller, Seriennumer, Datum FROM Mitarbeiter WHERE Vorname IS NOT NULL")


root = Tk()
root.title("CODEMY")
root.geometry("1500x600")

my_tree = ttk.Treeview(root)

my_tree ['columns'] = ("Vorname", "Name", "Artikel", "Model", "Sn", "Datum")

my_tree.column("#0", width=1, minwidth=1)
my_tree.column("Vorname", anchor="w", width=155)
my_tree.column("Name", anchor="w", minwidth=10)
my_tree.column("Artikel", anchor="w", minwidth=15)
my_tree.column("Model", anchor="w", minwidth=15)
my_tree.column("Sn", anchor="w", minwidth=15)
my_tree.column("Datum", anchor="w", minwidth=15)


my_tree.heading("#0", text="")
my_tree.heading("Vorname", text="Vorname")
my_tree.heading("Name", text="Name")
my_tree.heading("Artikel", text="Artikel")
my_tree.heading("Model", text="Model")
my_tree.heading("Sn", text="SN")
my_tree.heading("Datum", text="Datum")

c = 0
for i in cursor_position.fetchall():
    my_tree.insert(parent="", index="end", iid=c, text="", values=(i[0],i[1],i[2],i[3],i[4],i[5]))
    c +=1

my_tree.pack(pady=20)
def select():
    sel = my_tree.focus()
    values = my_tree.item(sel, 'values')
    vorname = values[0]
    print(vorname)

btn = Button(text="push", command=select).pack()


root.mainloop()