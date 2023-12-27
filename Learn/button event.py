import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

root = tk.Tk()

# Создаем первую кнопку
button1 = MyButton(root, text='Кнопка 1')
button1.pack()

# Создаем вторую кнопку
button2 = MyButton(root, text='Кнопка 2')
button2.pack()

root.mainloop()