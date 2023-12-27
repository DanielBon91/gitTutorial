import tkinter as tk
import tkinter.ttk as ttk

class CustomTreeView(ttk.Treeview):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.custom_attribute = "Custom attribute"

    def custom_method(self):
        print("Custom method called")