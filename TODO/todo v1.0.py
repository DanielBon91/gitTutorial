import datetime
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import configparser

date_now  = datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y")
config = configparser.ConfigParser()
config.read('dir.ini')
class Todo(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("To-Do List")
        self.geometry("300x560")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.iconbitmap(config['directory']['icon_img'])
        img_config = ctk.CTkImage(Image.open(config['directory']['config_img']), size=(20, 20))
        img_save = ctk.CTkImage(Image.open(config['directory']['save_img']), size=(20, 20))

        self.field = ctk.CTkTextbox(self, fg_color="white", text_color="black", corner_radius=5)
        self.field.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.file_dir = ctk.CTkButton(self, text="", width=25, image=img_config,
                                      command=self.open_file).grid(row=1, column=0, padx=55, pady=(0, 10), sticky="e")
        self.save_btn = ctk.CTkButton(self, text="", width=25, image=img_save,
                                      command=self.save_file).grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")
        self.insert_datei()

        self.protocol("WM_DELETE_WINDOW", self.quit_command)
    def open_file(self):
        file_path = filedialog.askopenfilename()
        config.set('directory', 'main_dir', file_path)

        with open('dir.ini', "w", encoding="utf-8") as config_file:
            config.write(config_file)
        self.insert_datei()

    def save_file(self):
        with open(config['directory']['main_dir'], "w", encoding="utf-8") as txt_file:
            for row in self.field.get('0.0', 'end').strip():
                txt_file.write(row)
        self.backup()

    def insert_datei(self):
        self.field.delete("0.0", "end")
        with open(config['directory']['main_dir'], "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            lines.reverse()
            for row in lines:
                self.field.insert("0.0", row.strip() + "\n")

    def backup(self):
        with open(config['directory']['archiv_dir'], "a", encoding="utf-8") as backup_file:
            backup_file.write("\n\n\n" + date_now + "\n\n")
            for row in self.field.get('0.0', 'end').strip():
                backup_file.write(row)
    def quit_command(self):
        self.save_file()
        self.backup()
        self.quit()

if __name__ == "__main__":
    app = Todo()
    app.mainloop()