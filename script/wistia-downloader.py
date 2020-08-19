import os
import time
import sys
import json
import requests
import getpass
from shutil import copy
from clint.textui import progress  # for the progress effects

video_index = 1


def logo():
    sprint("""\033[1;33;40m
     _  _  _ _           _          _____
    | || || (_)     _   (_)        (____ \\
    | || || |_  ___| |_  _  ____    _   \ \ ___  _ _ _ ____
    | ||_|| | |/___)  _)| |/ _  |  | |   | / _ \| | | |  _ \\
    | |___| | |___ | |__| ( ( | |  | |__/ / |_| | | | | | | |
     \______|_(___/ \___)_|\_||_|  |_____/ \___/ \____|_| |_|
      https://github.com/abdlalisalmi
	\033[0;37;40m""", 0.1)


def sprint(string, tm=10):
    for c in string + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(tm / 100)


def download_video(url):
    video_name = url.split('/')[-1]
    reponse = requests.get(url, stream=True)
    with open(video_name, 'wb') as video:
        total_length = int(reponse.headers.get('content-length'))
        for chunk in progress.bar(reponse.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                video.write(chunk)
                video.flush()
    return video_name


def html_page_handle_and_download(file_name, resolution):
    print("\033[1;32;40m")
    global video_index
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
            sprint("\033[1;31;40mYour video id is not valid\033[0;37;40m", 2)
        else:
            video_data = video_data.split('[')[1].split(']')[0]
            video_data = video_data.replace('},{', '}abdlalisalmi{')
            video_data_list = video_data.split('abdlalisalmi')

            resolution_dic = {
                '1': '224p',
                '2': '360p',
                '3': '540p',
                '4': '720p',
                '5': 'Original file'
            }
            video_url = None
            for video in video_data_list:
                video_data_json = json.loads(video)
                if video_data_json['display_name'] == resolution_dic[str(resolution)]:
                    video_url = video_data_json['url']
            if (video_url):
                video_name = download_video(video_url)

                video_name_and_index = "Video{}.mp4".format(str(video_index))
                video_index += 1
                os.rename(video_name, video_name_and_index)
            else:
                print(
                    "\033[1;31;40mThe resulotion ({}) does not exist for this video, we will download it with the original resolution.\033[0;37;40m".format(resolution_dic[str(resolution)]))
                video_url = json.loads(video_data_list[0])['url']
                print(json.loads(video_data_list[0]))
                video_name = download_video(video_url)

                video_name_and_index = "Video{}.mp4".format(str(video_index))
                video_index += 1
                os.rename(video_name, video_name_and_index)

    os.remove(file_name)
    print("\033[0;37;40m")


def download_folder():
    try:
        username = getpass.getuser()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        sprint(
            "\033[1;32;40mPlease enter the PATH of download folder: \033[0;37;40m", 2)
        sprint(
            "\033[1;31;40m\t\tExample: \033[0;37;40m/Users/{}/Desktop".format(username), 2)
        sprint(
            "\033[1;31;40m\t\tExample: \033[0;37;40m/Volumes/Storage/goinfre/{}".format(username), 2)
        sprint(
            "\033[1;31;40m\t\tExample: \033[0;37;40m{}".format(BASE_DIR), 2)

        folder_path = input("PATH: \033[1;33;40m")
        print("\033[0;37;40m")

        slash = '/' if '/' in folder_path else '\\'
        if folder_path[-1] == slash:
            folder_path += "wistia-downloader"
        else:
            folder_path += slash + "wistia-downloader"

        os.mkdir(folder_path)
        copy('video_ID.txt', folder_path)

        os.chdir("{}".format(folder_path))
        sprint("\033[1;33;40mYou will find the videos in  {}\033[0;37;40m".format(
            folder_path), 2)

    except FileNotFoundError:
        print("\033[1;31;40mThe PATH does not exist !! try again\033[0;37;40m")
        sprint(".....", 100)
        main()
    except FileExistsError:
        print(
            "\033[1;31;40mThe wistia-downloader folder is exist !! try another PATH\033[0;37;40m")
        sprint(".....", 100)
        main()


def resolution_select():
    resolution = 0
    print('')
    sprint(
        "\033[1;32;40mPlease select download resolution:\033[0;37;40m", 2)
    sprint(
        "\033[1;31;40m\t\t1) \033[0;37;40m224p", 2)
    sprint(
        "\033[1;31;40m\t\t2) \033[0;37;40m360p", 2)
    sprint(
        "\033[1;31;40m\t\t3) \033[0;37;40m540p", 2)
    sprint(
        "\033[1;31;40m\t\t4) \033[0;37;40m720p", 2)
    sprint(
        "\033[1;31;40m\t\t5) \033[0;37;40mBest Quality", 2)
    choices = ['1', '2', '3', '4', '5']
    while not resolution in choices:
        resolution = input('> ')
        if not resolution in choices:
            print('Please select a number between 1 and 5.')
    return int(resolution)


def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()

    url = "http://fast.wistia.net/embed/iframe/"

    i = 0
    with open("video_ID.txt", "r+") as video_id:
        if os.stat("video_ID.txt").st_size == 0:
            print("")
            sprint(
                "\033[1;31;40mThe file video_ID.txt is empty !!\033[0;37;40m", 0.2)
            sprint(".....", 100)
        else:
            start = time.time()
            download_folder()
            resolution = resolution_select()

            for id in video_id:

                if '\n' in id:
                    new_id = id[:-1]
                else:
                    new_id = id

                video_url = url + new_id
                local_filename = download_file(video_url)
                print("Video ID " + str(i + 1) +
                      "--------------------------------------------------------------------------")
                html_page_handle_and_download(
                    local_filename, resolution)
                i += 1

            end = time.time()
            sprint(
                "\033[1;33;40mDownload finished, Total time {}\033[0;37;40m".format(end - start), 2)


if __name__ == '__main__':
    main()
