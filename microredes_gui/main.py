from tkinter import Tk

from microredes_gui.ui import main_window

class Main():
    def __init__(self):
        pass

    def open_window(self):
        self.root = Tk()
        self.root.title("CAN Sender-Receiver")
        # self.root.iconbitmap("./assets/1.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (screen_width, screen_height))
        # self.root.resizable(0,0)

        self.main_window = main_window.Main_Window(self.root)
        self.main_window.create_menu()
        self.main_window.create_footer()

        self.root.mainloop()

    def close_window(self):
        self.main_window.disconnect()
        self.root.destroy()
