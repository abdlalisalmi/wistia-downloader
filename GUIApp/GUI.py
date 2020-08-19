from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter.ttk import Progressbar

import os
import sys
import time

from Core import WistiaDownloaderCore


class WistiaDownloaderGUI():
    def __init__(self, master, screen_width, screen_height):
        self.master = master

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.borderX = int(screen_width * 0.06)
        self.borderY = int(screen_width - (screen_width * 0.06))

        self.btnBorderX = int(self.screen_width / 2.5)
        self.btnBorderY = int(self.screen_height / 5)

        self.IDsList = []
        self.resolution = "224p"
        self.downloadFolder = None

        self.showLogo()
        self.showTextInput()
        self.showExportandImmport()
        self.showResolutionSelect()
        self.showDownloadFolderSelect()
        self.showDownloadBtn()
        self.showLogs()
        self.showProgressBar()
        self.showQuitBtn()

    def showLogo(self):
        Label(self.master, text="Wistia Downloader ",
              fg='#574b90', font=('Helvetica', 30)).place(x=int(self.screen_width/3.6), y=15)
        Label(self.master, text="https://github.com/abdlalisalmi",
              fg='#786fa6', font=("Arial Bold", 10)).place(x=int(self.screen_width/3.6) + 5, y=55)

    def showExportandImmport(self):
        # Exporting the IDs in a file
        def exportIDsToFile():
            self.dataCollection()
            if self.IDsList:
                exportedFile = filedialog.asksaveasfile(
                    mode='w', defaultextension=".txt")
                if exportedFile:
                    for ID in self.IDsList:
                        exportedFile.write('{}\n'.format(ID))
                    Label(self.master, text='PATH: {}'.format(exportedFile.name),
                          fg='#2c3e50', font=("Arial Bold", 7)).place(x=self.borderX - 5, y=465)
                    exportedFile.close()

                    messagebox.showinfo("Wistia Downloader",
                                        "You IDs is exported.")
            else:
                messagebox.showinfo("Wistia Downloader",
                                    "You IDs field is empty.")
        Button(
            self.master, font=("Arial Bold", 8), fg="white",
            bg='#575fcf', text="Export",
            command=exportIDsToFile
        ).place(x=self.borderX + 120, y=430)
        ################################

        # Importing the IDs from a file
        def importIDsFromFile():
            filePATH = filedialog.askopenfilename(
                initialdir=os.path.dirname(os.path.realpath(__file__)),
                title="Select file",
                filetypes=(("text files", "*.txt"),)
            )
            if filePATH:
                with open(filePATH, 'r') as f:
                    content = f.read().split('\n')
                    content = list(filter(None, content))
                    str_content = ""
                    for id in content:
                        str_content += id + '\n'
                    self.textArea.insert(END, str_content)

        Button(
            self.master, font=("Arial Bold", 8),
            fg="white", bg='#575fcf',
            text="Import", command=importIDsFromFile
        ).place(x=self.borderX + 20, y=430)

    def showTextInput(self):

        self.showBorder(self.borderX, self.btnBorderY+10, width=25, height=2)

        self.textInputLable = Label(self.master, text="Enter The IDs:",
                                    fg='#303952', font=("Arial Bold", 10))
        self.textInputLable.place(x=self.borderX, y=self.btnBorderY)

        self.textArea = Text(self.master, bg='#dff9fb', borderwidth=2, height=19,
                             width=25, font=("Arial Bold", 9))
        self.textArea.place(x=self.borderX, y=130)
        self.textArea.focus()
        self.textArea.insert(
            END, "cu1xdspoew")

    def showBorder(self, x, y, height=2, width=48):
        Label(self.master,
              borderwidth=2,
              width=width,
              height=height,
              relief="ridge",).place(x=x, y=y)

    def showResolutionSelect(self):
        self.showBorder(self.btnBorderX, self.btnBorderY+10)
        resolutionLable = Label(self.master,
                                text="Select The Resolution:",
                                fg='#303952', font=("Arial Bold", 10))
        resolutionLable.place(x=self.btnBorderX, y=self.btnBorderY)

        self.resolutions_list = {"224p": "224p",
                                 "360p": "360p",
                                 "540p": "540p",
                                 "720p": "720p",
                                 "Best Quality": "Best Quality"}

        def choiceClicked():
            self.resolution = choice.get()
        choice = StringVar(self.master, "224p")
        x = self.btnBorderX + 6
        for (resolution, value) in self.resolutions_list.items():
            Radiobutton(self.master,
                        text=resolution,
                        variable=choice,
                        value=value,
                        command=choiceClicked
                        ).place(x=x, y=self.btnBorderY + 20)
            x = x + 65

    def showDownloadFolderSelect(self):
        self.showBorder(self.btnBorderX, y=self.btnBorderY + 75)

        def selectDownloadFolder():
            self.downloadFolder = filedialog.askdirectory()
            try:
                self.downloadPATH.destroy()
            except:
                pass
            self.downloadPATH = Label(self.master, text=self.downloadFolder,
                                      fg='#303952', font=("Arial Bold", 7))
            self.downloadPATH.place(
                x=self.btnBorderX + 5, y=self.btnBorderY + 90)

        folderLable = Label(self.master, text="Select The Download Folder:",
                            fg='#2c3e50', font=("Arial Bold", 10))
        folderLable.place(x=self.btnBorderX, y=self.btnBorderY + 65)

        self.selectDownloadFolderBtn = Button(
            self.master, font=("Arial Bold", 9),
            fg="white", bg='#6a89cc', text="Browse",
            command=selectDownloadFolder
        )
        self.selectDownloadFolderBtn.place(
            x=self.btnBorderX + 310, y=self.btnBorderY + 80)

    def showDownloadBtn(self):
        self.showBorder(self.btnBorderX, y=self.btnBorderY + 140, height=10)

        Label(self.master, text="Download:",
              fg='#303952', font=("Arial Bold", 10)
              ).place(x=self.btnBorderX, y=self.btnBorderY + 130)
        self.downloadBtn = Button(
            self.master, text="Start Download",
            fg="white", bg='#079992',
            command=self.download
        )
        self.downloadBtn.place(x=self.btnBorderX + 253,
                               y=self.btnBorderY + 150)

    def showQuitBtn(self):
        frame = Frame(self.master)
        frame.place(x=int(self.screen_width - (self.borderX * 2)),
                    y=int(self.screen_height - (self.borderX * 1.2)))
        self.quit = Button(frame,
                           text="QUIT", fg="white", bg='#ff3f34',
                           command=frame.quit)
        self.quit.grid(row=0, column=0)

