import customtkinter as ctk
import configparser
import openpyxl
import Image

config = configparser.ConfigParser()
config.read("configuration.ini", encoding='utf-8')
class InkaCam(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.book = openpyxl.open(config['datei']['file'], read_only=True)
        self.sheet = self.book.active
        self.main_list = []
        for rows in self.sheet.iter_rows(min_row=2, min_col=0):
            sublist = []
            for column in rows:
                sublist.append(column.value)
            self.main_list.append(sublist)
        self.book.close()

        self.image = ctk.CTkImage(Image.open("logo.png"), size=(300,50))
        """Windows geometry"""

        self.geometry("1920x1080+1+1")
        self.config(bg='black')
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((0,2), weight=0)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_columnconfigure((0,1), minsize=960)

        """Windows elemente"""

        #self.wilkommen = ctk.CTkLabel(self,text="Scannen Sie bitte den Artikel", bg_color='gray', font=ctk.CTkFont('Calibri', 150, 'bold'))
        #self.wilkommen.grid(row=1, column=0)
        self.lbl_up_left = ctk.CTkLabel(self, text="65412", height=150, fg_color="gray25", bg_color='black',
                                        text_color="white", corner_radius=50, font=ctk.CTkFont('Verdana ', 100, 'bold'))
        self.lbl_up_left.grid(row=0, column=0, padx=160, pady=(25, 15), sticky='we')
        self.lbl_up_right = ctk.CTkLabel(self, text="Vorne", height=150, fg_color="#64D86E", bg_color='black',
                                         text_color="white", corner_radius=50, font=ctk.CTkFont('Verdana ', 100, 'bold'))
        self.lbl_up_right.grid(row=0, column=1, padx=160, pady=(25, 15), sticky='we')
        #"#64D86E"
        self.lbl_middle = ctk.CTkLabel(self, text="C-3", height=150, fg_color="#F7996E", bg_color='black',
                                         text_color="white", corner_radius=50, font=ctk.CTkFont('Courier ', 800, 'bold'))
        self.lbl_middle.grid(row=1, column=0, columnspan=2, padx=160, pady=(15,25), sticky='NSEW')
        self.lbl_image = ctk.CTkLabel(self, text='', image=self.image, bg_color="black").grid(row=2, column=1, sticky="se", pady=(15, 30), padx=25)

        self.entry = ctk.CTkEntry(self, fg_color='black', font=ctk.CTkFont('Verdana ', 11, 'bold'))
        self.update()
        self.entry.focus_set()
        self.entry.grid(row=3, column=0, columnspan=2, pady=10)

        self.entry.bind('<Return>', self.get)
        self.bind('<Escape>', quit)

    def get(self, event):
        print(1)

if __name__ == "__main__":
    inkacam = InkaCam()
    inkacam.mainloop()

