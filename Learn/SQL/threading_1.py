import tkinter as tk
import threading
import time
class MyApp:

    def __init__(self, master):
        self.master = master
        self.progress = tk.DoubleVar()
        self.progress_bar = tk.Progressbar(self.master, variable=self.progress)
        self.progress_bar.pack()

        # создание потока для загрузки виджетов
        self.load_widgets_thread = threading.Thread(target=self.load_widgets)
        self.load_widgets_thread.start()

        # создание потока для обновления прогресс бара
        self.update_progress_thread = threading.Thread(target=self.update_progress)
        self.update_progress_thread.start()

    def load_widgets(self):
        # загрузка большого количества виджетов
        # ...
        print(1)
    def update_progress(self):
        while self.load_widgets_thread.is_alive():
            self.progress.set(self.get_progress())
            self.master.update()
            time.sleep(0.1)

    def get_progress(self):
        # возвращает процент загрузки виджетов
        # ...

root = tk.Tk()
app = MyApp(root)
root.mainloop()
