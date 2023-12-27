import customtkinter

class Label:

    def printer(self):
        global label
        label = customtkinter.CTkLabel(self, text="Hallo Daniel")
        label.grid()
        return label

    def delete(self):
        label.grid_forget()
