import os
import subprocess
from tkinter import messagebox, ttk
from tkinter.ttk import Scrollbar, Style
from docxtpl import DocxTemplate

import customtkinter
import pyodbc as odbc
from datetime import date
from PIL import Image
import customtreeview as ctv

date_today = date.today().strftime("%d.%m.%Y")

# Verbindung zum Database
connection = odbc.connect("Driver={SQL Server};"
                          "Server=NB-DBO-01\SQLEXPRESS;"
                          "Database=ARGEN;"
                          "Trusted_Connection=yes;")

cursor_position = connection.cursor()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Argen IT Invertory")

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        x = (self.screen_width/2)-(1410/2)
        y = (self.screen_height/2)-(1200/2)
        self.geometry(f"{1410}x{1200}+{int(x)}+{int(y)}")

        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Create Navi frame
        self.navi_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navi_frame.grid(row=0, column=0, sticky="nsew")
        self.navi_frame.grid_rowconfigure(5, weight=1)

        # Create Image
        self.image_directory = customtkinter.CTkImage(dark_image=Image.open(
            r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//ArgenLogo_Weiss.png"),
            light_image=Image.open(
                r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//ArgenLogo_Schwarz.png"),
            size=(300, 50))
        self.image_label = customtkinter.CTkLabel(self.navi_frame, text="", image=self.image_directory)
        self.image_label.grid(row=0, column=0, padx=15, pady=(55, 25))

        self.image_access = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                              r"//pythonProject//Learn//SQL//test_images//access.png"),
                                                   size=(50, 50))

        self.image_error_confirm = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                                     r"//pythonProject//Learn//SQL//test_images//error.png"),
                                                          size=(50, 50))

        self.image_error_artikel = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                                     r"//pythonProject//Learn//SQL//test_images//error.png"),
                                                          size=(30, 30))

        self.image_warenannahme = customtkinter.CTkImage(dark_image=Image.open(
            r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//box_dark.png"),
            light_image=Image.open(
                r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//box_light.png"),
            size=(30, 30))

        self.image_warenuebergabe = customtkinter.CTkImage(dark_image=Image.open(
            r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//ubergabe_dark.png"),
            light_image=Image.open(
                r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//ubergabe_light.png"),
            size=(35, 35))

        self.image_liste = customtkinter.CTkImage(dark_image=Image.open(
            r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//list_dark.png"),
            light_image=Image.open(
                r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//list_light.png"),
            size=(30, 30))

        self.image_arbeiter = customtkinter.CTkImage(dark_image=Image.open(
            r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//arbeiter_dark.png"),
            light_image=Image.open(
                r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//test_images//arbeiter_light.png"),
            size=(30, 30))

        self.image_row = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                           r"//pythonProject//Learn//SQL//test_images//row.png"),
                                                size=(180, 180))

        self.image_plus = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                           r"//pythonProject//Learn//SQL//test_images//plus.png"),
                                                size=(35, 35))

        self.image_minus = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                            r"//pythonProject//Learn//SQL//test_images//minus.png"),
                                                 size=(35, 35))

        self.word = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//PycharmProjects"
                                                            r"//pythonProject//Learn//SQL//test_images//word.png"),
                                                 size=(35, 35))

        # Navigation frame button griding
        self.navi_button_1 = customtkinter.CTkButton(self.navi_frame, text="Warenannahme",
                                                     text_color=("gray10", "gray90"),
                                                     height=120, width=250, fg_color="transparent",
                                                     image=self.image_warenannahme,
                                                     hover_color=("gray70", "gray30"),
                                                     command=self.first_frame_navi_button,
                                                     corner_radius=0, font=customtkinter.CTkFont(size=24))
        self.navi_button_1.grid(row=1, column=0, pady=(35, 0), sticky="ew")

        self.navi_button_2 = customtkinter.CTkButton(self.navi_frame, text="Warenübergabe",
                                                     text_color=("gray10", "gray90"),
                                                     height=120, image=self.image_warenuebergabe,
                                                     fg_color="transparent", hover_color=("gray70", "gray30"),
                                                     corner_radius=0, command=self.second_frame_navi_button,
                                                     border_spacing=10, font=customtkinter.CTkFont(size=24))
        self.navi_button_2.grid(row=2, column=0, sticky="ew")

        self.navi_button_3 = customtkinter.CTkButton(self.navi_frame, text="Liste", height=120, fg_color="transparent",
                                                     text_color=("gray10", "gray90"), image=self.image_liste,
                                                     hover_color=("gray70", "gray30"),
                                                     corner_radius=0, command=self.three_frame_navi_button,
                                                     font=customtkinter.CTkFont(size=24))
        self.navi_button_3.grid(row=3, column=0, sticky="ew")

        self.navi_button_4 = customtkinter.CTkButton(self.navi_frame, text="Mitarbeiter",
                                                     text_color=("gray10", "gray90"), image=self.image_arbeiter,
                                                     corner_radius=0, height=120, fg_color="transparent",
                                                     hover_color=("gray70", "gray30"),
                                                     command=self.four_frame_navi_button,
                                                     font=customtkinter.CTkFont(size=24))
        self.navi_button_4.grid(row=4, column=0, sticky="ew")

        self.change_mode = customtkinter.CTkOptionMenu(self.navi_frame, values=["Dark", "Light"],
                                                       command=self.change_mode)
        self.change_mode.grid(row=6, sticky="s", pady=15)

        ############ FIRST FRAME ############

        self.first_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.first_frame.grid_columnconfigure(0, weight=1)

        # 1.Labels create
        self.first_frame_artikel_label = customtkinter.CTkLabel(self.first_frame, text="Artikel",
                                                                font=customtkinter.CTkFont(size=19, weight="bold"))
        self.first_frame_artikel_label.grid(row=2, column=0, pady=(150, 15), padx=(190, 15), sticky="w")
        self.first_frame_hersteller_label = customtkinter.CTkLabel(self.first_frame, text="Hersteller",
                                                                   font=customtkinter.CTkFont(size=19, weight="bold"))
        self.first_frame_hersteller_label.grid(row=3, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
        self.first_frame_model_label = customtkinter.CTkLabel(self.first_frame, text="Model",
                                                              font=customtkinter.CTkFont(size=19, weight="bold"))
        self.first_frame_model_label.grid(row=4, column=0, pady=(15, 15), padx=(190, 15), sticky="w")
        self.first_frame_sn_label = customtkinter.CTkLabel(self.first_frame, text="Seriennumer",
                                                           font=customtkinter.CTkFont(size=19, weight="bold"))
        self.first_frame_sn_label.grid(row=5, column=0, pady=(15, 15), padx=(190, 15), sticky="w")

        self.first_frame_datum_label = customtkinter.CTkLabel(self.first_frame, text="Datum",
                                                              font=customtkinter.CTkFont(size=19, weight="bold"))
        self.first_frame_datum_label.grid(row=6, column=0, pady=(15, 15), padx=(190, 15), sticky="w")

        self.first_frame_bemerkung_label = customtkinter.CTkLabel(self.first_frame, text="Bemerkung",
                                                                  font=customtkinter.CTkFont(size=19, weight="bold"))
        self.first_frame_bemerkung_label.grid(row=7, column=0, pady=(15, 15), padx=(190, 15), sticky="w")

        self.label_access = customtkinter.CTkLabel(self.first_frame, text="", image=self.image_access,
                                                   font=customtkinter.CTkFont(size=44))
        self.label_error_artikel = customtkinter.CTkLabel(self.first_frame, text="", image=self.image_error_artikel)
        self.label_error_confirm = customtkinter.CTkLabel(self.first_frame, text="", image=self.image_error_confirm)

        # 1.Entry boxes create
        self.first_frame_artikel_entry = customtkinter.CTkEntry(self.first_frame,
                                                                width=560,
                                                                font=customtkinter.CTkFont(size=19))
        self.first_frame_artikel_entry.grid(row=2, column=1, columnspan=3, pady=(150, 5), padx=(10, 15), sticky="w")
        self.first_frame_artikel_entry.bind("<FocusOut>", self.change_artikel)
        self.first_frame_hersteller_entry = customtkinter.CTkEntry(self.first_frame, width=560,
                                                                   font=customtkinter.CTkFont(size=19))
        self.first_frame_hersteller_entry.grid(row=3, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
        self.first_frame_model_entry = customtkinter.CTkEntry(self.first_frame, width=560,
                                                              font=customtkinter.CTkFont(size=19))
        self.first_frame_model_entry.grid(row=4, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")
        self.first_frame_sn_entry = customtkinter.CTkEntry(self.first_frame, width=560,
                                                           font=customtkinter.CTkFont(size=19))
        self.first_frame_sn_entry.grid(row=5, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")

        self.first_frame_datum_entry = customtkinter.CTkEntry(self.first_frame, width=560,
                                                              font=customtkinter.CTkFont(size=19))
        self.first_frame_datum_entry.insert("0", date_today)
        self.first_frame_datum_entry.grid(row=6, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")

        self.first_frame_bemerkung_entry = customtkinter.CTkTextbox(self.first_frame, width=560, height=100,
                                                                    font=customtkinter.CTkFont(size=19))
        self.first_frame_bemerkung_entry.grid(row=7, column=1, columnspan=3, pady=(5, 5), padx=(10, 15), sticky="w")

        self.first_frame_button_confirm = customtkinter.CTkButton(self.first_frame, text="Confirm",
                                                                  corner_radius=10, height=75, width=265,
                                                                  font=customtkinter.CTkFont(size=34),
                                                                  command=self.writing_data_frame_1)

        # 1.Buttons create
        self.first_frame_button_confirm.grid(row=8, column=1, pady=(55, 15), padx=(115, 0))

        self.first_frame_button_clear = customtkinter.CTkButton(self.first_frame, text="Clear all",
                                                                corner_radius=5,
                                                                height=25, width=145,
                                                                fg_color="gray", hover_color="#C52233",
                                                                font=customtkinter.CTkFont(size=14),
                                                                command=self.first_frame_clear_all)
        self.first_frame_button_clear.grid(row=9, column=1, padx=(115, 0), pady=(55, 15))

        ############ SECOND FRAME ############

        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(1, weight=1)

        self.treeview_vorrat_frame_2 = ctv.CustomTreeView(self.second_frame, height=24, columns=(
            "column1", "column2", "column3", "column4", "column5"))

        self.tree_scroll_vorrat_frame_2 = customtkinter.CTkScrollbar(self.second_frame,
                                                      command=self.treeview_vorrat_frame_2.yview)
        self.tree_scroll_vorrat_frame_2.grid(row=1, column=1, sticky="nse", pady=(35, 0))

        self.treeview_vorrat_frame_2.configure(yscrollcommand=self.tree_scroll_vorrat_frame_2.set)

        self.treeview_vorrat_frame_2.heading("#0", text="Item")
        self.treeview_vorrat_frame_2.heading("column1", text="Artikel", command=lambda: self.sort_function("column1", self.treeview_vorrat_frame_2, False))
        self.treeview_vorrat_frame_2.heading("column2", text="Hersteller", command=lambda: self.sort_function("column2", self.treeview_vorrat_frame_2, False))
        self.treeview_vorrat_frame_2.heading("column3", text="Model", command=lambda: self.sort_function("column3", self.treeview_vorrat_frame_2, False))
        self.treeview_vorrat_frame_2.heading("column4", text="Seriennumer", command=lambda: self.sort_function("column4", self.treeview_vorrat_frame_2, False))
        self.treeview_vorrat_frame_2.heading("column5", text="Bemerkung", command=lambda: self.sort_function("column5", self.treeview_vorrat_frame_2, False))

        self.treeview_vorrat_frame_2.column("#0", width=0, minwidth=0)
        self.treeview_vorrat_frame_2.column("column1", width=150)
        self.treeview_vorrat_frame_2.column("column2", width=110)
        self.treeview_vorrat_frame_2.column("column3")
        self.treeview_vorrat_frame_2.column("column4", width=170)
        self.treeview_vorrat_frame_2.column("column5", width=190)

        self.sorted_treeview_vorrat_label_2 = customtkinter.CTkLabel(self.second_frame, text="Sorted by...",
                                                                     font=customtkinter.CTkFont(size=19, weight="bold"))

        self.sorted_treeview_vorrat_option_2 = customtkinter.CTkOptionMenu(self.second_frame,
                                                                           values=["Artikel", "Hersteller", "Model",
                                                                                   "Seriennumer", "Bemerkung"],
                                                                           command=self.sorted_by_second_frame,
                                                                           font=customtkinter.CTkFont(size=17,
                                                                                                      weight="bold"),
                                                                           dropdown_font=customtkinter.CTkFont(size=17,
                                                                                                               weight="bold"))

        #self.sorted_treeview_vorrat_label_2.grid(row=0, column=0, sticky="w", padx=(145,0), pady=10, columnspan=2)
        #self.sorted_treeview_vorrat_option_2.grid(row=0, column=0, sticky="w", padx=260, columnspan=2)


        self.second_frame_movedown_button = customtkinter.CTkButton(self.second_frame, text="", fg_color="#399E5A",
                                                            hover_color="#328E3D", command=self.plus_funktion, image=self.image_plus, height=50)
        self.second_frame_movedown_button.grid(row=3, column=0, pady=30, padx=120)

        self.second_frame_moveup_button = customtkinter.CTkButton(self.second_frame, text="", fg_color="#C52233",
                                                                  hover_color="#F31B31", command=self.minus_function, image=self.image_minus, height=50)
        self.second_frame_moveup_button.grid(row=3, column=1, pady=30)

        self.treeview_leer_frame_2 = ctv.CustomTreeView(self.second_frame, height=10, columns=(
            "column1", "column2", "column3", "column4", "column5"))


        self.treeview_leer_frame_2.heading("#0", text="Item")
        self.treeview_leer_frame_2.heading("column1", text="Artikel", command=lambda: self.sort_function("column1", self.treeview_leer_frame_2, False))
        self.treeview_leer_frame_2.heading("column2", text="Hersteller", command=lambda: self.sort_function("column2", self.treeview_leer_frame_2, False))
        self.treeview_leer_frame_2.heading("column3", text="Model", command=lambda: self.sort_function("column3", self.treeview_leer_frame_2, False))
        self.treeview_leer_frame_2.heading("column4", text="Seriennumer", command=lambda: self.sort_function("column4", self.treeview_leer_frame_2, False))
        self.treeview_leer_frame_2.heading("column5", text="Bemerkung", command=lambda: self.sort_function("column5", self.treeview_leer_frame_2, False))

        self.treeview_leer_frame_2.column("#0", width=0, minwidth=0)
        self.treeview_leer_frame_2.column("column1", width=150)
        self.treeview_leer_frame_2.column("column2", width=110)
        self.treeview_leer_frame_2.column("column3")
        self.treeview_leer_frame_2.column("column4", width=170)
        self.treeview_leer_frame_2.column("column5", width=190)

        self.treeview_leer_frame_2.grid(row=4, column=0, padx=(140, 0),columnspan=2)

        self.zuweisen_button = customtkinter.CTkButton(self.second_frame, text="Die Waren übergebe an...",
                                                       width=350, height=80,
                                                       command=self.uebergabe_button,
                                                       font=customtkinter.CTkFont(size=25))
        self.zuweisen_button.grid(row=5, column=0, columnspan=2, pady=15, padx=180)

        #self.current_select_nachname = cursor_position.execute(f"SELECT Nachname FROM Mitarbeiter "
        #                                                       f"WHERE Vorname = '{name}' GROUP BY Nachname ")
        #self.list_nachname = []
        #for nachname in self.current_select_nachname:
        #    self.list_nachname.append(*nachname)
#
        #self.second_frame_nachname_box = customtkinter.CTkOptionMenu(self.second_frame, values=self.list_nachname,
        #                                                             width=180,
        #                                                             font=customtkinter.CTkFont(size=19),
        #                                                             dropdown_font=customtkinter.CTkFont(size=19))
        #self.second_frame_nachname_box.set("Bitte auswählen")
        #self.second_frame_nachname_box.grid(row=0, column=3, pady=(45, 15), padx=(10, 0), sticky="w")
        #self.second_frame_nachname_label.grid(row=0, column=2, pady=(45, 15), padx=(25, 15), sticky="w")






        ############ THIRD FRAME ############

        self.three_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.three_frame.grid_columnconfigure(5, weight=1)

        self.three_frame_lager_button = customtkinter.CTkButton(self.three_frame, text="Lager", width=350,
                                                                height=50, corner_radius=0,
                                                                font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                command=self.table_1)
        self.three_frame_invent_button = customtkinter.CTkButton(self.three_frame, text="Inventarisierung",
                                                                 width=350, height=50, corner_radius=0,
                                                                 font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                 command=self.table_2)
        self.three_frame_mitarbeter_button = customtkinter.CTkButton(self.three_frame, text="Mitarbeiter",
                                                                     width=350, height=50, corner_radius=0,
                                                                     font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                     command=self.table_3)
        self.three_frame_lager_button.grid(row=0, column=0, pady=(10, 0), padx=(15, 0))
        self.three_frame_invent_button.grid(row=0, column=1, pady=(10, 0))
        self.three_frame_mitarbeter_button.grid(row=0, column=2, pady=(10, 0))

        ### Table 1 Create ##
        self.three_frame_table1_frame = customtkinter.CTkFrame(self.three_frame, fg_color="transparent")
        self.three_frame_table1_frame.grid_columnconfigure(0, weight=0)

        self.treeview_vorrat = ctv.CustomTreeView(self.three_frame_table1_frame, height=35, columns=(
            "column1", "column2", "column3", "column4", "column5"))

        self.tree_scroll_vorrat = customtkinter.CTkScrollbar(self.three_frame_table1_frame,
                                                      command=self.treeview_vorrat.yview)
        self.tree_scroll_vorrat.grid(row=2, column=7, sticky="nse")

        self.treeview_vorrat.configure(yscrollcommand=self.tree_scroll_vorrat.set)

        self.treeview_vorrat.heading("#0", text="Item")
        self.treeview_vorrat.heading("column1", text="Artikel", command=lambda: self.sort_function("column1", self.treeview_vorrat, False))
        self.treeview_vorrat.heading("column2", text="Hersteller", command=lambda: self.sort_function("column2", self.treeview_vorrat, False))
        self.treeview_vorrat.heading("column3", text="Model", command=lambda: self.sort_function("column3", self.treeview_vorrat, False))
        self.treeview_vorrat.heading("column4", text="Seriennumer", command=lambda: self.sort_function("column4", self.treeview_vorrat, False))
        self.treeview_vorrat.heading("column5", text="Bemerkung", command=lambda: self.sort_function("column5", self.treeview_vorrat, False))

        self.treeview_vorrat.column("#0", width=0, minwidth=0)
        self.treeview_vorrat.column("column1", width=150)
        self.treeview_vorrat.column("column2", width=110)
        self.treeview_vorrat.column("column3")
        self.treeview_vorrat.column("column4", width=170)
        self.treeview_vorrat.column("column5", width=190)

        self.sorted_treeview_vorrat_label_2 = customtkinter.CTkLabel(self.three_frame_table1_frame, text="Sorted by...",
                                                                     font=customtkinter.CTkFont(size=19, weight="bold"))
        self.sorted_treeview_vorrat_label_2.grid(row=1, column=0, padx=(15, 7), pady=20, sticky="w")
        self.sorted_treeview_vorrat_option_2 = customtkinter.CTkOptionMenu(self.three_frame_table1_frame,
                                                                           values=["Artikel", "Hersteller", "Model",
                                                                                 "Seriennumer", "Bemerkung"],
                                                                           command=self.sorted_by_lager,
                                                                           font=customtkinter.CTkFont(size=17,
                                                                                                    weight="bold"),
                                                                           dropdown_font=customtkinter.CTkFont(size=17,
                                                                                                             weight="bold"))
        self.sorted_treeview_vorrat_option_2.grid(row=1, column=0, padx=(135, 0), pady=20, sticky="w")

        self.treeview_vorrat.grid(row=2, column=0, padx=(15, 0), columnspan=8)
        #self.sorted_by_lager("Artikel")

        self.treeview_vorrat.bind("<Double-1>", self.clicker_table_1)

        ### Table 2 Create ##
        self.three_frame_table2_frame = customtkinter.CTkFrame(self.three_frame, fg_color="transparent")
        self.three_frame_table2_frame.grid_columnconfigure(0, weight=0)

        self.treeview_invent = ctv.CustomTreeView(self.three_frame_table2_frame, height=35, columns=(
            "column1", "column2", "column3", "column4", "column5", "column6", "column7"))

        self.tree_scroll_invent = customtkinter.CTkScrollbar(self.three_frame_table2_frame,
                                                      command=self.treeview_invent.yview)
        self.tree_scroll_invent.grid(row=2, column=7, sticky="nse")

        self.treeview_invent.configure(yscrollcommand=self.tree_scroll_invent.set)

        self.treeview_invent.heading("#0", text="Item")
        self.treeview_invent.heading("column1", text="Vorname", command=lambda: self.sort_function("column1", self.treeview_invent, False))
        self.treeview_invent.heading("column2", text="Nachname", command=lambda: self.sort_function("column2", self.treeview_invent, False))
        self.treeview_invent.heading("column3", text="Artikel", command=lambda: self.sort_function("column3", self.treeview_invent, False))
        self.treeview_invent.heading("column4", text="Hersteller", command=lambda: self.sort_function("column4", self.treeview_invent, False))
        self.treeview_invent.heading("column5", text="Model", command=lambda: self.sort_function("column5", self.treeview_invent, False))
        self.treeview_invent.heading("column6", text="Seriennumer", command=lambda: self.sort_function("column6", self.treeview_invent, False))
        self.treeview_invent.heading("column7", text="Bemerkung", command=lambda: self.sort_function("column7", self.treeview_invent, False))

        self.treeview_invent.column("#0", width=0, minwidth=0)
        self.treeview_invent.column("column1", width=110)
        self.treeview_invent.column("column2", width=110)
        self.treeview_invent.column("column3", width=145)
        self.treeview_invent.column("column4", width=110)
        self.treeview_invent.column("column5")
        self.treeview_invent.column("column6", width=169)
        self.treeview_invent.column("column7", width=190)

        self.sorted_treeview_invent_label = customtkinter.CTkLabel(self.three_frame_table2_frame, text="Sorted by...",
                                                                   font=customtkinter.CTkFont(size=19, weight="bold"))
        self.sorted_treeview_invent_label.grid(row=1, column=0, padx=(15, 7), pady=20, sticky="w")
        self.sorted_treeview_invent_option = customtkinter.CTkOptionMenu(self.three_frame_table2_frame,
                                                                         values=["Vorname", "Nachname", "Artikel",
                                                                                 "Hersteller", "Model", "Seriennumer",
                                                                                 "Bemerkung"],
                                                                         command=self.sorted_by_invertar,
                                                                         font=customtkinter.CTkFont(size=17,
                                                                                                    weight="bold"),
                                                                         dropdown_font=customtkinter.CTkFont(size=17,
                                                                                                             weight="bold"))
        self.sorted_treeview_invent_option.grid(row=1, column=0, padx=(135, 0), pady=20, sticky="w")
        self.treeview_invent.grid(row=2, column=0, padx=(15, 0), columnspan=8)
        self.sorted_by_invertar("Vorname")

        self.treeview_invent.bind("<Double-1>", self.clicker_table_2)

        self.rueckgabe_button = customtkinter.CTkButton(self.three_frame_table2_frame, width=240, height=60,
                                                        text="Rückgabe machen", fg_color="#328E3D", hover_color="#399E5A",
                                                        font=customtkinter.CTkFont(size=21, weight="bold"),
                                                        command=self.rueckgabe).grid(row=3, column=0, padx=15, pady=25)



        ### Table 3 Create ###

        self.three_frame_table3_frame = customtkinter.CTkFrame(self.three_frame, fg_color="transparent")
        self.three_frame_table3_frame.grid_columnconfigure(0, weight=0)

        self.style_treeview_style = Style()
        self.style_treeview_style.configure("Treeview", rowheight=25)

        self.treeview_struktur = ctv.CustomTreeView(self.three_frame_table3_frame, height=35, columns=(
            "column1", "column2", "column3", "column4"))

        self.tree_scroll = customtkinter.CTkScrollbar(self.three_frame_table3_frame, command=self.treeview_struktur.yview)
        self.tree_scroll.grid(row=2, column=7, sticky="nse")

        self.treeview_struktur.configure(yscrollcommand=self.tree_scroll.set)

        self.treeview_struktur.heading("#0", text="Item2")
        self.treeview_struktur.heading("column1", text="Vorname", command=lambda: self.sort_function("column1", self.treeview_struktur, False))
        self.treeview_struktur.heading("column2", text="Nachname", command=lambda: self.sort_function("column2", self.treeview_struktur, False))
        self.treeview_struktur.heading("column3", text="Abteilung", command=lambda: self.sort_function("column3", self.treeview_struktur, False))
        self.treeview_struktur.heading("column4", text="Vorgesetzer", command=lambda: self.sort_function("column4", self.treeview_struktur, False))

        self.treeview_struktur.column("#0", width=0, minwidth=0)
        self.treeview_struktur.column("column1", width=150)
        self.treeview_struktur.column("column2", width=150)
        self.treeview_struktur.column("column3", width=150)
        self.treeview_struktur.column("column4", width=150)

        self.sorted_treeview_mitareiter_label = customtkinter.CTkLabel(self.three_frame_table3_frame,
                                                                       text="Sorted by...",
                                                                       font=customtkinter.CTkFont(size=19,
                                                                                                  weight="bold"))
        self.sorted_treeview_mitareiter_label.grid(row=1, column=0, padx=(15, 7), pady=20, sticky="w")
        self.sorted_treeview_mitarbeiter_option = customtkinter.CTkOptionMenu(self.three_frame_table3_frame,
                                                                              values=["Vorname", "Nachname",
                                                                                      "Abteilung", "Vorgesetzter"],
                                                                              command=self.sorted_by_mitarbeiter,
                                                                              font=customtkinter.CTkFont(size=17,
                                                                                                         weight="bold"),
                                                                              dropdown_font=customtkinter.CTkFont(
                                                                                  size=17, weight="bold"))
        self.sorted_treeview_mitarbeiter_option.grid(row=1, column=0, padx=(135, 0), pady=20, sticky="w")
        self.treeview_struktur.grid(row=2, column=0, padx=(15, 0), columnspan=8)
        self.sorted_by_mitarbeiter("Vorname")

        self.select_table("Table_1")


        ############ FOURTH FRAME ############

        self.four_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.four_frame.grid_columnconfigure(1, weight=1)

        # 4.Label create
        self.four_frame_vorname_label = customtkinter.CTkLabel(self.four_frame, text="Vorname",
                                                               font=customtkinter.CTkFont(size=19, weight="bold"))
        self.four_frame_vorname_label.grid(row=0, column=0, pady=(155, 0), padx=(255, 10), sticky="w")

        self.four_frame_nachname_label = customtkinter.CTkLabel(self.four_frame, text="Nachname",
                                                                font=customtkinter.CTkFont(size=19, weight="bold"))
        self.four_frame_nachname_label.grid(row=0, column=1, pady=(155, 0), padx=10, sticky="w")

        self.four_frame_abteilung_label = customtkinter.CTkLabel(self.four_frame, text="Abteilung",
                                                                 font=customtkinter.CTkFont(size=19, weight="bold"))
        self.four_frame_abteilung_label.grid(row=2, column=0, columnspan=2, pady=(55, 0), padx=(255, 10), sticky="w")

        # 4.Entry create
        self.four_frame_vorname_entry = customtkinter.CTkEntry(self.four_frame, width=250,
                                                               font=customtkinter.CTkFont(size=19))
        self.four_frame_vorname_entry.grid(row=1, column=0, padx=(255, 10), sticky="w")

        self.four_frame_nachname_entry = customtkinter.CTkEntry(self.four_frame, width=250,
                                                                font=customtkinter.CTkFont(size=19))
        self.four_frame_nachname_entry.grid(row=1, column=1, padx=10, sticky="w")

        # 4.Combo create
        self.list_abteilung = ["Auftrag", "Außendienst", "Buchhaltung", "Fertigung", "Support", "IT-Abteilung",
                               "Verwaltung"]

        self.four_frame_abteilung_box = customtkinter.CTkComboBox(self.four_frame, values=self.list_abteilung,
                                                                  width=320,
                                                                  font=customtkinter.CTkFont(size=19),
                                                                  dropdown_font=customtkinter.CTkFont(size=19))
        self.four_frame_abteilung_box.set("Bitte auswählen")
        self.four_frame_abteilung_box.grid(row=2, column=0, sticky="w", columnspan=2, pady=(55, 0), padx=(355, 0))

        self.four_frame_button_confirm = customtkinter.CTkButton(self.four_frame, text="Hinzufügen", width=235,
                                                                 height=65,
                                                                 font=customtkinter.CTkFont(size=24),
                                                                 command=lambda: self.mitarbeiter_add(
                                                                     self.four_frame_vorname_entry.get().strip().capitalize(),
                                                                     self.four_frame_nachname_entry.get().strip().capitalize(),
                                                                     self.four_frame_abteilung_box.get()))
        self.four_frame_button_confirm.grid(row=3, column=0, pady=(55, 0), padx=(255, 0), columnspan=2)
        self.four_frame_label = customtkinter.CTkLabel(self.four_frame, text="", image=self.image_row)

        self.four_frame_button_neu = customtkinter.CTkButton(self.four_frame, text="Neue Anfrage +", width=135,
                                                             height=45,
                                                             font=customtkinter.CTkFont(size=21),
                                                             command=self.neue_anfrage)

        self.four_frame_label_error = customtkinter.CTkLabel(self.four_frame, text_color="red")

        # select default frame
        self.select_frame_by_name("Button_1")

########################################################################################################################





    #def print_test(self):

    #    for rows in self.treeview_vorrat.selection():
    #        # print(self.treeview_vorrat.item(rows, 'values'))

    #        self.test = cursor_position.execute(
    #            f"UPDATE Lager SET Vorname = 'Daniel', "
    #            f"Nachname = 'BBB' "
    #            f"WHERE Hersteller = '{self.treeview_vorrat.item(rows, 'values')[1]}' "
    #            f"AND Model='{self.treeview_vorrat.item(rows, 'values')[2]}' AND Seriennumer='{self.treeview_vorrat.item(rows, 'values')[3]}'")
    #        self.test.commit()

        # self.rows = self.treeview_vorrat.selection()
        # self.valu_2 = self.treeview_vorrat.item(self.rows, 'values')
        # print(self.valu_2)

    ############ FIRST FRAME FUNKTIONS ############

    def change_artikel(self, event):

        self.list_artikel_ausnahme_smartphone = ["smartphone", "handy", "telephone", "iphone"]  # CF
        self.list_artikel_ausnahme_bildschirm = ["bildschirm", "monitor", "bild", "schirm"]  # CF
        self.list_artikel_ausnahme_laptop = ["laptop", "notebook"]  # CF
        self.list_artikel_ausnahme_transponder = ["transponderchip", "chip", "dongle", "donglechip"]  # CF

        if self.first_frame_artikel_entry.get().lower() in self.list_artikel_ausnahme_smartphone:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Smartphone")

        if self.first_frame_artikel_entry.get().lower() in self.list_artikel_ausnahme_bildschirm:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Bildschirm")

        if self.first_frame_artikel_entry.get().lower() in self.list_artikel_ausnahme_laptop:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Laptop")

        if self.first_frame_artikel_entry.get().lower() in self.list_artikel_ausnahme_transponder:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Transponderchip")

    def writing_data_frame_1(self):

        if len(self.first_frame_artikel_entry.get()) > 0:
            command_string = f"INSERT INTO Lager (Artikel, Hersteller, Model, Seriennumer, Datum, Bemerkung) " \
                             f"VALUES ('{self.first_frame_artikel_entry.get().capitalize().strip()}','{self.first_frame_hersteller_entry.get().capitalize().capitalize().strip()}'," \
                             f"'{self.first_frame_model_entry.get().capitalize().strip()}','{self.first_frame_sn_entry.get().strip()}'," \
                             f"'{self.first_frame_datum_entry.get().strip()}','{self.first_frame_bemerkung_entry.get('0.0', 'end')}')"



            self.writing_data_first_frame = cursor_position.execute(command_string)
            self.writing_data_first_frame.commit()
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_hersteller_entry.delete(0, "end")
            self.first_frame_model_entry.delete(0, "end")
            self.first_frame_sn_entry.delete(0, "end")
            self.first_frame_bemerkung_entry.delete("0.0", "end")
            self.label_access.grid(row=8, column=2, padx=(0, 0), pady=(35, 0))
            self.label_error_artikel.grid_forget()
            self.label_error_confirm.grid_forget()

            self.after(3000, lambda: self.label_access.grid_forget())

        else:
            self.label_error_artikel.grid(row=2, column=4, pady=(145, 0))
            self.label_error_confirm.grid(row=8, column=3, padx=(0, 0), pady=(35, 0))

    def first_frame_clear_all(self):
        self.first_frame_artikel_entry.delete(0, "end")
        self.first_frame_hersteller_entry.delete(0, "end")
        self.first_frame_model_entry.delete(0, "end")
        self.first_frame_sn_entry.delete(0, "end")
        self.first_frame_datum_entry.delete(0, "end")
        self.first_frame_datum_entry.insert("0", date_today)
        self.first_frame_bemerkung_entry.delete("0.0", "end")
        self.label_error_artikel.grid_forget()
        self.label_error_confirm.grid_forget()

        ############ SECOND FRAME FUNKTIONS ############

    def sorted_by_second_frame(self, sort_2):

        self.treeview_vorrat_frame_2.delete(*self.treeview_vorrat_frame_2.get_children())

        self.current_list_f2 = cursor_position.execute(
            f'SELECT Artikel, Hersteller, Model, Seriennumer, Bemerkung '
            f'From Lager WHERE Vorname IS NULL ORDER BY {sort_2}')

        self.records_inv_f2 = []
        for i in self.current_list_f2:
            self.records_inv_f2.append(i)

        self.treeview_vorrat_frame_2.tag_configure("oddrow", background="white")
        self.treeview_vorrat_frame_2.tag_configure("evenrow", background="gray95")

        count = 0
        for record in self.records_inv_f2:
            if count % 2 != 0:
                self.treeview_vorrat_frame_2.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4]),
                                                    tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.treeview_vorrat_frame_2.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4]),
                                                    tags=("evenrow"))
                count += 1

        self.treeview_vorrat_frame_2.grid(row=1, column=0, padx=(140,0), pady=(35, 0), columnspan=2)

    def plus_funktion(self):


        for rows in self.treeview_vorrat_frame_2.selection():
            self.treeview_leer_frame_2.insert("", "end", text="", values=(self.treeview_vorrat_frame_2.item(rows, 'values')[0],
                                                             self.treeview_vorrat_frame_2.item(rows, 'values')[1],
                                                             self.treeview_vorrat_frame_2.item(rows, 'values')[2],
                                                             self.treeview_vorrat_frame_2.item(rows, 'values')[3],
                                                             self.treeview_vorrat_frame_2.item(rows, 'values')[4]))

            self.treeview_vorrat_frame_2.delete(self.treeview_vorrat_frame_2.selection()[0])

    def minus_function(self):

        for rows in self.treeview_leer_frame_2.selection():
           self.treeview_vorrat_frame_2.insert("", "end", text="", values=(self.treeview_leer_frame_2.item(rows, 'values')[0],
                                                            self.treeview_leer_frame_2.item(rows, 'values')[1],
                                                            self.treeview_leer_frame_2.item(rows, 'values')[2],
                                                            self.treeview_leer_frame_2.item(rows, 'values')[3],
                                                            self.treeview_leer_frame_2.item(rows, 'values')[4]))
           self.treeview_leer_frame_2.delete(self.treeview_leer_frame_2.selection()[0])


    def sort_function(self, column, table, reverse=False):


        data = [(table.set(child, column), child) for child in table.get_children()]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            table.move(child, '', index)

        table.tag_configure("evenrow", background='gray95')
        table.tag_configure("oddrow", background='white')
        for i, item in enumerate(table.get_children()):
            if i % 2 == 0:
                table.item(item, tags=("evenrow",))
            else:
                table.item(item, tags=("oddrow",))

    def uebergabe_button(self):
        self.dialog_mitarbeiter = customtkinter.CTkToplevel(self)
        self.dialog_mitarbeiter.title("Bitte auswählen")
        self.dialog_mitarbeiter.geometry("500x500+1200+450")
        self.dialog_mitarbeiter.resizable(True, False)
        self.dialog_mitarbeiter.grab_set()
        self.dialog_mitarbeiter.grid_columnconfigure(0, weight=1)
        self.dialog_mitarbeiter.grid_columnconfigure(1, weight=1)
        self.dialog_mitarbeiter_label_vorname = customtkinter.CTkLabel(self.dialog_mitarbeiter, text="Vorname",
                                                                       font=customtkinter.CTkFont(size=25))
        self.dialog_mitarbeiter_label_vorname.grid(row=0, column=0, sticky="w", padx=23, pady=15)
        self.dialog_mitarbeiter_label_nachname = customtkinter.CTkLabel(self.dialog_mitarbeiter, text="Nachname",
                                                                        font=customtkinter.CTkFont(size=25))
        self.dialog_mitarbeiter_label_nachname.grid(row=0, column=1, sticky="w", padx=23, pady=15)
        vorname_list = []
        for row in cursor_position.execute(f"SELECT Vorname FROM Mitarbeiter GROUP BY Vorname"):
            vorname_list.append(*row)
        self.dialog_mitarbeiter_box_vorname = customtkinter.CTkOptionMenu(self.dialog_mitarbeiter, width=200,
                                                                          values=vorname_list,
                                                                          command=self.vorwahl_nachname, font=customtkinter.CTkFont(size=21), dropdown_font=customtkinter.CTkFont(size=19))
        self.dialog_mitarbeiter_box_vorname.grid(row=1, column=0)
        self.dialog_mitarbeiter_box_vorname.set("Bitte auswählen")
        self.dialog_mitarbeiter_box_nachname = customtkinter.CTkOptionMenu(self.dialog_mitarbeiter, width=200, font=customtkinter.CTkFont(size=21), dropdown_font=customtkinter.CTkFont(size=19))
        self.dialog_mitarbeiter_box_nachname.grid(row=1, column=1)
        self.dialog_mitarbeiter_box_nachname.set("")

    def vorwahl_nachname(self, name):
        self.dialog_mitarbeiter_box_nachname.set("Bitte auswählen")
        nachname_list = []
        for row in cursor_position.execute(f"SELECT Nachname FROM Mitarbeiter WHERE Vorname = '{name}' ORDER BY Nachname"):
            nachname_list.append(*row)
        self.dialog_mitarbeiter_box_nachname.configure(values=nachname_list, command=self.bestaetigung_grid)

    def bestaetigung_grid(self, n):


        customtkinter.CTkLabel(self.dialog_mitarbeiter, text=("Folgende mitarbeiter bekomt die Waren:")).grid(row=2, column=0, pady=15)

        for row in self.treeview_leer_frame_2.get_children():
            sofort_label = ' '.join(str(x) for x in self.treeview_leer_frame_2.item(row)['values'][:4])
            customtkinter.CTkLabel(self.dialog_mitarbeiter, text=f"""{sofort_label}""").grid(columnspan=2, column=0, sticky="w", padx=20)

        self.pack1_button = customtkinter.CTkButton(self.dialog_mitarbeiter, text="Bestätigen",
                                                    command=self.bestaetigung_command)
        self.pack1_button.grid(column=0, columnspan=2, pady=45)

        self.abteilung_sting = cursor_position.execute(f"SELECT Abteilung, Vorgesetzter FROM Mitarbeiter "
                                                 f"WHERE Vorname = '{self.dialog_mitarbeiter_box_vorname.get()}' "
                                                 f"AND Nachname = '{self.dialog_mitarbeiter_box_nachname.get()}'")

        abteilung_info = []
        for i in self.abteilung_sting.fetchall():
            for k in i:
                abteilung_info.append(k)

        self.abteilung = abteilung_info[0]
        self.vorgesetzer = abteilung_info[1]



    def bestaetigung_command(self):

        contex = {'name': f'{self.dialog_mitarbeiter_box_vorname.get()}',
                  'nachname': f'{self.dialog_mitarbeiter_box_nachname.get()}',
                  'abteilung': f'{self.abteilung}',
                  'datum': f'{date_today}',
                  'chef': f'{self.vorgesetzer}'}

        for rows in self.treeview_leer_frame_2.get_children():
            self.waren_uebergabe_best = cursor_position.execute(
                f"UPDATE Lager SET Vorname = '{self.dialog_mitarbeiter_box_vorname.get()}', Nachname='{self.dialog_mitarbeiter_box_nachname.get()}' "
                f"WHERE Artikel='{self.treeview_leer_frame_2.item(rows)['values'][0]}' "
                f"AND Hersteller='{self.treeview_leer_frame_2.item(rows)['values'][1]}' "
                f"AND Model='{self.treeview_leer_frame_2.item(rows)['values'][2]}'"
                f"AND Seriennumer='{self.treeview_leer_frame_2.item(rows)['values'][3]}'")

            self.waren_uebergabe_best.commit()

        for num, rows in enumerate(self.treeview_leer_frame_2.get_children()):
            art_name = ' '.join(str(x) for x in self.treeview_leer_frame_2.item(rows)['values'][:3])
            sn = self.treeview_leer_frame_2.item(rows)['values'][3]
            contex[f'art{num}'] = art_name
            contex[f'sn{num}'] = sn
            contex[f'dat{num}'] = date_today

        #self.dialog_mitarbeiter.destroy()
        self.treeview_leer_frame_2.delete(*self.treeview_leer_frame_2.get_children())

        file_dir = (r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//protokoll.docx")
        doc = DocxTemplate(file_dir)
        doc.render(contex)

        count_name = 0
        file_dir_2 = (r"C://Users//dbondarenko//PycharmProjects//pythonProject//Learn//SQL//")
        files = os.listdir(file_dir_2)

        vollname = f'{self.dialog_mitarbeiter_box_vorname.get()}_{self.dialog_mitarbeiter_box_nachname.get()}'

        for name in files:
            if vollname in name:
                count_name+=1

        if count_name==0:
            self.file_name = f"Übergabeprotokoll_{self.dialog_mitarbeiter_box_vorname.get()}_{self.dialog_mitarbeiter_box_nachname.get()}.docx"
            doc.save(self.file_name)
        else:
            self.file_name = f"Übergabeprotokoll_{self.dialog_mitarbeiter_box_vorname.get()}_{self.dialog_mitarbeiter_box_nachname.get()}_({count_name+1}).docx"
            doc.save(self.file_name)

        self.best_btn = customtkinter.CTkButton(self.dialog_mitarbeiter, text="Word", image=self.word, command=self.open)
        self.best_btn.grid(column=0, columnspan=2)


    def open(self):

        subprocess.Popen(['start', fr"C:\Users\dbondarenko\PycharmProjects\pythonProject\Learn\SQL\{self.file_name}"], shell=True)

        ############ THIRD FRAME FUNKTIONS ############

    def sorted_by_lager(self, value_lag):

        self.treeview_vorrat.delete(*self.treeview_vorrat.get_children())

        self.current_list = cursor_position.execute(
            f'SELECT Artikel, Hersteller, Model, Seriennumer, Bemerkung '
            f'From Lager WHERE Vorname IS NULL ORDER BY {value_lag}')

        self.records_inv = []
        for i in self.current_list:
            self.records_inv.append(i)

        self.treeview_vorrat.tag_configure("oddrow", background="white")
        self.treeview_vorrat.tag_configure("evenrow", background="gray95")

        count = 0
        for record in self.records_inv:
            if count % 2 != 0:
                self.treeview_vorrat.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4]),
                                            tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.treeview_vorrat.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4]),
                                            tags=("evenrow"))
                count += 1

        self.treeview_vorrat.grid(row=2, column=0, padx=15, columnspan=8)

    def sorted_by_invertar(self, value_inv):

        self.treeview_invent.delete(*self.treeview_invent.get_children())

        self.current_list = cursor_position.execute(
            f'SELECT Vorname, Nachname, Artikel, Hersteller, Model, Seriennumer, Bemerkung '
            f'From Lager WHERE Vorname IS NOT NULL ORDER BY {value_inv}')

        self.records_inv = []
        for i in self.current_list:
            self.records_inv.append(i)

        self.treeview_invent.tag_configure("oddrow", background="white")
        self.treeview_invent.tag_configure("evenrow", background="gray95")

        count = 0
        for record in self.records_inv:
            if count % 2 != 0:
                self.treeview_invent.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                                            tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.treeview_invent.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                                            tags=("evenrow"))
                count += 1

        self.treeview_invent.grid(row=2, column=0, padx=15, columnspan=8)

    def sorted_by_mitarbeiter(self, value_str):

        self.treeview_struktur.delete(*self.treeview_struktur.get_children())

        self.current_list_struktur = cursor_position.execute(
            f'SELECT Vorname, Nachname, Abteilung, Vorgesetzter '
            f'From Mitarbeiter ORDER BY {value_str}')

        self.records_str = []
        for i in self.current_list_struktur:
            self.records_str.append(i)

        self.treeview_struktur.tag_configure("oddrow", background="white")
        self.treeview_struktur.tag_configure("evenrow", background="gray95")

        count = 0
        for record in self.records_str:
            if count % 2 != 0:
                self.treeview_struktur.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3]),
                                              tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.treeview_struktur.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3]),
                                              tags=("evenrow"))
                count += 1

        self.treeview_struktur.grid(row=2, column=0, padx=15, columnspan=8)

    def clicker_table_1(self, event):

        self.dialog_table1 = customtkinter.CTkToplevel(self)
        self.dialog_table1.geometry(f"260x290+1200+450")
        self.dialog_table1.resizable(False, False)
        self.dialog_table1.grab_set()
        self.dialog_table1.configure(background="green")
        self.dialog_table1.grid_columnconfigure(0, weight=1)
        self.dialog_table1.grid_columnconfigure(1, weight=1)

        self.artikel_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Artikel").grid(row=0, column=0, pady=(16, 4), sticky="e")
        self.hersteller_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Hersteller").grid(row=1, column=0, pady=4, sticky="e")
        self.model_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Model").grid(row=2, column=0, pady=4, sticky="e")
        self.sn_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Seriennummer").grid(row=3, column=0, pady=4, sticky="e")
        self.bemerkung_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Bemerkung").grid(row=4, column=0, pady=4, sticky="e")
        self.artikel_table1 = customtkinter.CTkEntry(self.dialog_table1)
        self.artikel_table1.grid(row=0, column=1, pady=(16, 4))
        self.hersteller_table1 = customtkinter.CTkEntry(self.dialog_table1)
        self.hersteller_table1.grid(row=1, column=1, pady=4)
        self.model_table1 = customtkinter.CTkEntry(self.dialog_table1)
        self.model_table1.grid(row=2, column=1, pady=4)
        self.sn_table1 = customtkinter.CTkEntry(self.dialog_table1)
        self.sn_table1.grid(row=3, column=1, pady=4)
        self.bemerkung_table1 = customtkinter.CTkEntry(self.dialog_table1)
        self.bemerkung_table1.grid(row=4, column=1, pady=4)

        self.selected_table1 = self.treeview_vorrat.focus()

        self.values_table1 = self.treeview_vorrat.item(self.selected_table1, 'values')

        self.dialog_table1.title(f"{self.values_table1[0]} {self.values_table1[1]}")

        self.artikel_table1.insert(0, self.values_table1[0])
        self.hersteller_table1.insert(0, self.values_table1[1])
        self.model_table1.insert(0, self.values_table1[2])
        self.sn_table1.insert(0, self.values_table1[3])
        self.bemerkung_table1.insert(0, self.values_table1[4])

        self.confirm_button_table1 = customtkinter.CTkButton(self.dialog_table1, text="OK",
                                                             command=self.update_record_table_1).grid(row=5, column=1, pady=(20,4))
        self.delete_button_table1 = customtkinter.CTkButton(self.dialog_table1, text="Löschen", fg_color="#C52233",
                                                            hover_color="#F31B31",
                                                            command=self.delete_command_table1).grid(row=6, column=1, pady=4)

    def update_record_table_1(self):
        self.treeview_vorrat.item(self.selected_table1, text="",
                                  values=(self.artikel_table1.get(), self.hersteller_table1.get(),
                                          self.model_table1.get(),
                                          self.sn_table1.get(),
                                          self.bemerkung_table1.get()))

        self.click = cursor_position.execute(f"""UPDATE Lager SET Artikel = '{self.artikel_table1.get()}', 
                                                                         Hersteller = '{self.hersteller_table1.get()}', 
                                                                         Model='{self.model_table1.get()}', 
                                                                         Seriennumer = '{self.sn_table1.get()}', 
                                                                         Bemerkung = '{self.bemerkung_table1.get()}' 
                                                                         WHERE Artikel = '{self.values_table1[0]} '
                                                                         AND Hersteller = '{self.values_table1[1]}' 
                                                                         AND Model = '{self.values_table1[2]}' 
                                                                         AND Seriennumer = '{self.values_table1[3]}' 
                                                                         AND Bemerkung = '{self.values_table1[4]}'""")
        self.click.commit()
        self.dialog_table1.destroy()

    def delete_command_table1(self):

        self.delete_table1_string = cursor_position.execute(f"""DELETE FROM Lager WHERE Artikel = '{self.artikel_table1.get()}' AND Hersteller='{self.hersteller_table1.get()}' AND Model='{self.model_table1.get()}' AND Seriennumer ='{self.sn_table1.get()}'""")

        self.treeview_vorrat.delete(self.selected_table1)
        cursor_position.commit()
        self.dialog_table1.destroy()

    def clicker_table_2(self, event):

        self.dialog_table2 = customtkinter.CTkToplevel(self)
        self.dialog_table2.geometry("260x290+1200+450")
        self.dialog_table2.resizable(False, False)
        self.dialog_table2.grab_set()
        self.dialog_table2.grid_columnconfigure(0, weight=1)
        self.dialog_table2.grid_columnconfigure(1, weight=1)

        self.artikel_table2_label = customtkinter.CTkLabel(self.dialog_table2, text="Artikel").grid(row=0, column=0,
                                                                                                    pady=(16, 4),
                                                                                                    sticky="e")
        self.hersteller_table2_label = customtkinter.CTkLabel(self.dialog_table2, text="Hersteller").grid(row=1,
                                                                                                          column=0,
                                                                                                          pady=4,
                                                                                                          sticky="e")
        self.model_table2_label = customtkinter.CTkLabel(self.dialog_table2, text="Model").grid(row=2, column=0, pady=4,
                                                                                                sticky="e")
        self.sn_table2_label = customtkinter.CTkLabel(self.dialog_table2, text="Seriennummer").grid(row=3, column=0,
                                                                                                    pady=4,
                                                                                                    sticky="e")
        self.bemerkung_table2_label = customtkinter.CTkLabel(self.dialog_table2, text="Bemerkung").grid(row=4, column=0,
                                                                                                        pady=4,
                                                                                                        sticky="e")

        self.artikel_table2 = customtkinter.CTkEntry(self.dialog_table2)
        self.artikel_table2.grid(row=0, column=1, pady=(16, 4))
        self.hersteller_table2 = customtkinter.CTkEntry(self.dialog_table2)
        self.hersteller_table2.grid(row=1, column=1, pady=4)
        self.model_table2 = customtkinter.CTkEntry(self.dialog_table2)
        self.model_table2.grid(row=2, column=1, pady=4)
        self.sn_table2 = customtkinter.CTkEntry(self.dialog_table2)
        self.sn_table2.grid(row=3, column=1, pady=4)
        self.bemerkung_table2 = customtkinter.CTkEntry(self.dialog_table2)
        self.bemerkung_table2.grid(row=4, column=1, pady=4)

        self.selected_table2 = self.treeview_invent.focus()
        self.values_table2 = self.treeview_invent.item(self.selected_table2, 'values')

        self.dialog_table2.title(f"{self.values_table2[0]} {self.values_table2[1]}")

        self.artikel_table2.insert(0, self.values_table2[2])
        self.hersteller_table2.insert(0, self.values_table2[3])
        self.model_table2.insert(0, self.values_table2[4])
        self.sn_table2.insert(0, self.values_table2[5])
        self.bemerkung_table2.insert(0, self.values_table2[6])

        self.confirm_button_table2 = customtkinter.CTkButton(self.dialog_table2, text="OK",
                                                             command=self.update_record_table_2).grid(row=5, column=1,
                                                                                                      pady=(30, 4))

    def update_record_table_2(self):
        self.treeview_invent.item(self.selected_table2, text="",
                                  values=(self.values_table2[0], self.values_table2[1], self.artikel_table2.get(), self.hersteller_table2.get(),
                                          self.model_table2.get(),
                                          self.sn_table2.get(),
                                          self.bemerkung_table2.get()))

        self.click_2 = cursor_position.execute(f"""UPDATE Lager SET Artikel = '{self.artikel_table2.get()}', 
                                                                         Hersteller = '{self.hersteller_table2.get()}', 
                                                                         Model='{self.model_table2.get()}', 
                                                                         Seriennumer = '{self.sn_table2.get()}', 
                                                                         Bemerkung = '{self.bemerkung_table2.get()}' 
                                                                         WHERE Artikel = '{self.values_table2[2]} '
                                                                         AND Hersteller = '{self.values_table2[3]}' 
                                                                         AND Model = '{self.values_table2[4]}' 
                                                                         AND Seriennumer = '{self.values_table2[5]}' 
                                                                         AND Bemerkung = '{self.values_table2[6]}'""")
        self.click_2.commit()
        self.dialog_table2.destroy()

    def rueckgabe(self):

        self.rueckgabe_bestaetigen = messagebox.askyesno("Bitte bestätigen", "Sind Sie sicher?")

        if self.rueckgabe_bestaetigen:


        #self.selected_table2 = self.treeview_invent.focus()
        #self.values_table2 = self.treeview_invent.item(self.selected_table2, 'values')
            for rows in self.treeview_invent.selection():



                self.rueckgabe_string = cursor_position.execute(f"UPDATE Lager SET Vorname = NULL, Nachname = NULL "
                                                                f"WHERE Artikel = '{self.treeview_invent.item(rows, 'values')[2]}' "
                                                                f"AND Hersteller = '{self.treeview_invent.item(rows, 'values')[3]}' "
                                                                f"AND Model = '{self.treeview_invent.item(rows, 'values')[4]}' "
                                                                f"AND Seriennumer = '{self.treeview_invent.item(rows, 'values')[5]}'")
                self.rueckgabe_string.commit()

            self.sorted_by_invertar("Vorname")

        else:
            pass


    def select_table(self, table):

        self.three_frame_lager_button.configure(text_color=("black", "white"),
                                                fg_color=("gray75", "gray25") if table == "Table_1" else "transparent")
        self.three_frame_invent_button.configure(text_color=("black", "white"),
                                                 fg_color=("gray75", "gray25") if table == "Table_2" else "transparent")
        self.three_frame_mitarbeter_button.configure(text_color=("black", "white"), fg_color=(
        "gray75", "gray25") if table == "Table_3" else "transparent")

        if table == "Table_1":
            self.three_frame_table1_frame.grid(columnspan=3, sticky="w")
            self.sorted_by_lager("Artikel")
        else:
            self.three_frame_table1_frame.grid_forget()
        if table == "Table_2":
            self.three_frame_table2_frame.grid(columnspan=3, sticky="w")
        else:
            self.three_frame_table2_frame.grid_forget()
        if table == "Table_3":
            self.three_frame_table3_frame.grid(columnspan=3, sticky="w")
            self.sorted_by_mitarbeiter("Vorname")
        else:
            self.three_frame_table3_frame.grid_forget()

    def table_1(self):
        self.select_table("Table_1")

    def table_2(self):
        self.select_table("Table_2")

    def table_3(self):
        self.select_table("Table_3")


















    ############ FOURTH FRAME FUNKTIONS ############

    def mitarbeiter_add(self, vorname, nachname, abteilung):
        self.vorgesetzer_dict = {"Auftrag": "Svea Wolter",
                                 "Außendienst": "Uwe Heermann",
                                 "Buchhaltung": "Sven von Orsouw",
                                 "Fertigung": "Ina Buch",
                                 "IT-Abteilung": "Andre Gorbunov",
                                 "Support": "Jan Weiske",
                                 "Verwaltung": "Sven Raderschatt"}

        self.current_name = cursor_position.execute(f"SELECT CONCAT(Vorname, ' ', Nachname) FROM Mitarbeiter")
        self.repeat_liste = []
        for name in self.current_name:
            self.repeat_liste.append(*name)

        if vorname + ' ' + nachname in self.repeat_liste:
            self.four_frame_label_error.configure(text=f"Der Mitarbeiter {vorname} {nachname}\nexistiert bereits",
                                                  text_color="Yellow")
            self.four_frame_label_error.grid(row=4, column=0, padx=(255, 0), pady=(5, 0), columnspan=2)
            self.four_frame_vorname_entry.delete(0, "end")
            self.four_frame_nachname_entry.delete(0, "end")
            self.four_frame_abteilung_box.set("Bitte auswählen")

        elif len(vorname) > 0 and \
                len(nachname) > 0 and \
                abteilung != "Bitte auswählen":

            command_string = f"INSERT INTO Mitarbeiter (Vorname, Nachname, Abteilung, Vorgesetzter) VALUES ('{vorname}','{nachname}','{abteilung}','{self.vorgesetzer_dict[abteilung]}')"
            self.writing_data_mitarbeiter = cursor_position.execute(command_string)
            self.writing_data_mitarbeiter.commit()
            self.four_frame_label_hinzu = customtkinter.CTkLabel(self.four_frame,
                                                                 font=customtkinter.CTkFont(size=22),
                                                                 text_color="#9fd8cb",
                                                                 justify=customtkinter.LEFT,
                                                                 text=f"Mitarbeiter {vorname} {nachname}\n\nAbtelung:"
                                                                      f" {abteilung}\nVorgesetzter: {self.vorgesetzer_dict[abteilung]}\n\nwurde "
                                                                      f"erfolgreich hinzugefügt", anchor="w")

            self.four_frame_label_hinzu.grid(row=4, column=0, padx=(455, 0), columnspan=2, pady=(95, 0))
            self.four_frame_label.grid(row=4, column=0, padx=(55, 0), pady=(55, 0))
            self.four_frame_button_neu.grid(row=5, column=0, pady=(85, 0), padx=(250, 0), columnspan=2)
            self.four_frame_label_error.grid_forget()
        else:
            self.four_frame_label_error.configure(text="Bitte füllen Sie alle Felder aus", text_color="red")
            self.four_frame_label_error.grid(row=4, column=0, padx=(255, 0), pady=(5, 0), columnspan=2)

    def neue_anfrage(self):
        self.four_frame_label_hinzu.grid_forget()
        self.four_frame_label.grid_forget()
        self.four_frame_vorname_entry.delete(0, "end")
        self.four_frame_nachname_entry.delete(0, "end")
        self.four_frame_abteilung_box.set("Bitte auswählen")
        self.four_frame_button_neu.grid_forget()




















        ############ ALLGEMEIN ############

    def select_frame_by_name(self, name):
        self.navi_button_1.configure(fg_color=("gray75", "gray25") if name == "Button_1" else "transparent")
        self.navi_button_2.configure(fg_color=("gray75", "gray25") if name == "Button_2" else "transparent")
        self.navi_button_3.configure(fg_color=("gray75", "gray25") if name == "Button_3" else "transparent")
        self.navi_button_4.configure(fg_color=("gray75", "gray25") if name == "Button_4" else "transparent")

        if name == "Button_1":
            self.first_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.first_frame.grid_forget()
        if name == "Button_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.sorted_by_second_frame("Artikel")
        else:
            self.second_frame.grid_forget()
        if name == "Button_3":
            self.three_frame.grid(row=0, column=1, sticky="nsew")
            self.sorted_by_lager("Artikel")
        else:
            self.three_frame.grid_forget()
        if name == "Button_4":
            self.four_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.four_frame.grid_forget()

    def first_frame_navi_button(self):
        self.select_frame_by_name("Button_1")

    def second_frame_navi_button(self):
        self.select_frame_by_name("Button_2")

    def three_frame_navi_button(self):
        self.select_frame_by_name("Button_3")

    def four_frame_navi_button(self):
        self.select_frame_by_name("Button_4")

    def change_mode(self, mode):
        customtkinter.set_appearance_mode(mode)



if __name__ == "__main__":
    app = App()
    app.mainloop()
