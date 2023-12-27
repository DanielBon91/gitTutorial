import datetime
import subprocess

import customtkinter
from PIL import Image
from docxtpl import DocxTemplate

date_now  = datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y")

class Todo(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("ToDo")
        self.geometry("420x910")
        #self.wm_attributes("-topmost", True)
        #self.overrideredirect(True)

        self.bind("<Escape>", self._exit)
        self.my_dir = r"C:\Users\dbondarenko\Desktop\MyTodo"

        img_word = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//Desktop//MyTodo//print.png"),
                                          size=(20, 20))
        img_save = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//Desktop//MyTodo//save.png"),
                                          size=(20, 20))

        self.grid_columnconfigure(0, weight=1)

        self.label_allgemein = customtkinter.CTkLabel(self, text="Allgemein").grid(row=0, pady=(10, 0))
        self.label_andre = customtkinter.CTkLabel(self, text="Andre").grid(row=2)
        self.label_dringend = customtkinter.CTkLabel(self, text="Dringend").grid(row=4)

        self.field_allgemein = customtkinter.CTkTextbox(self, width=400, height=250, fg_color="white",
                                                        text_color="black", corner_radius=5)
        self.field_allgemein.grid(row=1)
        self.field_andre = customtkinter.CTkTextbox(self, width=400, height=250, fg_color="white", text_color="black",
                                                    corner_radius=5)
        self.field_andre.grid(row=3)
        self.field_dringend = customtkinter.CTkTextbox(self, width=400, height=250, fg_color="white",
                                                       text_color="black", corner_radius=5)
        self.field_dringend.grid(row=5)

        self.btn_word = customtkinter.CTkButton(self, text="", image=img_word, width=55,
                                                command=self.word_command).grid(row=6, column=0, pady=10, padx=(0, 12),
                                                                                sticky="e")
        self.btn_save = customtkinter.CTkButton(self, text="", image=img_save, width=55, command=self.save_button).grid(
            row=6, column=0, pady=10, padx=(200, 0))

        self.insert_data("allgemein", self.field_allgemein)
        self.insert_data("andre", self.field_andre)
        self.insert_data("dringend", self.field_dringend)

        self.protocol("WM_DELETE_WINDOW", self.quit_command)



    def insert_data(self, file, field):

        with open(fr"{self.my_dir}\{file}.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            lines.reverse()
            for row in lines:
                field.insert("0.0", row.strip() + "\n")

    def save(self, file, getting):

        with open(fr"{self.my_dir}\{file}.txt", "w", encoding="utf-8") as txt_file:
            for row in getting:
                txt_file.write(row)

    def save_button(self):

        self.save("allgemein", self.field_allgemein.get('0.0', 'end').strip())
        self.save("andre", self.field_andre.get('0.0', 'end').strip())
        self.save("dringend", self.field_dringend.get('0.0', 'end').strip())

        self.backup(self.field_allgemein.get('0.0', 'end').strip(),
                    self.field_andre.get('0.0', 'end').strip(),
                    self.field_dringend.get('0.0', 'end').strip())

    def word_command(self):

        dict = {"allgemein": f"{self.field_allgemein.get('0.0', 'end')}",
                "andre": f"{self.field_andre.get('0.0', 'end')}",
                "dringend": f"{self.field_dringend.get('0.0', 'end')}"}

        doc = DocxTemplate(r"C://Users//dbondarenko//Desktop//MyTodo//TODO.docx")
        doc.render(dict)
        doc.save(r"C://Users//dbondarenko//Desktop//MyTodo//TODO_2.docx")

        subprocess.Popen(['start', fr"{self.my_dir}\TODO_2.docx"], shell=True)

    def quit_command(self):

        self.save("allgemein", self.field_allgemein.get('0.0', 'end').strip())
        self.save("andre", self.field_andre.get('0.0', 'end').strip())
        self.save("dringend", self.field_dringend.get('0.0', 'end').strip())

        self.backup(self.field_allgemein.get('0.0', 'end').strip(),
                    self.field_andre.get('0.0', 'end').strip(),
                    self.field_dringend.get('0.0', 'end').strip())

        self.quit()

    def _exit(self, e):
        self.quit_command()

    def backup(self, allgemein, andre, dringend):
        with open(r"C://Users//dbondarenko//Desktop//MyTodo//backup.txt", "a", encoding="utf-8") as backup_file:
            backup_file.write("\n\n\n" + date_now + "\n\n")
            backup_file.write("\n\nAllgemein\n\n")
            for row in allgemein:
                backup_file.write(row)
            backup_file.write("\n\nAndre\n\n")
            for row in andre:
                backup_file.write(row)
            backup_file.write("\n\nDringend\n\n")
            for row in dringend:
                backup_file.write(row)


if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()
