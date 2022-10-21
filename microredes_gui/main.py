from tkinter import Tk

from microredes_gui.ui import tabs

class Main():
    def __init__(self):
        pass

    def open_window(self):
        self.root = Tk()
        self.root.title("CAN Sender-Receiver")
        # self.root.iconbitmap("./assets/1.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.resizable(0,0)


        self.tabs = tabs.Tabs(self.root)
        self.tabs.create_menu()
        self.tabs.create_footer()

        self.root.mainloop()

    def close_window(self):
        self.root.destroy()