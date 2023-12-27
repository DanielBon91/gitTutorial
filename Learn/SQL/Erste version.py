import tkinter as ttk
import customtkinter
import pyodbc as odbc
from datetime import date

from PIL import Image

date_today = date.today().strftime("%d.%m.%Y")

# Verbindung zum Database
connection = odbc.connect("Driver={SQL Server};"
                    "Server=NB-DBO-01\SQLEXPRESS;"
                    "Database=ARGEN;"
                    "Trusted_Connection=yes;")

cursor_position = connection.cursor()

image_directory = customtkinter.CTkImage(dark_image=Image.open(
    r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//ArgenLogo_Weiss.png"),
    light_image=Image.open(
        r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//ArgenLogo_Schwarz.png"),
    size=(300, 50))

customtkinter.set_appearance_mode("Dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1300x1000+600+150")
app.title("Argen Invertory")
app.grid_columnconfigure(1, weight=0)
app.grid_rowconfigure(0, weight=1)

#+
def vorwahl_vorname(choise):
    # combobox Nachname
    global combo_nachname
    cur_sel = cursor_position.execute(f"SELECT Nachname FROM Mitarbeiter WHERE Vorname = '{choise}' GROUP BY Nachname ")
    list_nachname = []
    for row in cur_sel:
        list_nachname.append(*row)
    combo_nachname = customtkinter.CTkComboBox(uebergabe_frame, values=list_nachname, width=180,
                                               font=customtkinter.CTkFont(size=19),
                                               dropdown_font=customtkinter.CTkFont(size=19))
    combo_nachname.grid(row=0, column=3, pady=(45, 15), sticky="w")
    uebergabe_label_nachname.grid(row=0, column=2, pady=(45, 15), padx=(25, 15), sticky="w")


def uebergabe_func():
    global uebergabe_enter_vorname, \
        uebergabe_enter_nachname, uebergabe_enter_artikel, uebergabe_enter_hersteller, \
        uebergabe_enter_model, uebergabe_enter_seriennumer, uebergabe_enter_bemerkung, \
        uebergabe_enter_datum, uebergabe_frame, combo_name, uebergabe_label_nachname

    navi_button_1.configure(fg_color=("gray75", "gray25"))
    navi_button_2.configure(fg_color="transparent")
    navi_button_3.configure(fg_color="transparent")
    navi_button_4.configure(fg_color="transparent")
    #+
    uebergabe_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    uebergabe_frame.grid_columnconfigure(0, weight=1)
    uebergabe_frame.grid(row=0, column=1, sticky="nsew")
    uebergabe_label_vorname = customtkinter.CTkLabel(uebergabe_frame, text="Vorname",
                                                     font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_vorname.grid(row=0, column=0, pady=(45, 15), padx=(190, 15), sticky="w")
    uebergabe_label_nachname = customtkinter.CTkLabel(uebergabe_frame, text="Nachname",
                                                      font=customtkinter.CTkFont(size=19, weight="bold"))

    uebergabe_label_artikel = customtkinter.CTkLabel(uebergabe_frame, text="Artikel",
                                                     font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_artikel.grid(row=2, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
    uebergabe_label_hersteller = customtkinter.CTkLabel(uebergabe_frame, text="Hersteller",
                                                        font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_hersteller.grid(row=3, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
    uebergabe_label_model = customtkinter.CTkLabel(uebergabe_frame, text="Model",
                                                   font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_model.grid(row=4, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
    uebergabe_label_seriennumer = customtkinter.CTkLabel(uebergabe_frame, text="Seriennumer",
                                                         font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_seriennumer.grid(row=5, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
    uebergabe_label_bemerkung = customtkinter.CTkLabel(uebergabe_frame, text="Bemerkung",
                                                       font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_bemerkung.grid(row=6, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
    uebergabe_label_datum = customtkinter.CTkLabel(uebergabe_frame, text="Datum",
                                                   font=customtkinter.CTkFont(size=19, weight="bold"))
    uebergabe_label_datum.grid(row=7, column=0, pady=(15, 15), padx=(190, 15), sticky="w")

    # combobox Vorname+
    cur_sel = cursor_position.execute(f"SELECT Vorname FROM Mitarbeiter WHERE Vorname IS NOT NULL GROUP BY Vorname")
    list_vorname = []

    for row in cur_sel:
        list_vorname.append(*row)

    combo_name = customtkinter.CTkComboBox(uebergabe_frame, values=list_vorname, width=180, command=vorwahl_vorname,
                                           font=customtkinter.CTkFont(size=19),
                                           dropdown_font=customtkinter.CTkFont(size=19))
    combo_name.set("Bitte auswählen")
    combo_name.grid(row=0, column=1, pady=(35, 5), padx=(10, 0), sticky="w")

    # uebergabe_enter_vorname = customtkinter.CTkEntry(uebergabe_frame, width=450, font=customtkinter.CTkFont(size=19))
    # uebergabe_enter_vorname.grid(row=0, column=2, pady=(35, 5), padx=(15, 15), sticky="w")
    # uebergabe_enter_nachname = customtkinter.CTkEntry(uebergabe_frame, width=450, font=customtkinter.CTkFont(size=19))
    # uebergabe_enter_nachname.grid(row=1, column=2, pady=(5, 5), padx=(15, 15), sticky="w")
    uebergabe_enter_artikel = customtkinter.CTkEntry(uebergabe_frame, width=535, font=customtkinter.CTkFont(size=19))
    uebergabe_enter_artikel.grid(row=2, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
    uebergabe_enter_hersteller = customtkinter.CTkEntry(uebergabe_frame, width=535, font=customtkinter.CTkFont(size=19))
    uebergabe_enter_hersteller.grid(row=3, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
    uebergabe_enter_model = customtkinter.CTkEntry(uebergabe_frame, width=535, font=customtkinter.CTkFont(size=19))
    uebergabe_enter_model.grid(row=4, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
    uebergabe_enter_seriennumer = customtkinter.CTkEntry(uebergabe_frame, width=535,
                                                         font=customtkinter.CTkFont(size=19))
    uebergabe_enter_seriennumer.grid(row=5, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
    uebergabe_enter_bemerkung = customtkinter.CTkEntry(uebergabe_frame, width=535, font=customtkinter.CTkFont(size=19))
    uebergabe_enter_bemerkung.grid(row=6, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
    uebergabe_enter_datum = customtkinter.CTkEntry(uebergabe_frame, width=535, font=customtkinter.CTkFont(size=19))
    uebergabe_enter_datum.insert("0", date_today)
    uebergabe_enter_datum.grid(row=7, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")

    uebergabe_button_confirm = customtkinter.CTkButton(uebergabe_frame, text="Confirm", height=65, width=265,
                                                       font=customtkinter.CTkFont(size=24),
                                                       command=lambda: writing_data_uebergabe(
                                                           combo_name.get(),
                                                           combo_nachname.get(),
                                                           uebergabe_enter_artikel.get(),
                                                           uebergabe_enter_hersteller.get(),
                                                           uebergabe_enter_model.get(),
                                                           uebergabe_enter_seriennumer.get(),
                                                           uebergabe_enter_bemerkung.get(),
                                                           uebergabe_enter_datum.get()))

    uebergabe_button_confirm.grid(row=8, column=1, columnspan=3, pady=(55, 15))
    global label_confirm
    label_confirm = customtkinter.CTkLabel(uebergabe_frame, text="✓", font=customtkinter.CTkFont(size=44))


def vorwahl(choise):
    global choise_name
    choise_name = choise


def writing_data_uebergabe(vorname, nachname, artikel, hersteller, model, seriennumer, bemerkung, datum):
    combo_name.set("")
    combo_nachname.set("")
    uebergabe_enter_artikel.delete(0, "end")
    uebergabe_enter_hersteller.delete(0, "end")
    uebergabe_enter_model.delete(0, "end")
    uebergabe_enter_seriennumer.delete(0, "end")
    uebergabe_enter_bemerkung.delete(0, "end")
    uebergabe_enter_datum.delete(0, "end")

    command_string = f"INSERT INTO Mitarbeiter (Vorname, Nachname, Artikel, Hersteller, Model, Seriennumer, Bemerkung, Datum) VALUES ('{vorname}','{nachname}','{artikel}','{hersteller}','{model}','{seriennumer}','{bemerkung}','{datum}')"
    cursor_position.execute(command_string)
    connection.commit()

    label_confirm.grid(row=8, column=3, pady=(35, 0))


def writing_data_waren(artikel, hersteller, model, seriennumer, bemerkung, datum):
    waren_enter_artikel.delete(0, "end")
    waren_enter_hersteller.delete(0, "end")
    waren_enter_model.delete(0, "end")
    waren_enter_seriennumer.delete(0, "end")
    waren_enter_bemerkung.delete(0, "end")
    waren_enter_datum.delete(0, "end")

    command_string = f"INSERT INTO Artikel (Artikel, Hersteller, Model, Seriennumer, Bemerkung, Datum) VALUES ('{artikel}','{hersteller}','{model}','{seriennumer}','{bemerkung}','{datum}')"
    cursor_position.execute(command_string)
    connection.commit()

#+
def change_mode(mode):
    customtkinter.set_appearance_mode(mode)


def waren():
    global waren_enter_artikel, waren_enter_hersteller, waren_enter_model, waren_enter_seriennumer, waren_enter_bemerkung, waren_enter_datum

    navi_button_1.configure(fg_color="transparent")
    navi_button_2.configure(fg_color=("gray75", "gray25"))
    navi_button_3.configure(fg_color="transparent")
    navi_button_4.configure(fg_color="transparent")

    waren_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    waren_frame.grid_columnconfigure(1, weight=0)
    waren_frame.grid(row=0, column=1, sticky="nsew")

    waren_artikel = customtkinter.CTkLabel(waren_frame, text="Artikel")
    waren_artikel.grid(row=2, column=1, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_hersteller = customtkinter.CTkLabel(waren_frame, text="Hersteller")
    waren_hersteller.grid(row=3, column=1, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_model = customtkinter.CTkLabel(waren_frame, text="Model")
    waren_model.grid(row=4, column=1, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_seriennumer = customtkinter.CTkLabel(waren_frame, text="Seriennumer")
    waren_seriennumer.grid(row=5, column=1, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_bemerkung = customtkinter.CTkLabel(waren_frame, text="Bemerkung")
    waren_bemerkung.grid(row=6, column=1, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_datum = customtkinter.CTkLabel(waren_frame, text="Datum")
    waren_datum.grid(row=7, column=1, pady=(5, 5), padx=(15, 15), sticky="w")

    waren_enter_artikel = customtkinter.CTkEntry(waren_frame, width=350)
    waren_enter_artikel.grid(row=2, column=2, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_enter_hersteller = customtkinter.CTkEntry(waren_frame, width=350)
    waren_enter_hersteller.grid(row=3, column=2, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_enter_model = customtkinter.CTkEntry(waren_frame, width=350)
    waren_enter_model.grid(row=4, column=2, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_enter_seriennumer = customtkinter.CTkEntry(waren_frame, width=350)
    waren_enter_seriennumer.grid(row=5, column=2, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_enter_bemerkung = customtkinter.CTkEntry(waren_frame, width=350)
    waren_enter_bemerkung.grid(row=6, column=2, pady=(5, 5), padx=(15, 15), sticky="w")
    waren_enter_datum = customtkinter.CTkEntry(waren_frame, width=350)
    waren_enter_datum.insert("0", date_today)
    waren_enter_datum.configure(state="disabled")
    waren_enter_datum.grid(row=7, column=2, pady=(5, 5), padx=(15, 15), sticky="w")

    waren_button_confirm = customtkinter.CTkButton(waren_frame, text="Confirm", height=65, width=265,
                                                   command=lambda: writing_data_waren(
                                                       waren_enter_artikel.get(),
                                                       waren_enter_hersteller.get(),
                                                       waren_enter_model.get(),
                                                       waren_enter_seriennumer.get(),
                                                       waren_enter_bemerkung.get(),
                                                       waren_enter_datum.get()))

    waren_button_confirm.grid(row=8, column=2, pady=(55, 15))




# Navi frame +
navi_frame = customtkinter.CTkFrame(app, corner_radius=0)
navi_frame.grid(row=0, column=0, sticky="nsew")
navi_frame.grid_rowconfigure(5, weight=1)

image_label = customtkinter.CTkLabel(navi_frame, text="", image=image_directory)
image_label.grid(row=0, column=0, padx=15, pady=(55, 25))

def liste_button():

    navi_button_1.configure(fg_color="transparent")
    navi_button_2.configure(fg_color="transparent")
    navi_button_3.configure(fg_color=("gray75", "gray25"))
    navi_button_4.configure(fg_color="transparent")

    liste_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="transparent")
    liste_frame.grid(row=0, column=1, sticky="nsew")
    liste_frame.grid_columnconfigure(0, weight=1)

    tab_view = customtkinter.CTkTabview(liste_frame)
    tab_view.grid(row=0, column=0, padx=(60, 0), sticky="nsew")
    tab_view.add("Abgegebene")
    tab_view.add("Lager")
    tab_view.tab("Abgegebene").grid_columnconfigure(0, weight=0)

    cur_sel = cursor_position.execute(f"SELECT Vorname, Nachname, Artikel, Hersteller, Model, Seriennumer, Datum FROM Mitarbeiter")
    records = cur_sel.fetchall()

    string_rec = ""
    for record in records:
        string_rec += str(record[0]) + " " + str(record[1]) + " " + str(record[2])+" " + str(record[3]) + " " + str(record[4])+" " + str(record[5]) + " " + str(record[6]) + "\n\n"
        string_rec.lstrip()

    list_label = customtkinter.CTkLabel(tab_view.tab("Abgegebene"), text=string_rec, justify=ttk.LEFT, font=customtkinter.CTkFont(size=15))
    list_label.grid(row=0, column=0, padx=20, pady=35)

    lager_string = ""

    for record in records:
        lager_string += str(record[2]) + " " + str(record[3]) + " " + str(
            record[4]) + " " + str(record[5]) + " " + str(record[6]) + "\n\n"

    list_label_2 = customtkinter.CTkLabel(tab_view.tab("Lager"), text=lager_string,
                                          justify=ttk.LEFT,
                                        font=customtkinter.CTkFont(size=15))
    list_label_2.grid(row=0, column=0, padx=20, pady=35)






def mitarbeiter():
    navi_button_1.configure(fg_color="transparent")
    navi_button_2.configure(fg_color="transparent")
    navi_button_3.configure(fg_color="transparent")
    navi_button_4.configure(fg_color=("gray75", "gray25"))




#+

navi_button_1 = customtkinter.CTkButton(navi_frame, text="Übergabeprotokoll", text_color=("gray10", "gray90"),
                                        height=120, width=250, fg_color="transparent", hover_color=("gray70", "gray30"),
                                        corner_radius=0,
                                        command=uebergabe_func, font=customtkinter.CTkFont(size=24))
navi_button_1.grid(row=1, column=0, pady=(35, 0), sticky="ew")

navi_button_2 = customtkinter.CTkButton(navi_frame, text="Warenannahme", text_color=("gray10", "gray90"), height=120,
                                        fg_color="transparent", hover_color=("gray70", "gray30"), corner_radius=0,
                                        border_spacing=10,
                                        command=waren, font=customtkinter.CTkFont(size=24))
navi_button_2.grid(row=2, column=0, sticky="ew")

navi_button_3 = customtkinter.CTkButton(navi_frame, text="Liste", height=120, fg_color="transparent",
                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        corner_radius=0, command=liste_button,
                                        font=customtkinter.CTkFont(size=24))
navi_button_3.grid(row=3, column=0, sticky="ew")

navi_button_4 = customtkinter.CTkButton(navi_frame, text="Mitarbeiter", text_color=("gray10", "gray90"),
                                        corner_radius=0, height=120, fg_color="transparent",
                                        hover_color=("gray70", "gray30"), command=mitarbeiter,
                                        font=customtkinter.CTkFont(size=24))
navi_button_4.grid(row=4, column=0, sticky="ew")

change_mode = customtkinter.CTkOptionMenu(navi_frame, values=["Dark", "Light"], command=change_mode)
change_mode.grid(row=6, sticky="s", pady=15)

uebergabe_func()

app.mainloop()
