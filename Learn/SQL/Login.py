import customtkinter
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CustomTkinter example_background_image.py")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="CustomTkinter\nLogin Page",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

        # create main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=9)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.main_label = customtkinter.CTkLabel(self.main_frame, text="CustomTkinter\nMain Page",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))

        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.back_event, width=200)
        self.back_button.grid(row=0, column=1, padx=30, pady=(15, 15))



        self.navi_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0)
        self.navi_frame.grid(row=0, column=0, sticky="nsew")

        self.navi_frame.grid_rowconfigure(5, weight=1)
        self.navi_frame.grid(row=0, column=0)

        self.btn1 = customtkinter.CTkButton(self.navi_frame, text="BTN1")
        self.btn1.grid(row=0, column=1, sticky="ew", padx=15, pady=15)
        self.btn2 = customtkinter.CTkButton(self.navi_frame, text="BTN2")
        self.btn2.grid(row=1, column=1, sticky="ew", padx=15, pady=15)
        self.btn3 = customtkinter.CTkButton(self.navi_frame, text="BTN3")
        self.btn3.grid(row=2, column=1, sticky="ew", padx=15, pady=15)
        self.btn4 = customtkinter.CTkButton(self.navi_frame, text="BTN4")
        self.btn4.grid(row=3, column=1, sticky="ew", padx=15, pady=15)
        self.btn5 = customtkinter.CTkButton(self.navi_frame, text="BTN5")
        self.btn5.grid(row=6, column=1, sticky="s", padx=15, pady=15)

    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

        self.login_frame.grid_forget()  # remove login frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

    def back_event(self):
        self.main_frame.grid_forget()  # remove main frame
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame


if __name__ == "__main__":
    app = App()
    app.mainloop()