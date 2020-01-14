
import os
import time
import sys

video_index = 1

def sprint(string):
    for c in string + '\n' :
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(10 / 100)


def html_handle(file_name):
	print("\033[1;32;40m")
	global video_index
	with open(file_name, "r+") as file:
		i = 1
		for con in file:
			if i == 63:
				video_url = con
			i+=1
		new_video_url = video_url.split("url")[1].split(',')[0].split('"')[2]
		os.system("curl -O {}".format(new_video_url))
		video_name = video_url.split("url")[1].split(',')[0].split('"')[2].split("/")[4]
		video_name_and_index = "Video " + str(video_index) + ".mp4"
		video_index += 1
		os.rename(video_name, video_name_and_index)
		os.system("rm -rf {}".format(file_name))
	print("\033[0;37;40m")

def main():
	os.system("clear")
	username = os.path.expanduser("~").split('/')[2]
	os.system("mkdir /Volumes/Storage/goinfre/$(whoami)/wistia-downloader")
	os.system("cp video_ID.txt /Volumes/Storage/goinfre/{}/wistia-downloader/".format(username))
	os.chdir("/Volumes/Storage/goinfre/{}/wistia-downloader".format(username))
	url = "http://fast.wistia.net/embed/iframe/"
	i = 0
	sprint("\033[1;33;40mOpening the download folder...\033[0;37;40m")
	os.system("open /Volumes/Storage/goinfre/{}/wistia-downloader/".format(username))
	with open("video_ID.txt", "r+") as video_id:
		for id in video_id:
			os.system("curl -O {}".format(url + id))
			print("Video " + str(i + 1) + "--------------------------------------------------------------------------")
			html_handle(id[:-1])
			print("-----------------------------------------------------------------------------------")
			i+=1 

	

if __name__ == '__main__':
	main()