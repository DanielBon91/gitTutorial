import customtkinter
from erst import Label

class App(customtkinter.CTk):

    def __init__(self, master=None, width=400, height=400):
        super().__init__(master)

        self.geometry(f"{width}x{height}")



    def prin(self):
        self.btn = customtkinter.CTkButton(self, text="PUSH")
        self.btn.grid(row=0, column=0)
        self.btn = customtkinter.CTkButton(self, text="WEG")
        self.btn.grid(row=1, column=0)






if __name__ == "__main__":
    app = App()
    app.prin()
    app.mainloop()

