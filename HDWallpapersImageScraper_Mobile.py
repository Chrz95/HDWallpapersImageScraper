from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import time
import shutil
import sys

directory = "Images_Mobile"
wallpaper_dir = "D:\My Personal Files\Πολυμέσα\Εικόνες\Φόντα\Mobile"

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
                Wallpaper_webpage = "https://www.hdwallpapers.in/download" + ImageName[0:-4] + "-1440x2560" + ImageName[-4:]
                Wallpaper_webpage = Wallpaper_webpage.replace("-HD","")
                #print ("\t" + Wallpaper_webpage.strip())

                #### Download the image ####

                for word in Exclude_Words:
                    if (word.strip() in ImageName):
                        return

                ImageName = ImageName.replace("-HD","")
                NewImageName = ImageName[0:-4]

                ImageExists = False
                ImgLength = len(NewImageName)
                ImageNames = []

                #print(ImageNames)

                if (os.path.isfile(wallpaper_dir + ImageName)) or (os.path.isfile(directory + ImageName)):
                    ImageExists = True

                if (not ImageExists):
                    for img in ImageNames:
                        if (os.path.isfile(wallpaper_dir + img)) or (os.path.isfile(directory + img)):
                            ImageExists = True
                            break

                if (not ImageExists):
                    r = requests.get(Wallpaper_webpage,stream=True, headers={'User-agent': 'Mozilla/5.0'})
                    with open(directory + ImageName, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    print("Downloaded Image <<" + ImageName[1:-4] + ">> from url:",Wallpaper_webpage)
                    #time.sleep(1)
                
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
NumOfPages = int(sys.argv[1])
os.system("mkdir " + directory)
PageToPause = 50

start = 1
end = NumOfPages + 1
#start = 208

for num in range (start,end):
    print("====================== Page " + str(num) + " ======================")

    if (num % PageToPause == 0):
        time.sleep(10)

    r = requests.get ("https://www.hdwallpapers.in/1440x2560_android-mobiles-hd-wallpapers-r/page/"+ str(num))
    soup = BeautifulSoup(r.text,"html.parser")
    ListOfImages = soup.find("ul",{"class":"wallpapers"})
    links = ListOfImages.findAll("li",{"class":"wall"})
    ParseImageLinks(links)


