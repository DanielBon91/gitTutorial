import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Переменные для хранения координат при перемещении окна
        self.x = 0
        self.y = 0

        # Создаем фрейм для заголовка окна
        self.title_bar = tk.Frame(self, bg='gray')
        self.title_bar.pack(side='top', fill='x')

        # Создаем кнопку для закрытия окна
        self.close_btn = tk.Button(self.title_bar, text='X', command=self.destroy)
        self.close_btn.pack(side='right')

        # Назначаем обработчики событий для перемещения окна
        self.title_bar.bind('<ButtonPress-1>', self.start_move)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_move)
        self.title_bar.bind('<B1-Motion>', self.move_window)

        # Настраиваем окно
        self.geometry('400x300+200+200')
        self.overrideredirect(True)

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


if __name__ == '__main__':
    app = App()
    app.mainloop()
