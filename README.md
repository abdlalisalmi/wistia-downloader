# Wistia Downloader
Python script/GUIApp to download from wistia hosted videos

## Requirements
to run the program without problems you have to make sure you have this things in your machine.

for the script you just need :
> - python3
> - requests

for run the GUIApp you need :
> - python3
> - requests
> - tkinter

## install tkinter :
as we say before, to run the GUIApp you need also the library tkinter, now we will explain how to install it.
### Windows:
Tkinter (and, since Python 3.1, ttk) are included with all standard Python distributions, The Tkinter library is built-in with every Python installation. And since you are on Windows, I believe you installed Python through the binaries on their website?
### MacOS:
If you are using a Python from any current python.org Python installer for macOS (3.8.0+, 3.7.2+, 3.6.8, or 2.7.16+), no further action is needed to use tkinter.
### Linux:
Actually, you just need to use the following to install the tkinter
>sudo apt-get install python3-tk

In addition, for Fedora users, use the following command:
>sudo dnf install python3-tkinter

## Images from the GUIApp:
<img align="center" alt="Python" width="512px" src="https://i.imgur.com/P4kpFQS.png" />

## Features:
- Download all video Automatique
- You can see the download progress
- You can choose the video resolution

## How to use

### step 1: (Install requests)
>pip install requests==2.20.0

### step 2: (Cloning the script)
>git clone https://github.com/abdlalisalmi/wistia-downloader.git</br>
>cd wistia-downloader</br>

### step 3: (Grabbing the videos id)
![](https://media.giphy.com/media/YkJhH3iHcuXNaeRBCR/giphy.gif)

### step 4: (adding the IDs)
for the script you need to add the IDs in  video_ID.txt file, but in the GUIApp you will find the IDs input filed.

### step 5: (Execute the script/GUIApp)

#### The GUIApp:
>python3 GUIApp/start.py

#### The script
>cd script
>python3 wistia-downloader.py</br>

## Created by 

[Abdelaali es salmi](https://github.com/salmiabdlali) &
[Amine tahiri](https://github.com/aminetahiri1998)
