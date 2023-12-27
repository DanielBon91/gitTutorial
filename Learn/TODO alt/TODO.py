import subprocess
import customtkinter
from PIL import Image
from docxtpl import DocxTemplate

class Todo(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("ToDo")
        self.geometry("255x487")
        self.wm_attributes("-topmost", True)
        self.overrideredirect(True)

        self.bind("<Escape>", self._exit)
        self.my_dir = r"C:\Users\dbondarenko\Desktop\MyTodo"

        img_word = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//Desktop//MyTodo//print.png"),
                                     size=(20, 20))
        img_save = customtkinter.CTkImage(Image.open(r"C://Users//dbondarenko//Desktop//MyTodo//save.png"),
                                     size=(20, 20))

        self.title_bar = customtkinter.CTkFrame(self, height=25, corner_radius=0)
        self.title_bar.grid(sticky="nwe")
        self.title_bar.bind('<ButtonPress-1>', self.start_move)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_move)
        self.title_bar.bind('<B1-Motion>', self.move_window)

        self.grid_columnconfigure(0, weight=1)

        self.label_allgemein = customtkinter.CTkLabel(self, text="Allgemein").grid(row=0, pady=(25,0))
        self.label_andre = customtkinter.CTkLabel(self, text="Andre").grid(row=2)
        self.label_dringend = customtkinter.CTkLabel(self, text="Dringend").grid(row=4)

        self.field_allgemein = customtkinter.CTkTextbox(self, width=230, height=110, fg_color="white", text_color="black", corner_radius=5)
        self.field_allgemein.grid(row=1)
        self.field_andre = customtkinter.CTkTextbox(self, width=230, height=110, fg_color="white", text_color="black", corner_radius=5)
        self.field_andre.grid(row=3)
        self.field_dringend = customtkinter.CTkTextbox(self, width=230, height=110, fg_color="white", text_color="black", corner_radius=5)
        self.field_dringend.grid(row=5)

        self.btn_word = customtkinter.CTkButton(self, text="", image=img_word, width=55, command=self.word_command).grid(row=6, column=0, pady=10, padx=(0, 12), sticky="e")
        self.btn_save = customtkinter.CTkButton(self, text="", image=img_save, width=55, command=self.save_button).grid(row=6, column=0, pady=10, padx=(67, 0))

        self.insert("allgemein", self.field_allgemein)
        self.insert("andre", self.field_andre)
        self.insert("dringend", self.field_dringend)

    def insert(self, file, field):

        with open(fr"{self.my_dir}\{file}.txt", "r", encoding="utf-8") as txt_file:
            for row in txt_file:
                field.insert("0.0", row.strip() + "\n")

    def save(self, file, getting):

        with open(fr"{self.my_dir}\{file}.txt", "w", encoding="utf-8") as txt_file:
            for row in getting:
                txt_file.write(row)

    def word_command(self):

        dict = {"allgemein": f"{self.field_allgemein.get('0.0', 'end')}",
                     "andre": f"{self.field_andre.get('0.0', 'end')}",
                     "dringend": f"{self.field_dringend.get('0.0', 'end')}"}

        doc = DocxTemplate(r"C://Users//dbondarenko//Desktop//MyTodo//TODO.docx")
        doc.render(dict)
        doc.save(r"C://Users//dbondarenko//Desktop//MyTodo//TODO_2.docx")

        subprocess.Popen(['start', fr"{self.my_dir}\TODO_2.docx"], shell=True)

    def _exit(self, e):

        self.save("allgemein", self.field_allgemein.get('0.0', 'end').strip())
        self.save("andre", self.field_andre.get('0.0', 'end').strip())
        self.save("dringend", self.field_dringend.get('0.0', 'end').strip())

        self.quit()

    def save_button(self):

        self.save("allgemein", self.field_allgemein.get('0.0', 'end').strip())
        self.save("andre", self.field_andre.get('0.0', 'end').strip())
        self.save("dringend", self.field_dringend.get('0.0', 'end').strip())

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def move_window(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

if __name__=="__main__":
    todo = Todo()
    todo.mainloop()

