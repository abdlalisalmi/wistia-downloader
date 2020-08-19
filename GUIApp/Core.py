from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import os
import time
import sys
import json
import requests
from shutil import copy


class WistiaDownloaderCore():
    def __init__(self, master, IDsList, resolution, downloadFolder, btnBorderX, btnBorderY):
        self.master = master
        self.IDsList = IDsList
        self.resolution = resolution
        self.resolution_list = ["224p", "360p", "540p", "720p", "Best Quality"]
        self.downloadFolder = downloadFolder
        self.URL = "http://fast.wistia.net/embed/iframe/"
        self.videoIndex = 1
        self.logs = ""

        self.btnBorderX = btnBorderX
        self.btnBorderY = btnBorderY

        if self.dataCheck():
            for ID in self.IDsList:
                videoURL = self.URL + ID
                html_file = self.download_HTML_file(videoURL)
                self.html_page_handle_and_download(html_file, self.resolution)
            try:
                self.downloadLable.configure(text='Download Completed')
            except:
                pass
            messagebox.showinfo(
                "Wistia Downloader", "Download completed, check logs for any error.")

    def dataCheck(self):
        if not self.IDsList:
            messagebox.showinfo(
                "Wistia Downloader", "You need to enter at least one ID.")
            return 0
        if not self.resolution in self.resolution_list:
            messagebox.showinfo(
                "Wistia Downloader", "You have to select a resolution from the list.")
            return 0
        if not self.downloadFolder:
            messagebox.showinfo(
                "Wistia Downloader", "You need to select the download folder.")
            return 0
        return 1

    def download_HTML_file(self, url):
        local_filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename

    def html_page_handle_and_download(self, file_name, resolution):
        with open(file_name, "r") as file:
            i = 1
            for con in file:
                # ERROR
                if i == 1 and con == '{"error":true,"iframe":true}':
                    video_data = con
                if i == 63:
                    video_data = con
                    break
                i += 1
            if video_data == '{"error":true,"iframe":true}':
                self.logs += 'ID number {}, is not valid.\n'.format(
                    self.videoIndex)
                self.showLogs(self.logs)
                self.videoIndex += 1
            else:
                video_data = video_data.split('[')[1].split(']')[0]
                video_data = video_data.replace('},{', '}abdlalisalmi{')
                video_data_list = video_data.split('abdlalisalmi')

                video_url = None
                for video in video_data_list:
                    video_data_json = json.loads(video)
                    if video_data_json['display_name'] == resolution:
                        video_url = video_data_json['url']

                self.showProgressBar()
                self.downloadLable.configure(
                    text='Downloading Video {}...'.format(self.videoIndex))

                if (video_url):
                    video_name = self.download_video(video_url)

                    video_name_and_index = "Video{}.mp4".format(
                        str(self.videoIndex))
                    self.videoIndex += 1
                    os.rename(video_name, video_name_and_index)
                else:
                    video_url = json.loads(video_data_list[0])['url']
                    print(json.loads(video_data_list[0]))
                    video_name = self.download_video(video_url)

                    video_name_and_index = "Video{}.mp4".format(
                        str(self.videoIndex))
                    self.videoIndex += 1
                    os.rename(video_name, video_name_and_index)

        os.remove(file_name)

    def download_video(self, url):
        video_name = url.split('/')[-1]
        reponse = requests.get(url, stream=True)
        with open(video_name, 'wb') as video:
            total_length = int(reponse.headers.get('content-length'))
            total_received = 0
            for chunk in reponse.iter_content(chunk_size=1024):
                if chunk:
                    progress = ((total_received / total_length) * 100) + 1
                    self.progressBar['value'] = progress
                    self.progressLabel.configure(
                        text='{}%'.format(int(progress)))
                    self.progressBar.update()

                    video.write(chunk)
                    total_received += 1024

        return video_name

    def showProgressBar(self):
        self.progressBar = Progressbar(self.master, length=300)
        self.progressBar['value'] = 0

        self.downloadLable = Label(self.master, text="Downloading...",
                                   fg='#2c3e50', font=("Arial Bold", 10))
        self.downloadLable.place(
            x=self.btnBorderX + 10, y=self.btnBorderY + 187)

        self.progressLabel = Label(self.master, text='0%',
                                   fg='#2c3e50', font=("Arial Bold", 10))
        self.progressLabel.place(
            x=self.btnBorderX + 10, y=self.btnBorderY + 210)
        Label(self.master, text="100%",
              fg='#2c3e50', font=("Arial Bold", 10)).place(x=self.btnBorderX + 340, y=self.btnBorderY + 210)

        self.progressBar.place(x=self.btnBorderX + 40, y=self.btnBorderY + 210)

    def showLogs(self, error):
        self.errorLabel = Label(self.master, text='Logs:',
                                fg='#2c3e50', font=("Arial Bold", 10))
        self.errorLabel.place(
            x=self.btnBorderX + 10, y=self.btnBorderY + 245)

        self.errorField = Text(self.master, background="#ff7979", borderwidth=2, height=3,
                               width=52, font=("Arial Bold", 8))
        self.errorField.place(x=self.btnBorderX + 10, y=self.btnBorderY + 265)
        self.errorField.insert(
            END, error)
        self.errorField.config(state=DISABLED)
