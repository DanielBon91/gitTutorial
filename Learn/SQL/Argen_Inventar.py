import tkinter
from tkinter import messagebox
from tkinter.ttk import Scrollbar, Style
import os
import customtkinter
from PIL import Image
from datetime import date, datetime
import customtreeview as ctv
import pyodbc as odbc
from docxtpl import DocxTemplate
import subprocess

date_today = date.today().strftime("%d.%m.%Y")

img_dir = "I://Dokumentation//Dokumentation_IT//Inventariesierung//images"
connection = odbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=EDV-DBO-2;"
                          "Database=ARGEN_INV;"
                          "Trusted_Connection=yes;")

cursor_position = connection.cursor()


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("Argen IT Invertory")
        self.iconbitmap(img_dir + "//argen.ico")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        x = (self.screen_width / 2) - (1410 / 2)
        y = (self.screen_height / 2) - (1200 / 2)

        self.geometry(f"{1410}x{1200}+{int(x)}+{int(y)}")
        self.resizable(False, False)
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.navi_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0)
        self.navi_frame.grid_rowconfigure(5, weight=1)

        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.image_directory = customtkinter.CTkImage(dark_image=Image.open(fr"{img_dir}//ArgenLogo_Weiss.png"),
                                                      light_image=Image.open(fr"{img_dir}//ArgenLogo_Schwarz.png"),
                                                      size=(300, 50))

        # Login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns", padx=530)
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="", image=self.image_directory,
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, pady=(180, 20))
        self.login_name = customtkinter.CTkEntry(self.login_frame, width=300, placeholder_text="username",
                                                 font=customtkinter.CTkFont(size=24))
        self.login_name.grid(row=1, column=0, padx=30, pady=(235, 35))
        self.login_password = customtkinter.CTkEntry(self.login_frame, width=300, show="*", placeholder_text="password",
                                                     font=customtkinter.CTkFont(size=24))
        self.login_password.grid(row=2, column=0, padx=30, pady=(0, 35))
        self.btn_login = customtkinter.CTkButton(self.login_frame, height=80, width=250, text="Login", corner_radius=10,
                                                 command=self.login_event, font=customtkinter.CTkFont(size=24))
        self.btn_login.grid(row=3, column=0, pady=(250, 500))

        self.login_password.bind("<Return>", self.login_event_enter)

        # Create Image
        self.image_label = customtkinter.CTkLabel(self.navi_frame, text="", image=self.image_directory)
        self.image_label.grid(row=0, column=0, padx=15, pady=(55, 25))
        self.image_access = customtkinter.CTkImage(Image.open(fr"{img_dir}//access.png"), size=(50, 50))
        self.image_error_confirm = customtkinter.CTkImage(Image.open(fr"{img_dir}//error.png"), size=(50, 50))

        self.image_error_artikel = customtkinter.CTkImage(Image.open(fr"{img_dir}//error.png"), size=(30, 30))

        self.image_warenannahme = customtkinter.CTkImage(dark_image=Image.open(fr"{img_dir}//box_dark.png"),
                                                         light_image=Image.open(fr"{img_dir}//box_light.png"),
                                                         size=(30, 30))

        self.image_warenuebergabe = customtkinter.CTkImage(dark_image=Image.open(fr"{img_dir}//ubergabe_dark.png"),
                                                           light_image=Image.open(fr"{img_dir}//ubergabe_light.png"),
                                                           size=(35, 35))

        self.image_liste = customtkinter.CTkImage(dark_image=Image.open(fr"{img_dir}//list_dark.png"),
                                                  light_image=Image.open(fr"{img_dir}//list_light.png"), size=(30, 30))

        self.image_mitarbeiter = customtkinter.CTkImage(dark_image=Image.open(fr"{img_dir}//arbeiter_dark.png"),
                                                        light_image=Image.open(fr"{img_dir}//arbeiter_light.png"),
                                                        size=(30, 30))

        self.image_row = customtkinter.CTkImage(Image.open(fr"{img_dir}//row.png"), size=(180, 180))

        self.image_plus = customtkinter.CTkImage(Image.open(fr"{img_dir}//plus.png"), size=(35, 35))

        self.image_minus = customtkinter.CTkImage(Image.open(fr"{img_dir}//minus.png"), size=(35, 35))

        self.word = customtkinter.CTkImage(Image.open(fr"{img_dir}//word.png"), size=(35, 35))

        self.image_rueckgabe = customtkinter.CTkImage(Image.open(fr"{img_dir}//rueckgabe.png"), size=(35, 35))

        self.image_uebergabe = customtkinter.CTkImage(Image.open(fr"{img_dir}//uebergabe.png"), size=(35, 35))

        self.image_pfeil = customtkinter.CTkImage(Image.open(fr"{img_dir}//pfeil.png"), size=(25, 25))

        self.navi_button_1 = customtkinter.CTkButton(self.navi_frame, text="Warenannahme",
                                                     text_color=("gray10", "gray90"),
                                                     height=120, width=250, fg_color="transparent",
                                                     image=self.image_warenannahme,
                                                     hover_color=("gray70", "gray30"),
                                                     command=self.first_frame_navi_button,
                                                     corner_radius=0, font=customtkinter.CTkFont(size=24))

        self.navi_button_2 = customtkinter.CTkButton(self.navi_frame, text="Warenübergabe",
                                                     text_color=("gray10", "gray90"),
                                                     height=120, image=self.image_warenuebergabe,
                                                     fg_color="transparent", hover_color=("gray70", "gray30"),
                                                     corner_radius=0, command=self.second_frame_navi_button,
                                                     border_spacing=10, font=customtkinter.CTkFont(size=24))

        self.navi_button_3 = customtkinter.CTkButton(self.navi_frame, text="Liste", height=120, fg_color="transparent",
                                                     text_color=("gray10", "gray90"), image=self.image_liste,
                                                     hover_color=("gray70", "gray30"),
                                                     corner_radius=0, command=self.three_frame_navi_button,
                                                     font=customtkinter.CTkFont(size=24))

        self.navi_button_4 = customtkinter.CTkButton(self.navi_frame, text="Mitarbeiter",
                                                     text_color=("gray10", "gray90"), image=self.image_mitarbeiter,
                                                     corner_radius=0, height=120, fg_color="transparent",
                                                     hover_color=("gray70", "gray30"),
                                                     command=self.four_frame_navi_button,
                                                     font=customtkinter.CTkFont(size=24))

        self.change_mode = customtkinter.CTkOptionMenu(self.navi_frame, values=["Dark", "Light"],
                                                       command=self.change_mode)

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
        self.first_frame_sn_label = customtkinter.CTkLabel(self.first_frame, text="Seriennummer",
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

        # 1.Buttons create
        self.first_frame_button_confirm = customtkinter.CTkButton(self.first_frame, text="Confirm",
                                                                  corner_radius=10, height=75, width=265,
                                                                  font=customtkinter.CTkFont(size=34),
                                                                  command=self.first_frame_writing_data)

        self.first_frame_button_confirm.grid(row=8, column=1, pady=(55, 15), padx=(115, 0))
        self.first_frame_button_clear = customtkinter.CTkButton(self.first_frame, text="Clear all",
                                                                corner_radius=10,
                                                                height=45, width=210,
                                                                fg_color="gray", hover_color="#C52233",
                                                                font=customtkinter.CTkFont(size=14),
                                                                command=self.first_frame_clear_all)
        self.first_frame_button_clear.grid(row=9, column=1, padx=(115, 0), pady=(55, 15))

        ############ SECOND FRAME ############

        self.style_treeview_style = Style()
        self.style_treeview_style.configure("Treeview", rowheight=25)

        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(1, weight=1)
        # Create upper table frame 2
        self.second_frame_lager_table = ctv.CustomTreeView(self.second_frame, height=24, columns=(
            "column1", "column2", "column3", "column4", "column5"))

        self.tree_scroll_vorrat_frame_2 = customtkinter.CTkScrollbar(self.second_frame,
                                                                     command=self.second_frame_lager_table.yview)
        self.tree_scroll_vorrat_frame_2.grid(row=1, column=1, sticky="nse", pady=(35, 0))

        self.second_frame_lager_table.configure(yscrollcommand=self.tree_scroll_vorrat_frame_2.set)

        self.second_frame_lager_table.heading("#0", text="Item")
        self.second_frame_lager_table.heading("column1", text="Artikel",
                                              command=lambda: self.sort_function("column1",
                                                                                 self.second_frame_lager_table,
                                                                                 False))
        self.second_frame_lager_table.heading("column2", text="Hersteller",
                                              command=lambda: self.sort_function("column2",
                                                                                 self.second_frame_lager_table,
                                                                                 False))
        self.second_frame_lager_table.heading("column3", text="Model",
                                              command=lambda: self.sort_function("column3",
                                                                                 self.second_frame_lager_table,
                                                                                 False))
        self.second_frame_lager_table.heading("column4", text="Seriennummer",
                                              command=lambda: self.sort_function("column4",
                                                                                 self.second_frame_lager_table,
                                                                                 False))
        self.second_frame_lager_table.heading("column5", text="Bemerkung",
                                              command=lambda: self.sort_function("column5",
                                                                                 self.second_frame_lager_table,
                                                                                 False))

        self.second_frame_lager_table.column("#0", width=0, minwidth=0)
        self.second_frame_lager_table.column("column1", width=150)
        self.second_frame_lager_table.column("column2", width=110)
        self.second_frame_lager_table.column("column3")
        self.second_frame_lager_table.column("column4", width=170)
        self.second_frame_lager_table.column("column5", width=190)

        self.second_frame_lager_table.bind("<Double-1>", self.plus_click)

        self.second_frame_movedown_button = customtkinter.CTkButton(self.second_frame, text="", fg_color="#399E5A",
                                                                    hover_color="#328E3D", command=self.plus_funktion,
                                                                    image=self.image_plus, height=50)
        self.second_frame_movedown_button.grid(row=3, column=0, pady=30, padx=120)

        self.second_frame_moveup_button = customtkinter.CTkButton(self.second_frame, text="", fg_color="#C52233",
                                                                  hover_color="#F31B31", command=self.minus_function,
                                                                  image=self.image_minus, height=50)
        self.second_frame_moveup_button.grid(row=3, column=1, pady=30)
        # Create bottom table frame 2
        self.second_frame_leer_table = ctv.CustomTreeView(self.second_frame, height=10, columns=(
            "column1", "column2", "column3", "column4", "column5"))

        self.second_frame_leer_table.heading("#0", text="Item")
        self.second_frame_leer_table.heading("column1", text="Artikel",
                                             command=lambda: self.sort_function("column1", self.second_frame_leer_table,
                                                                                False))
        self.second_frame_leer_table.heading("column2", text="Hersteller",
                                             command=lambda: self.sort_function("column2", self.second_frame_leer_table,
                                                                                False))
        self.second_frame_leer_table.heading("column3", text="Model",
                                             command=lambda: self.sort_function("column3", self.second_frame_leer_table,
                                                                                False))
        self.second_frame_leer_table.heading("column4", text="Seriennummer",
                                             command=lambda: self.sort_function("column4", self.second_frame_leer_table,
                                                                                False))
        self.second_frame_leer_table.heading("column5", text="Bemerkung",
                                             command=lambda: self.sort_function("column5", self.second_frame_leer_table,
                                                                                False))

        self.second_frame_leer_table.column("#0", width=0, minwidth=0)
        self.second_frame_leer_table.column("column1", width=150)
        self.second_frame_leer_table.column("column2", width=110)
        self.second_frame_leer_table.column("column3")
        self.second_frame_leer_table.column("column4", width=170)
        self.second_frame_leer_table.column("column5", width=185)

        self.second_frame_leer_table.grid(row=4, column=0, padx=(140, 0), columnspan=2)
        self.second_frame_leer_table.bind("<Double-1>", self.minus_click)
        self.zuweisen_button = customtkinter.CTkButton(self.second_frame, text="Die Waren übergebe an...",
                                                       width=350, height=80, state="disabled",
                                                       image=self.image_uebergabe,
                                                       command=self.uebergabe_function,
                                                       font=customtkinter.CTkFont(size=25))
        self.zuweisen_button.grid(row=5, column=0, columnspan=2, pady=15, padx=(145, 0))

        ############ THIRD FRAME ############

        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(5, weight=1)

        self.third_frame_lager_button = customtkinter.CTkButton(self.third_frame, text="Lager", width=350,
                                                                height=50, corner_radius=0,
                                                                font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                command=self.table_1)
        self.third_frame_inventar_button = customtkinter.CTkButton(self.third_frame, text="Inventarisierung",
                                                                   width=350, height=50, corner_radius=0,
                                                                   font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                   command=self.table_2)
        self.third_frame_mitarbeter_button = customtkinter.CTkButton(self.third_frame, text="Mitarbeiter",
                                                                     width=350, height=50, corner_radius=0,
                                                                     font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                     command=self.table_3)
        self.third_frame_lager_button.grid(row=0, column=0, pady=(10, 0), padx=(15, 0))
        self.third_frame_inventar_button.grid(row=0, column=1, pady=(10, 0))
        self.third_frame_mitarbeter_button.grid(row=0, column=2, pady=(10, 0))

        ### Table 1 Create ##
        self.third_frame_table1_frame = customtkinter.CTkFrame(self.third_frame, fg_color="transparent")
        self.third_frame_table1_frame.grid_columnconfigure(0, weight=0)

        self.treeview_lager = ctv.CustomTreeView(self.third_frame_table1_frame, height=35, columns=(
            "column1", "column2", "column3", "column4", "column5"))

        self.tree_scroll_lager = customtkinter.CTkScrollbar(self.third_frame_table1_frame,
                                                            command=self.treeview_lager.yview)
        self.tree_scroll_lager.grid(row=2, column=7, sticky="nse", pady=25)

        self.treeview_lager.configure(yscrollcommand=self.tree_scroll_lager.set)

        self.treeview_lager.heading("#0", text="Item")
        self.treeview_lager.heading("column1", text="Artikel",
                                    command=lambda: self.sort_function("column1", self.treeview_lager, False))
        self.treeview_lager.heading("column2", text="Hersteller",
                                    command=lambda: self.sort_function("column2", self.treeview_lager, False))
        self.treeview_lager.heading("column3", text="Model",
                                    command=lambda: self.sort_function("column3", self.treeview_lager, False))
        self.treeview_lager.heading("column4", text="Seriennummer",
                                    command=lambda: self.sort_function("column4", self.treeview_lager, False))
        self.treeview_lager.heading("column5", text="Bemerkung",
                                    command=lambda: self.sort_function("column5", self.treeview_lager, False))

        self.treeview_lager.column("#0", width=0, minwidth=0)
        self.treeview_lager.column("column1", width=180)
        self.treeview_lager.column("column2", width=180)
        self.treeview_lager.column("column3", width=260)
        self.treeview_lager.column("column4", width=190)
        self.treeview_lager.column("column5", width=224)

        self.treeview_lager.bind("<Double-1>", self.clicker_table_1)

        ### Table 2 Create ##
        self.third_frame_table2_frame = customtkinter.CTkFrame(self.third_frame, fg_color="transparent")
        self.third_frame_table2_frame.grid_columnconfigure(0, weight=0)

        self.treeview_inventar = ctv.CustomTreeView(self.third_frame_table2_frame, height=35, columns=(
            "column1", "column2", "column3", "column4", "column5", "column6", "column7"))

        self.tree_scroll_invent = customtkinter.CTkScrollbar(self.third_frame_table2_frame,
                                                             command=self.treeview_inventar.yview)
        self.tree_scroll_invent.grid(row=2, column=7, sticky="nse", pady=25)

        self.treeview_inventar.configure(yscrollcommand=self.tree_scroll_invent.set)

        self.treeview_inventar.heading("#0", text="Item")
        self.treeview_inventar.heading("column1", text="Vorname",
                                       command=lambda: self.sort_function("column1", self.treeview_inventar, False))
        self.treeview_inventar.heading("column2", text="Nachname",
                                       command=lambda: self.sort_function("column2", self.treeview_inventar, False))
        self.treeview_inventar.heading("column3", text="Artikel",
                                       command=lambda: self.sort_function("column3", self.treeview_inventar, False))
        self.treeview_inventar.heading("column4", text="Hersteller",
                                       command=lambda: self.sort_function("column4", self.treeview_inventar, False))
        self.treeview_inventar.heading("column5", text="Model",
                                       command=lambda: self.sort_function("column5", self.treeview_inventar, False))
        self.treeview_inventar.heading("column6", text="Seriennummer",
                                       command=lambda: self.sort_function("column6", self.treeview_inventar, False))
        self.treeview_inventar.heading("column7", text="Bemerkung",
                                       command=lambda: self.sort_function("column7", self.treeview_inventar, False))

        self.treeview_inventar.column("#0", width=0, minwidth=0)
        self.treeview_inventar.column("column1", width=110)
        self.treeview_inventar.column("column2", width=110)
        self.treeview_inventar.column("column3", width=145)
        self.treeview_inventar.column("column4", width=110)
        self.treeview_inventar.column("column5")
        self.treeview_inventar.column("column6", width=169)
        self.treeview_inventar.column("column7", width=190)

        self.treeview_inventar.bind("<Double-1>", self.clicker_table_2)

        self.rueckgabe_button = customtkinter.CTkButton(self.third_frame_table2_frame, width=300, height=70,
                                                        text="Rückgabe machen", image=self.image_rueckgabe,
                                                        fg_color="#328E3D",
                                                        hover_color="#399E5A",
                                                        font=customtkinter.CTkFont(size=21, weight="bold"),
                                                        command=self.rueckgabe).grid(row=3, column=0, padx=15, pady=25)

        self.search = customtkinter.CTkEntry(self.third_frame_table2_frame)
        self.search.grid(row=3, column=1, padx=15, pady=25)

        self.search.bind("<KeyRelease>", self.search_funktion_event)
        ### Table 3 Create ###

        self.third_frame_table3_frame = customtkinter.CTkFrame(self.third_frame, fg_color="transparent")
        self.third_frame_table3_frame.grid_columnconfigure(0, weight=0)

        self.style_treeview_style = Style()
        self.style_treeview_style.configure("Treeview", rowheight=25)

        self.treeview_struktur = ctv.CustomTreeView(self.third_frame_table3_frame, height=35, columns=(
            "column1", "column2", "column3", "column4"))

        self.tree_scroll = customtkinter.CTkScrollbar(self.third_frame_table3_frame,
                                                      command=self.treeview_struktur.yview)
        self.tree_scroll.grid(row=2, column=7, sticky="nse", pady=25)

        self.treeview_struktur.configure(yscrollcommand=self.tree_scroll.set)

        self.treeview_struktur.heading("#0", text="Item2")
        self.treeview_struktur.heading("column1", text="Vorname",
                                       command=lambda: self.sort_function("column1", self.treeview_struktur, False))
        self.treeview_struktur.heading("column2", text="Nachname",
                                       command=lambda: self.sort_function("column2", self.treeview_struktur, False))
        self.treeview_struktur.heading("column3", text="Abteilung",
                                       command=lambda: self.sort_function("column3", self.treeview_struktur, False))
        self.treeview_struktur.heading("column4", text="Vorgesetzter",
                                       command=lambda: self.sort_function("column4", self.treeview_struktur, False))

        self.treeview_struktur.column("#0", width=0, minwidth=0)
        self.treeview_struktur.column("column1", width=250)
        self.treeview_struktur.column("column2", width=250)
        self.treeview_struktur.column("column3", width=267)
        self.treeview_struktur.column("column4", width=267)

        self.treeview_struktur.grid(row=2, column=0, padx=(15, 0), columnspan=8)

        self.treeview_struktur.bind("<Double-1>", self.clicker_table_3)
        self.select_table("Table_1")

        self.neue_mitarbeiter_button = customtkinter.CTkButton(self.third_frame_table3_frame,
                                                                            text="Neue Mitarbeiter +", command=self.neue_mitarbeiter).grid(row=3, column=0)

        ############ FOURTH FRAME ############

        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(1, weight=1)

        # 4.Label create
        self.fourth_frame_vorname_label = customtkinter.CTkLabel(self.fourth_frame, text="Vorname",
                                                                 font=customtkinter.CTkFont(size=19, weight="bold"))
        self.fourth_frame_vorname_label.grid(row=0, column=0, pady=(155, 0), padx=(255, 10), sticky="w")

        self.fourth_frame_nachname_label = customtkinter.CTkLabel(self.fourth_frame, text="Nachname",
                                                                  font=customtkinter.CTkFont(size=19, weight="bold"))
        self.fourth_frame_nachname_label.grid(row=0, column=1, pady=(155, 0), padx=10, sticky="w")

        self.fourth_frame_abteilung_label = customtkinter.CTkLabel(self.fourth_frame, text="Abteilung",
                                                                   font=customtkinter.CTkFont(size=19, weight="bold"))
        self.fourth_frame_abteilung_label.grid(row=2, column=0, columnspan=2, pady=(55, 0), padx=(255, 10), sticky="w")

        # 4.Entry create
        self.fourth_frame_vorname_entry = customtkinter.CTkEntry(self.fourth_frame, width=250,
                                                                 font=customtkinter.CTkFont(size=19))
        self.fourth_frame_vorname_entry.grid(row=1, column=0, padx=(255, 10), sticky="w")

        self.fourth_frame_nachname_entry = customtkinter.CTkEntry(self.fourth_frame, width=250,
                                                                  font=customtkinter.CTkFont(size=19))
        self.fourth_frame_nachname_entry.grid(row=1, column=1, padx=10, sticky="w")

        # 4.Combo create
        self.list_abteilung = ["Auftrag", "Außendienst", "Buchhaltung", "Fertigung", "Support", "IT-Abteilung",
                               "Verwaltung"]

        self.fourth_frame_abteilung_box = customtkinter.CTkComboBox(self.fourth_frame, values=self.list_abteilung,
                                                                    width=320,
                                                                    font=customtkinter.CTkFont(size=19),
                                                                    dropdown_font=customtkinter.CTkFont(size=19))
        self.fourth_frame_abteilung_box.set("Bitte auswählen")
        self.fourth_frame_abteilung_box.grid(row=2, column=0, sticky="w", columnspan=2, pady=(55, 0), padx=(355, 0))

        self.fourth_frame_button_confirm = customtkinter.CTkButton(self.fourth_frame, text="Hinzufügen", width=235,
                                                                   height=65,
                                                                   font=customtkinter.CTkFont(size=24),
                                                                   command=lambda: self.mitarbeiter_add(
                                                                       self.fourth_frame_vorname_entry.get().strip().capitalize(),
                                                                       self.fourth_frame_nachname_entry.get().strip().capitalize(),
                                                                       self.fourth_frame_abteilung_box.get()))
        self.fourth_frame_button_confirm.grid(row=3, column=0, pady=(55, 0), padx=(255, 0), columnspan=2)
        self.fourth_frame_label_row = customtkinter.CTkLabel(self.fourth_frame, text="", image=self.image_row)

        self.four_frame_label_error = customtkinter.CTkLabel(self.fourth_frame, text_color="red")



        # select default frame
        self.select_frame_by_name("Button_1")

    ############################################################################################################################################################################################
    def neue_mitarbeiter(self):
        self.neue_mitarbeiter_dialog = customtkinter.CTkToplevel(self)
        self.neue_mitarbeiter_dialog.title("TEST-TEST-TEST-TEST")
        self.neue_mitarbeiter_dialog.geometry(f"460x560+1200+450")
        self.neue_mitarbeiter_dialog.resizable(False, False)
        self.neue_mitarbeiter_dialog.grab_set()
        self.neue_mitarbeiter_dialog.grid_columnconfigure(0, weight=1)
        self.neue_mitarbeiter_dialog.grid_columnconfigure(1, weight=1)

        def radiobutton_event():
            if radio_var.get() == 1:
                self.geschlecht = "Herr"
            else:
                self.geschlecht = "Frau"

        radio_var = tkinter.IntVar(0)
        self.geschlecht_mann = customtkinter.CTkRadioButton(self.neue_mitarbeiter_dialog, text="Mann",
                                             command=radiobutton_event, variable= radio_var, value=1)
        self.geschlecht_frau = customtkinter.CTkRadioButton(self.neue_mitarbeiter_dialog, text="Frau",
                                             command=radiobutton_event, variable= radio_var, value=2)
        self.geschlecht_mann.grid(row=0, column=0, pady=20)
        self.geschlecht_frau.grid(row=0, column=1, pady=20)

        self.nm_vorname_label = customtkinter.CTkLabel(self.neue_mitarbeiter_dialog, text="Vorname").grid(row=1, column=0, pady=20)
        self.nm_nachname_label = customtkinter.CTkLabel(self.neue_mitarbeiter_dialog, text="Nachname").grid(row=2, column=0, pady=20)
        self.nm_datum_label = customtkinter.CTkLabel(self.neue_mitarbeiter_dialog, text="Datum").grid(row=3, column=0, pady=20)
        self.nm_windows_ps = customtkinter.CTkLabel(self.neue_mitarbeiter_dialog, text="Windows Password").grid(row=4, column=0, pady=20)
        self.nm_quorra_ps = customtkinter.CTkLabel(self.neue_mitarbeiter_dialog, text="Quorra Password").grid(row=5, column=0, pady=20)

        self.nm_vorname_entry = customtkinter.CTkEntry(self.neue_mitarbeiter_dialog)
        self.nm_nachname_entry = customtkinter.CTkEntry(self.neue_mitarbeiter_dialog)
        self.nm_datum_entry = customtkinter.CTkEntry(self.neue_mitarbeiter_dialog)
        self.nm_windows_entry = customtkinter.CTkEntry(self.neue_mitarbeiter_dialog)
        self.nm_quorra_entry = customtkinter.CTkEntry(self.neue_mitarbeiter_dialog)

        self.nm_vorname_entry.grid(row=1, column=1, pady=20)
        self.nm_nachname_entry.grid(row=2, column=1, pady=20)
        self.nm_datum_entry.grid(row=3, column=1, pady=20)
        self.nm_windows_entry.grid(row=4, column=1, pady=20)
        self.nm_quorra_entry.grid(row=5, column=1, pady=20)

        self.nm_bestaetigung_button = customtkinter.CTkButton(self.neue_mitarbeiter_dialog,
                                                              text="PUSH",
                                                              command=lambda : self.neue_mitarbeiter_word(self.geschlecht,
                                                                                                          self.nm_vorname_entry.get(),
                                                                                                          self.nm_nachname_entry.get(),
                                                                                                          self.nm_datum_entry.get(),
                                                                                                          self.nm_windows_entry.get(),
                                                                                                          self.nm_quorra_entry.get())).grid(row=6,
                                                                                                       column=0,
                                                                                                       columnspan=2,
                                                                                                       pady=20)

    def neue_mitarbeiter_word(self, geschlecht, vorname, nachname, datum, wpassword, qpassword):

        contex = {'geschlecht': geschlecht,
                  'vorname': vorname,
                  'nachname': nachname,
                  'datum': datum,
                  'wpassword': wpassword,
                  'qpassword': qpassword}

        file_dir = (
            r"I://Dokumentation//Dokumentation_IT//Inventariesierung//Mitarbeiter//Neuer_Mitarbeiter.docx")
        doc = DocxTemplate(file_dir)
        doc.render(contex)

        folder_path = fr"I://Dokumentation//Dokumentation_IT//Inventariesierung//Mitarbeiter//{vorname.strip()}_{nachname}//"  # указываем путь для новой папки

        if not os.path.exists(folder_path):  # проверяем, существует ли папка
            os.makedirs(folder_path)  # создаем папку

        dir_path = fr"I://Dokumentation//Dokumentation_IT//Inventariesierung//Mitarbeiter//{vorname.strip()}_{nachname}//Neuer_Mitarbeiter_{vorname.strip()}_{nachname}.docx"
        doc.save(dir_path)

        self.word_open = customtkinter.CTkButton(self.neue_mitarbeiter_dialog,
                                                              text="WORD",
                                                              command=lambda: self.open_nm(dir_path)).grid(row=7, column=0, columnspan=2, pady=20)

    def open_nm(self, path):
        subprocess.Popen(
            ['start', path],
            shell=True)

    def login_event_enter(self, e):
        self.login_event()

    def login_event(self):
        if self.login_name.get() == "admin" and self.login_password.get() == "admin":
            self.login_frame.grid_forget()
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.navi_frame.grid(row=0, column=0, sticky="nsew")
            self.navi_button_1.grid(row=1, column=0, pady=(35, 0), sticky="ew")
            self.navi_button_2.grid(row=2, column=0, sticky="ew")
            self.navi_button_3.grid(row=3, column=0, sticky="ew")
            self.navi_button_4.grid(row=4, column=0, sticky="ew")
            self.change_mode.grid(row=6, sticky="s", pady=(500, 30))

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

    ############ FIRST FRAME FUNKTIONS ############

    def change_artikel(self, event):
        list_artikel_ausnahme_smartphone = ["smartphone", "handy", "telephone", "iphone"]  # CF
        list_artikel_ausnahme_bildschirm = ["bildschirm", "monitor", "bild", "schirm"]  # CF
        list_artikel_ausnahme_laptop = ["laptop", "notebook"]  # CF
        list_artikel_ausnahme_transponder = ["transponderchip", "chip", "dongle", "donglechip"]  # CF
        if self.first_frame_artikel_entry.get().lower() in list_artikel_ausnahme_smartphone:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Smartphone")
        if self.first_frame_artikel_entry.get().lower() in list_artikel_ausnahme_bildschirm:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Bildschirm")
        if self.first_frame_artikel_entry.get().lower() in list_artikel_ausnahme_laptop:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Laptop")
        if self.first_frame_artikel_entry.get().lower() in list_artikel_ausnahme_transponder:
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_artikel_entry.insert(0, "Transponderchip")

    def first_frame_writing_data(self):
        if self.first_frame_sn_entry.get().strip()[0] == "0":
            sn_null = f"1{self.first_frame_sn_entry.get().strip()}"
        else:
            sn_null = f"{self.first_frame_sn_entry.get().strip()}"

        if len(self.first_frame_artikel_entry.get()) > 0:
            command_string = f"INSERT INTO Inventar (Artikel, Hersteller, Model, Seriennummer, Datum, Bemerkung) " \
                             f"VALUES ('{self.first_frame_artikel_entry.get().capitalize().strip()}','{self.first_frame_hersteller_entry.get().capitalize().capitalize().strip()}'," \
                             f"'{self.first_frame_model_entry.get().strip()}','{sn_null}'," \
                             f"'{self.first_frame_datum_entry.get().strip()}','{self.first_frame_bemerkung_entry.get('0.0', 'end').strip()}')"
            writing_data_first_frame = cursor_position.execute(command_string)
            writing_data_first_frame.commit()
            self.first_frame_artikel_entry.delete(0, "end")
            self.first_frame_hersteller_entry.delete(0, "end")
            self.first_frame_model_entry.delete(0, "end")
            self.first_frame_sn_entry.delete(0, "end")
            self.first_frame_bemerkung_entry.delete("0.0", "end")
            self.label_access.grid(row=8, column=2, columnspan=2, padx=(0, 0), pady=(35, 0))
            self.label_error_artikel.grid_forget()
            self.label_error_confirm.grid_forget()
            self.after(3000, lambda: self.label_access.grid_forget())
            self.after(3000, lambda: self.first_frame_datum_entry.delete(0, "end"))
            self.after(3000, lambda: self.first_frame_datum_entry.insert(0, date_today))
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

    def second_frame_lager_tabelle(self):
        self.second_frame_lager_table.delete(*self.second_frame_lager_table.get_children())

        current_list_second_frame = cursor_position.execute(
            f'SELECT Artikel, Hersteller, Model, Seriennummer, Bemerkung '
            f'From Inventar WHERE Vorname IS NULL ORDER BY Artikel')

        records_invertar_second_frame = []

        for record in current_list_second_frame:
            records_invertar_second_frame.append(record)

        self.second_frame_lager_table.tag_configure("oddrow", background="white")
        self.second_frame_lager_table.tag_configure("evenrow", background="gray95")

        count = 0
        for record in records_invertar_second_frame:
            if count % 2 != 0:
                self.second_frame_lager_table.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], str(record[3]), record[4]),
                                                     tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.second_frame_lager_table.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], str(record[3]), record[4]),
                                                     tags=("evenrow"))
                count += 1

        self.second_frame_lager_table.grid(row=1, column=0, padx=(140, 0), pady=(35, 0), columnspan=2)


    def plus_funktion(self):

        for rows in self.second_frame_lager_table.selection():
            self.second_frame_leer_table.insert("", "end", text="",
                                                values=(self.second_frame_lager_table.item(rows, 'values')[0],
                                                        self.second_frame_lager_table.item(rows, 'values')[1],
                                                        self.second_frame_lager_table.item(rows, 'values')[2],
                                                        self.second_frame_lager_table.item(rows, 'values')[3],
                                                        self.second_frame_lager_table.item(rows, 'values')[4]))

            self.second_frame_lager_table.delete(self.second_frame_lager_table.selection()[0])

        if len(self.second_frame_leer_table.get_children()) > 0:
            self.zuweisen_button.configure(state="normal")

    def plus_click(self, e):
        self.plus_funktion()

    def minus_function(self):
        for rows in self.second_frame_leer_table.selection():
            self.second_frame_lager_table.insert("", "end", text="",
                                                 values=(self.second_frame_leer_table.item(rows, 'values')[0],
                                                         self.second_frame_leer_table.item(rows, 'values')[1],
                                                         self.second_frame_leer_table.item(rows, 'values')[2],
                                                         self.second_frame_leer_table.item(rows, 'values')[3],
                                                         self.second_frame_leer_table.item(rows, 'values')[4]))
            self.second_frame_leer_table.delete(self.second_frame_leer_table.selection()[0])

        if len(self.second_frame_leer_table.get_children()) == 0:
            self.zuweisen_button.configure(state="disabled")

    def minus_click(self, e):
        self.minus_function()

    def uebergabe_function(self):
        self.dialog_mitarbeiter = customtkinter.CTkToplevel(self)
        self.dialog_mitarbeiter.title("Bitte auswählen")
        self.dialog_mitarbeiter.geometry("800x750+1030+250")
        self.dialog_mitarbeiter.resizable(False, False)
        self.dialog_mitarbeiter.grab_set()
        self.dialog_mitarbeiter.grid_columnconfigure(0, weight=1)
        self.dialog_mitarbeiter.grid_columnconfigure(1, weight=1)
        self.dialog_mitarbeiter.grid_columnconfigure(2, weight=0)
        self.dialog_mitarbeiter.grid_rowconfigure(15, weight=0)
        self.dialog_mitarbeiter.grid_rowconfigure(16, weight=0)
        self.dialog_mitarbeiter_label_vorname = customtkinter.CTkLabel(self.dialog_mitarbeiter, text="Vorname",
                                                                       font=customtkinter.CTkFont(size=25))
        self.dialog_mitarbeiter_label_vorname.grid(row=0, column=0, sticky="w", padx=(95, 0), pady=15)
        self.dialog_mitarbeiter_label_nachname = customtkinter.CTkLabel(self.dialog_mitarbeiter, text="Nachname",
                                                                        font=customtkinter.CTkFont(size=25))
        self.dialog_mitarbeiter_label_nachname.grid(row=0, column=1, sticky="w", padx=(105, 0), pady=15)
        vorname_list = []
        for row in cursor_position.execute(f"SELECT Vorname FROM Mitarbeiter GROUP BY Vorname"):
            vorname_list.append(*row)
        self.dialog_mitarbeiter_box_vorname = customtkinter.CTkOptionMenu(self.dialog_mitarbeiter, width=200,
                                                                          values=vorname_list,
                                                                          command=self.vorwahl_nachname,
                                                                          font=customtkinter.CTkFont(size=21),
                                                                          dropdown_font=customtkinter.CTkFont(size=19))
        self.dialog_mitarbeiter_box_vorname.grid(row=1, column=0)
        self.dialog_mitarbeiter_box_vorname.set("Bitte auswählen")
        self.dialog_mitarbeiter_box_nachname = customtkinter.CTkOptionMenu(self.dialog_mitarbeiter, state="disabled",
                                                                           width=200,
                                                                           font=customtkinter.CTkFont(size=21),
                                                                           dropdown_font=customtkinter.CTkFont(size=19))
        self.dialog_mitarbeiter_box_nachname.grid(row=1, column=1)
        self.dialog_mitarbeiter_box_nachname.set("Bitte auswählen")

    def vorwahl_nachname(self, name):
        self.dialog_mitarbeiter_box_nachname.configure(state="normal")
        self.dialog_mitarbeiter_box_nachname.set("Bitte auswählen")
        nachname_list = []
        for row in cursor_position.execute(
                f"SELECT Nachname FROM Mitarbeiter WHERE Vorname = '{name}' ORDER BY Nachname"):
            nachname_list.append(*row)
        self.dialog_mitarbeiter_box_nachname.configure(values=nachname_list, command=self.bestaetigung_grid)

    def bestaetigung_grid(self, n):
        customtkinter.CTkLabel(self.dialog_mitarbeiter, font=customtkinter.CTkFont(size=25, weight="bold"), text=(
            f"{self.dialog_mitarbeiter_box_vorname.get()} {self.dialog_mitarbeiter_box_nachname.get()} bekomt die Waren:")).grid(
            row=2, column=0, columnspan=3, padx=(50, 0), pady=(45, 15), sticky="w")

        for row in self.second_frame_leer_table.get_children():
            sofort_label = ' '.join(str(x) for x in self.second_frame_leer_table.item(row)['values'][:4])
            customtkinter.CTkLabel(self.dialog_mitarbeiter, font=customtkinter.CTkFont(size=18),
                                   text=f"""- {sofort_label}""").grid(column=0, columnspan=3, sticky="w", padx=(75, 0))

        customtkinter.CTkLabel(self.dialog_mitarbeiter, text="Übergabedatum:",
                               font=customtkinter.CTkFont(size=19, weight="bold")).grid(row=14, column=0, columnspan=3,
                                                                                        sticky="w",
                                                                                        padx=(60, 0), pady=20)
        self.data_entry = customtkinter.CTkEntry(self.dialog_mitarbeiter, height=35, placeholder_text="dd.mm.YYYY",
                                                 font=customtkinter.CTkFont(size=19))
        self.data_entry.grid(row=14, column=0, sticky="w", padx=(230, 0), pady=20, columnspan=3)
        self.data_get = customtkinter.CTkButton(self.dialog_mitarbeiter, width=45, text="", image=self.image_pfeil,
                                                command=lambda: self.button_active(self.data_entry.get()))
        self.data_get.grid(row=14, column=0, columnspan=3)

        self.top_level_confirm_button = customtkinter.CTkButton(self.dialog_mitarbeiter, width=200, height=45,
                                                                text="Bestätigen", state="disabled",
                                                                font=customtkinter.CTkFont(size=21, weight="bold"),
                                                                command=self.bestaetigung_command)
        self.top_level_confirm_button.grid(row=15, column=0, columnspan=3, pady=45, sticky="s")

        abteilung_stirng = cursor_position.execute(f"SELECT Abteilung, Vorgesetzter FROM Mitarbeiter "
                                                   f"WHERE Vorname = '{self.dialog_mitarbeiter_box_vorname.get()}' "
                                                   f"AND Nachname = '{self.dialog_mitarbeiter_box_nachname.get()}'")

        abteilung_info = []
        for rows in abteilung_stirng.fetchall():
            for column in rows:
                abteilung_info.append(column)

        self.abteilung = abteilung_info[0]
        self.vorgesetzer = abteilung_info[1]

    def button_active(self, date):
        if len(date) == 10:
            self.top_level_confirm_button.configure(state="normal")
        else:
            pass

    def bestaetigung_command(self):
        contex = {'name': f'{self.dialog_mitarbeiter_box_vorname.get()}',
                  'nachname': f'{self.dialog_mitarbeiter_box_nachname.get()}',
                  'abteilung': f'{self.abteilung}',
                  'chef': f'{self.vorgesetzer}'}

        for rows in self.second_frame_leer_table.get_children():
            self.waren_uebergabe_best = cursor_position.execute(
                f"UPDATE Inventar SET Vorname = '{self.dialog_mitarbeiter_box_vorname.get()}', "
                f"Nachname='{self.dialog_mitarbeiter_box_nachname.get()}' "
                f"WHERE Artikel='{self.second_frame_leer_table.item(rows)['values'][0]}' "
                f"AND Hersteller='{self.second_frame_leer_table.item(rows)['values'][1]}' "
                f"AND Model='{self.second_frame_leer_table.item(rows)['values'][2]}'"
                f"AND Seriennummer='{self.second_frame_leer_table.item(rows)['values'][3]}'")
            self.waren_uebergabe_best.commit()

        for num, rows in enumerate(self.second_frame_leer_table.get_children()):
            art_name = ' '.join(str(x) for x in self.second_frame_leer_table.item(rows)['values'][:3])
            sn = self.second_frame_leer_table.item(rows)['values'][3]
            contex[f'art{num}'] = art_name
            contex[f'sn{num}'] = sn
            contex[f'dat{num}'] = self.data_entry.get()

        self.second_frame_leer_table.delete(*self.second_frame_leer_table.get_children())

        file_dir = (r"I://Dokumentation//Dokumentation_IT//Inventariesierung//Übergabeprotokoll//default_protokoll.docx")
        doc = DocxTemplate(file_dir)
        doc.render(contex)

        count_name = 0
        file_dir_2 = (r"I://Dokumentation//Dokumentation_IT//Inventariesierung//Übergabeprotokoll//")
        files = os.listdir(file_dir_2)

        vollname = f'{self.dialog_mitarbeiter_box_vorname.get()}_{self.dialog_mitarbeiter_box_nachname.get()}'

        for name in files:
            if vollname in name:
                count_name += 1
 
        if count_name == 0:
            self.file_name = f"Übergabeprotokoll_{self.dialog_mitarbeiter_box_vorname.get()}_" \
                             f"{self.dialog_mitarbeiter_box_nachname.get()}.docx"
            doc.save(f"{file_dir_2}{self.file_name}")
        else:
            self.file_name = f"Übergabeprotokoll_{self.dialog_mitarbeiter_box_vorname.get()}_" \
                             f"{self.dialog_mitarbeiter_box_nachname.get()}_({count_name + 1}).docx"
            doc.save(f"{file_dir_2}{self.file_name}")

        self.bestaetigung_button = customtkinter.CTkButton(self.dialog_mitarbeiter, text="Word", image=self.word,
                                                           command=self.open)
        self.bestaetigung_button.grid(row=16, column=0, columnspan=2)

    def open(self):
        subprocess.Popen(['start', fr"I:\Dokumentation\Dokumentation_IT\Inventariesierung\Übergabeprotokoll\{self.file_name}"],
            shell=True)
        self.dialog_mitarbeiter.destroy()
        self.zuweisen_button.configure(state="disabled")

    ############ THIRD FRAME FUNKTIONS ############
    # Table 1
    def third_frame_table_1(self):

        self.treeview_lager.delete(*self.treeview_lager.get_children())

        current_list = cursor_position.execute(
            f'SELECT Artikel, Hersteller, Model, Seriennummer, Bemerkung '
            f'From Inventar WHERE Vorname IS NULL ORDER BY Artikel')

        records_table_1 = []
        for row in current_list:
            records_table_1.append(row)

        self.treeview_lager.tag_configure("oddrow", background="white")
        self.treeview_lager.tag_configure("evenrow", background="gray95")

        count = 0
        for record in records_table_1:
            if count % 2 != 0:
                self.treeview_lager.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4]),
                                           tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.treeview_lager.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4]),
                                           tags=("evenrow"))
                count += 1

        self.treeview_lager.grid(row=2, column=0, padx=15, pady=25, columnspan=8)

    def clicker_table_1(self, event):

        self.dialog_table1 = customtkinter.CTkToplevel(self)
        self.dialog_table1.geometry(f"260x290+1200+450")
        self.dialog_table1.resizable(False, False)
        self.dialog_table1.grab_set()
        self.dialog_table1.configure(background="green")
        self.dialog_table1.grid_columnconfigure(0, weight=1)
        self.dialog_table1.grid_columnconfigure(1, weight=1)

        self.artikel_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Artikel").grid(row=0, column=0,
                                                                                                    pady=(16, 4),
                                                                                                    sticky="e")
        self.hersteller_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Hersteller").grid(row=1,
                                                                                                          column=0,
                                                                                                          pady=4,
                                                                                                          sticky="e")
        self.model_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Model").grid(row=2, column=0, pady=4,
                                                                                                sticky="e")
        self.sn_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Seriennummer").grid(row=3, column=0,
                                                                                                    pady=4, sticky="e")
        self.bemerkung_table1_label = customtkinter.CTkLabel(self.dialog_table1, text="Bemerkung").grid(row=4, column=0,
                                                                                                        pady=4,
                                                                                                        sticky="e")
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

        self.selected_table1 = self.treeview_lager.focus()

        self.values_table1 = self.treeview_lager.item(self.selected_table1, 'values')

        self.dialog_table1.title(f"{self.values_table1[0]} {self.values_table1[1]}")

        self.artikel_table1.insert(0, self.values_table1[0])
        self.hersteller_table1.insert(0, self.values_table1[1])
        self.model_table1.insert(0, self.values_table1[2])
        self.sn_table1.insert(0, self.values_table1[3])
        self.bemerkung_table1.insert(0, self.values_table1[4].strip())

        self.confirm_button_table1 = customtkinter.CTkButton(self.dialog_table1, text="OK",
                                                             command=self.update_record_table_1).grid(row=5, column=1,
                                                                                                      pady=(20, 4))
        self.delete_button_table1 = customtkinter.CTkButton(self.dialog_table1, text="Löschen", fg_color="#C52233",
                                                            hover_color="#F31B31",
                                                            command=self.delete_command_table1).grid(row=6, column=1,
                                                                                                     pady=4)

    def update_record_table_1(self):
        self.treeview_lager.item(self.selected_table1, text="",
                                 values=(self.artikel_table1.get(), self.hersteller_table1.get(),
                                         self.model_table1.get(),
                                         self.sn_table1.get(),
                                         self.bemerkung_table1.get()))

        update_record_1 = cursor_position.execute(f"""UPDATE Inventar SET Artikel = '{self.artikel_table1.get()}', 
                                                                         Hersteller = '{self.hersteller_table1.get()}', 
                                                                         Model='{self.model_table1.get()}', 
                                                                         Seriennummer = '{self.sn_table1.get()}', 
                                                                         Bemerkung = '{self.bemerkung_table1.get()}' 
                                                                         WHERE Artikel = '{self.values_table1[0]} '
                                                                         AND Hersteller = '{self.values_table1[1]}' 
                                                                         AND Model = '{self.values_table1[2]}' 
                                                                         AND Seriennummer = '{self.values_table1[3]}' 
                                                                         AND Bemerkung = '{self.values_table1[4]}'""")
        update_record_1.commit()
        self.dialog_table1.destroy()

    def delete_command_table1(self):

        delete_table1_string = cursor_position.execute(
            f"""DELETE FROM Inventar WHERE Artikel = '{self.artikel_table1.get()}' AND Hersteller='{self.hersteller_table1.get()}' AND Model='{self.model_table1.get()}' AND Seriennummer ='{self.sn_table1.get()}'""")

        self.treeview_lager.delete(self.selected_table1)
        delete_table1_string.commit()
        self.dialog_table1.destroy()

    # Table 2
    def third_frame_table_2(self):

        self.treeview_inventar.delete(*self.treeview_inventar.get_children())

        current_list = cursor_position.execute(
            f'SELECT Vorname, Nachname, Artikel, Hersteller, Model, Seriennummer, Bemerkung '
            f'From Inventar WHERE Vorname IS NOT NULL ORDER BY Vorname')

        records_table_2 = []
        for row in current_list:
            records_table_2.append(row)

        self.treeview_inventar.tag_configure("oddrow", background="white")
        self.treeview_inventar.tag_configure("evenrow", background="gray95")

        count = 0
        for record in records_table_2:
            if count % 2 != 0:
                self.treeview_inventar.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                                              tags=("oddrow"))
                count += 1
            elif count % 2 == 0:
                self.treeview_inventar.insert("", "end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                                              tags=("evenrow"))
                count += 1

        self.treeview_inventar.grid(row=2, column=0, padx=15, pady=25, columnspan=8)


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

        self.selected_table2 = self.treeview_inventar.focus()
        self.values_table2 = self.treeview_inventar.item(self.selected_table2, 'values')

        self.dialog_table2.title(f"{self.values_table2[0]} {self.values_table2[1]}")

        self.artikel_table2.insert(0, self.values_table2[2])
        self.hersteller_table2.insert(0, self.values_table2[3])
        self.model_table2.insert(0, self.values_table2[4])
        self.sn_table2.insert(0, self.values_table2[5])
        self.bemerkung_table2.insert(0, self.values_table2[6])

        self.confirm_button_table2 = customtkinter.CTkButton(self.dialog_table2, text="OK",
                                                             command=self.update_record_table_2).grid(row=5, column=1,
                                                                                                      pady=(30, 4))

    def rueckgabe(self):

        rueckgabe_bestaetigen = messagebox.askyesno("Bitte bestätigen", "Sind Sie sicher?")

        if rueckgabe_bestaetigen:

            for rows in self.treeview_inventar.selection():
                self.rueckgabe_string = cursor_position.execute(f"UPDATE Inventar SET Vorname = NULL, Nachname = NULL "
                                                                f"WHERE Artikel = '{self.treeview_inventar.item(rows, 'values')[2]}' "
                                                                f"AND Hersteller = '{self.treeview_inventar.item(rows, 'values')[3]}' "
                                                                f"AND Model = '{self.treeview_inventar.item(rows, 'values')[4]}' "
                                                                f"AND Seriennummer = '{self.treeview_inventar.item(rows, 'values')[5]}'")
                self.rueckgabe_string.commit()

        else:
            pass

        self.third_frame_table_2()

    def update_record_table_2(self):
        self.treeview_inventar.item(self.selected_table2, text="",
                                    values=(self.values_table2[0], self.values_table2[1], self.artikel_table2.get(),
                                            self.hersteller_table2.get(),
                                            self.model_table2.get(),
                                            self.sn_table2.get(),
                                            self.bemerkung_table2.get()))

        update_record_2 = cursor_position.execute(f"""UPDATE Inventar SET Artikel = '{self.artikel_table2.get()}', 
                                                                            Hersteller = '{self.hersteller_table2.get()}', 
                                                                            Model='{self.model_table2.get()}', 
                                                                            Seriennummer = '{self.sn_table2.get()}', 
                                                                            Bemerkung = '{self.bemerkung_table2.get()}' 
                                                                            WHERE Artikel = '{self.values_table2[2]} '
                                                                            AND Hersteller = '{self.values_table2[3]}' 
                                                                            AND Model = '{self.values_table2[4]}' 
                                                                            AND Seriennummer = '{self.values_table2[5]}' 
                                                                            AND Bemerkung = '{self.values_table2[6]}'""")
        update_record_2.commit()
        self.dialog_table2.destroy()
        if self.search=="":
            self.third_frame_table_2()
        else:
            self.search_function()

    def search_function(self):

        if self.search.get() == "":
            self.third_frame_table_2()
        else:
            self.treeview_inventar.delete(*self.treeview_inventar.get_children())

            current_list_second_frame = cursor_position.execute(
                f"""SELECT Vorname, Nachname, Artikel, Hersteller, Model, Seriennummer, Bemerkung From Inventar WHERE Vorname LIKE '{self.search.get()}%' ORDER BY Vorname""")
            records_invertar_second_frame = []
            for record in current_list_second_frame:
                records_invertar_second_frame.append(record)

            self.treeview_inventar.tag_configure("oddrow", background="white")
            self.treeview_inventar.tag_configure("evenrow", background="gray95")
            count = 0
            for record in records_invertar_second_frame:
                if count % 2 != 0:
                    self.treeview_inventar.insert("", "end", iid=count, text="", values=(
                        record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                                                  tags=("oddrow"))
                    count += 1
                elif count % 2 == 0:
                    self.treeview_inventar.insert("", "end", iid=count, text="", values=(
                        record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                                                  tags=("evenrow"))
                    count += 1

    def search_funktion_event(self, e):
        self.search_function()

    # Table 3
    def third_frame_table_3(self):

        self.treeview_struktur.delete(*self.treeview_struktur.get_children())

        current_list_struktur = cursor_position.execute(
            f'SELECT Vorname, Nachname, Abteilung, Vorgesetzter '
            f'From Mitarbeiter ORDER BY Vorname')

        records_str = []
        for row in current_list_struktur:
            records_str.append(row)

        self.treeview_struktur.tag_configure("oddrow", background="white")
        self.treeview_struktur.tag_configure("evenrow", background="gray95")

        count = 0
        for record in records_str:
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

        self.treeview_struktur.grid(row=2, column=0, padx=15, pady=25, columnspan=8)

    def clicker_table_3(self, event):
        self.dialog_table3 = customtkinter.CTkToplevel(self)
        self.dialog_table3.geometry("260x290+1200+450")
        self.dialog_table3.resizable(False, False)
        self.dialog_table3.grab_set()
        self.dialog_table3.grid_columnconfigure(0, weight=1)
        self.dialog_table3.grid_columnconfigure(1, weight=1)

        self.vorname_table_3 = customtkinter.CTkLabel(self.dialog_table3, text="Vorname").grid(row=0, column=0,
                                                                                               pady=(16, 4),
                                                                                               sticky="e")
        self.nachname_table_3 = customtkinter.CTkLabel(self.dialog_table3, text="Nachname").grid(row=1,
                                                                                                 column=0,
                                                                                                 pady=4,
                                                                                                 sticky="e")
        self.abteilung_table_3 = customtkinter.CTkLabel(self.dialog_table3, text="Abteilung").grid(row=2, column=0,
                                                                                                   pady=4,
                                                                                                   sticky="e")
        self.vorgesetzter_table_3 = customtkinter.CTkLabel(self.dialog_table3, text="Vorgesetzter").grid(row=3,
                                                                                                         column=0,
                                                                                                         pady=4,
                                                                                                         sticky="e")

        self.vorname_table3 = customtkinter.CTkEntry(self.dialog_table3)
        self.vorname_table3.grid(row=0, column=1, pady=(16, 4))
        self.nachname_table3 = customtkinter.CTkEntry(self.dialog_table3)
        self.nachname_table3.grid(row=1, column=1, pady=4)
        self.abteilung_table3 = customtkinter.CTkEntry(self.dialog_table3)
        self.abteilung_table3.grid(row=2, column=1, pady=4)
        self.vorgesetzter_table3 = customtkinter.CTkEntry(self.dialog_table3)
        self.vorgesetzter_table3.grid(row=3, column=1, pady=4)

        self.selected_table3 = self.treeview_struktur.focus()
        self.values_table3 = self.treeview_struktur.item(self.selected_table3, 'values')

        self.dialog_table3.title(f"{self.values_table3[0]} {self.values_table3[1]}")

        self.vorname_table3.insert(0, self.values_table3[0])
        self.nachname_table3.insert(0, self.values_table3[1])
        self.abteilung_table3.insert(0, self.values_table3[2])
        self.vorgesetzter_table3.insert(0, self.values_table3[3])

        self.confirm_button_table3 = customtkinter.CTkButton(self.dialog_table3, text="OK",
                                                             command=self.update_record_table_3).grid(row=5, column=1,
                                                                                                      pady=(30, 4))

        self.delete_button_table3 = customtkinter.CTkButton(self.dialog_table3, text="Löschen", fg_color="#C52233",
                                                            hover_color="#F31B31",
                                                            command=self.delete_command_table3).grid(row=6, column=1,
                                                                                                     pady=4)

    def update_record_table_3(self):
        self.treeview_struktur.item(self.selected_table3, text="",
                                    values=(self.vorname_table3.get(),
                                            self.nachname_table3.get(),
                                            self.abteilung_table3.get(),
                                            self.vorgesetzter_table3.get()))

        update_record_3 = cursor_position.execute(f"""UPDATE Mitarbeiter SET Vorname = '{self.vorname_table3.get()}',
                                                                                    Nachname = '{self.nachname_table3.get()}',
                                                                                    Abteilung='{self.abteilung_table3.get()}',
                                                                                    Vorgesetzter='{self.vorgesetzter_table3.get()}'
                                                                                    WHERE Vorname = '{self.values_table3[0]} '
                                                                                    AND Nachname = '{self.values_table3[1]}'
                                                                                    AND Abteilung = '{self.values_table3[2]}'
                                                                                    AND Vorgesetzter = '{self.values_table3[3]}'""")
        update_record_3.commit()
        self.dialog_table3.destroy()
        self.third_frame_table_3()

    def delete_command_table3(self):

        delete_bestaetigen = messagebox.askyesno("Bitte bestätigen",
                                                 f"Sind Sie sicher, dass Sie den Mitarbeiter {self.values_table3[0]} {self.values_table3[1]} löschen möchten?")

        if delete_bestaetigen:
            delete_table3_string = cursor_position.execute(
                f"""DELETE FROM Mitarbeiter WHERE Vorname = '{self.vorname_table3.get()}' AND Nachname='{self.nachname_table3.get()}'""")

            self.treeview_struktur.delete(self.selected_table3)
            delete_table3_string.commit()
            self.dialog_table3.destroy()

        else:
            pass

    def select_table(self, table):

        self.third_frame_lager_button.configure(text_color=("black", "white"),
                                                fg_color=("gray75", "gray25") if table == "Table_1" else "transparent")
        self.third_frame_inventar_button.configure(text_color=("black", "white"),
                                                   fg_color=(
                                                   "gray75", "gray25") if table == "Table_2" else "transparent")
        self.third_frame_mitarbeter_button.configure(text_color=("black", "white"), fg_color=(
            "gray75", "gray25") if table == "Table_3" else "transparent")

        if table == "Table_1":
            self.third_frame_table1_frame.grid(columnspan=3, sticky="w")
            self.third_frame_table_1()
        else:
            self.third_frame_table1_frame.grid_forget()
        if table == "Table_2":
            self.third_frame_table2_frame.grid(columnspan=3, sticky="w")
            if len(self.search.get())==0:
                self.third_frame_table_2()

        else:
            self.third_frame_table2_frame.grid_forget()

        if table == "Table_3":
            self.third_frame_table3_frame.grid(columnspan=3, sticky="w")
            self.third_frame_table_3()
        else:
            self.third_frame_table3_frame.grid_forget()

    def table_1(self):
        self.select_table("Table_1")

    def table_2(self):
        self.select_table("Table_2")

    def table_3(self):
        self.select_table("Table_3")

        ############ FOURTH FRAME FUNKTIONS ############

    def mitarbeiter_add(self, vorname, nachname, abteilung):
        vorgesetzer_dict = {"Auftrag": "Svea Wolter",
                            "Außendienst": "Uwe Heermann",
                            "Buchhaltung": "Sven von Orsouw",
                            "Fertigung": "Ina Buch",
                            "IT-Abteilung": "Andre Gorbunov",
                            "Support": "Jan Weiske",
                            "Verwaltung": "Sven Raderschatt"}
        current_name = cursor_position.execute(f"SELECT CONCAT(Vorname, ' ', Nachname) FROM Mitarbeiter")
        repeat_liste = []
        for name in current_name:
            repeat_liste.append(*name)
        if vorname + ' ' + nachname in repeat_liste:
            self.four_frame_label_error.configure(text=f"Der Mitarbeiter {vorname} {nachname}\nexistiert bereits",
                                                  text_color="Yellow")
            self.four_frame_label_error.grid(row=5, column=0, padx=(255, 0), pady=(5, 0), columnspan=2)
            self.fourth_frame_vorname_entry.delete(0, "end")
            self.fourth_frame_nachname_entry.delete(0, "end")
            self.fourth_frame_abteilung_box.set("Bitte auswählen")

        elif len(vorname) > 0 and \
                len(nachname) > 0 and \
                abteilung != "Bitte auswählen":
            command_string = f"INSERT INTO Mitarbeiter (Vorname, Nachname, Abteilung, Vorgesetzter) VALUES ('{vorname}','{nachname}','{abteilung}','{vorgesetzer_dict[abteilung]}')"
            writing_data_mitarbeiter = cursor_position.execute(command_string)
            writing_data_mitarbeiter.commit()

            self.four_frame_label_hinzu = customtkinter.CTkLabel(self.fourth_frame,
                                                                 font=customtkinter.CTkFont(size=22),
                                                                 text_color="#9fd8cb",
                                                                 justify=customtkinter.LEFT,
                                                                 text=f"Mitarbeiter {vorname} {nachname}\n\nAbtelung:"
                                                                      f" {abteilung}\nVorgesetzter: {vorgesetzer_dict[abteilung]}\n\nwurde "
                                                                      f"erfolgreich hinzugefügt", anchor="w")
            self.four_frame_label_hinzu.grid(row=4, column=0, padx=(455, 0), columnspan=2, pady=(95, 0))
            self.fourth_frame_label_row.grid(row=4, column=0, padx=(55, 0), pady=(55, 0))
            self.four_frame_label_error.grid_forget()
            self.fourth_frame_vorname_entry.delete(0, "end")
            self.fourth_frame_nachname_entry.delete(0, "end")
            self.fourth_frame_abteilung_box.set("Bitte auswählen")
        else:
            self.four_frame_label_error.configure(text="Bitte füllen Sie alle Felder aus", text_color="red")
            self.four_frame_label_error.grid(row=5, column=0, padx=(255, 0), pady=(5, 0), columnspan=2)

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
            if len(self.second_frame_leer_table.get_children()) == 0:
                self.second_frame_lager_tabelle()
        else:
            self.second_frame.grid_forget()
        if name == "Button_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
            self.third_frame_table_1()
            self.third_frame_table_2()
            self.third_frame_table_3()
            self.search_function()
        else:
            self.third_frame.grid_forget()
        if name == "Button_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

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
    connection.close()


#pyinstaller --noconfirm --onedir --windowed --add-data "C:/Users/dbondarenko/pycharmprojects/pythonproject/venv/lib/site-packages/customtkinter;customtkinter/" "C:/Users/dbondarenko/PycharmProjects/pythonProject/Learn/SQL/Argen_Inventar.py"
