from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import time
import shutil
import sys

directory = "Images"

Exclude = open("Exclude.txt",'r')
Exclude_Words = Exclude.readlines()
Exclude.close()

def DownloadPic(item):

        FoundError = 1
        FailCounter = 0

        while (FoundError == 1):
            try:
                FoundError = 0
                #ImageName = item.text.strip()
                #print(ImageName)

                ImageName = item.find("a").attrs["href"].replace("wallpapers.html","HD.jpg")
                Wallpaper_webpage = "https://www.hdwallpapers.in/download" + ImageName
                #print ("\t" + Wallpaper_webpage.strip())

                #### Download the image ####
                ImageName = ImageName.replace("-HD","")

                for word in Exclude_Words:
                    if (word.strip() in ImageName):
                        return

                NewImageName = ImageName[0:-4]

                ImageExists = False
                ImgLength = len(NewImageName)
                ImageNames = []
                
                if (os.path.isfile(directory + ImageName)):
                    ImageExists = True

                if (not ImageExists):
                    for img in ImageNames:
                        if (os.path.isfile(directory + img)):
                            ImageExists = True
                            break

                Resolutions = ["_5k-5120x2880","-5120x2880","-2560x1440","_4k-3840x2160","-3840x2160","-1920x1080","_2k-1920x1080","_8k-7680x4320","-7680x4320","_4k_8k-7680x4320","_4k","_5k","_2k","_8k","_4k_8k","_4k_5k","_3k","_2k","_4k_8k_2-7680x4320","_4k_8k_3-7680x4320","_4k_2","_4k_3","_4k_4"]
                for i in range((ImgLength//3),ImgLength + 1):
                    ImageNames.append(NewImageName[0:i] + ".jpg")
                    for res in Resolutions:
                        ImageNames.append(NewImageName[0:i] + res + ".jpg")

                if (not ImageExists):
                    r = requests.get(Wallpaper_webpage,stream=True, headers={'User-agent': 'Mozilla/5.0'})
                    with open(directory + ImageName, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    print("Downloaded Image <<" + ImageName[1:-4] + ">>")
                
            except Exception as e: # If it finds an error, try again
                print(e)
                FailCounter = FailCounter + 1
                if (FailCounter < 10):
                    FoundError = 1
                else:
                    FoundError = 0
                    FailCounter = 0
                print("Failed to download image << " + ImageName + " >>")


def ParseImageLinks(links) :

    for item in links:
        DownloadPic(item)
        #time.sleep(1)

################# MAIN ######################

#NumOfPages = int(input("Enter the number of pages : "))
NumOfPages = 5
os.system("mkdir " + directory)
PageToPause = 50

start = 1
end = NumOfPages + 1
#start = 208

for num in range (start,end):
    print("====================== Page " + str(num) + " ======================")

    if (num % PageToPause == 0):
        time.sleep(10)

    r = requests.get ("https://www.hdwallpapers.in/latest_wallpapers/page/"+ str(num))
    soup = BeautifulSoup(r.text,"html.parser")
    ListOfImages = soup.find("ul",{"class":"wallpapers"})
    links = ListOfImages.findAll("li",{"class":"wall"})
    ParseImageLinks(links)