# the function called when we click on Start Download button
    def download(self):
        self.downloadBtn['state'] = DISABLED
        self.dataCollection()
        core = WistiaDownloaderCore(
            self.master, self.IDsList,
            self.resolution, self.downloadFolder,
            self.btnBorderX, self.btnBorderY,
        )
        self.downloadBtn['state'] = NORMAL

# When we click on download btn or export btn,
# this function well be called for collect the IDs and convert them to a list
    def dataCollection(self):
        self.IDsList = self.textArea.get("1.0", "end").split('\n')
        self.IDsList = list(filter(None, self.IDsList))

    def showProgressBar(self):
        self.progressBar = Progressbar(self.master, length=300)
        self.progressBar['value'] = 0

        self.progressLabel = Label(self.master, text='0%',
                                   fg='#2c3e50', font=("Arial Bold", 10))
        self.progressLabel.place(
            x=self.btnBorderX + 10, y=self.btnBorderY + 210)
        Label(self.master, text="100%",
              fg='#2c3e50', font=("Arial Bold", 10)).place(x=self.btnBorderX + 340, y=self.btnBorderY + 210)

        self.progressBar.place(x=self.btnBorderX + 40, y=self.btnBorderY + 210)

    def showLogs(self):
        self.logsLabel = Label(self.master, text='Logs:',
                               fg='#2c3e50', font=("Arial Bold", 10))
        self.logsLabel.place(
            x=self.btnBorderX + 10, y=self.btnBorderY + 245)

        self.logsField = Text(self.master, background='#d1d8e0', borderwidth=2, height=3,
                              width=52, font=("Arial Bold", 8))
        self.logsField.place(x=self.btnBorderX + 10, y=self.btnBorderY + 265)
        self.logsField.config(state=DISABLED)
