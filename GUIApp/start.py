from GUI import WistiaDownloaderGUI
from tkinter import *


App = Tk()

# screen_width = int(root.winfo_screenwidth() * 0.5)
# screen_height = int(root.winfo_screenheight() * 0.65)

screen_width = 720
screen_height = 510

App.title('Wistia Downloader')
App.geometry("{}x{}".format(screen_width, screen_height))
App.resizable(False, False)

GUI = WistiaDownloaderGUI(App, screen_width, screen_height)

App.mainloop()
