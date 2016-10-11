#!/usr/bin/env python
import sys 
from win10notification import WindowsBalloonTip
# Downloads the bing wallpaper of the day 
# Takes in string directory, int keep
# Saves image in input directory
# Keep is number of unique images to keep in storage -1 is infinite
def downloadWallpaper(directory, keep):
    from selenium import webdriver
    import urllib.request
    import time, os, datetime

    if not os.path.isdir(directory):
        os.makedirs(directory)

    url = "http://bing.com"
    browser = webdriver.PhantomJS(executable_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "phantomjs.exe"))
    browser.get(url)
    link = None
    while link == None:
        time.sleep(10)
        link = browser.find_element_by_id("bgDiv").value_of_css_property("background-image")
        
    browser.quit()
    link = link.split('(')[1][:-1]

    image = link.split('/')[-1]
    image = os.path.join(directory, image)

    count = 0

    while True:
        try:
            urllib.request.urlretrieve(link, image)

            images = []
            for item in os.listdir(directory):
                if os.path.splitext(item)[1] in [".jpg", ".jpeg", ".png"]:
                    images.append(os.path.join(directory, item))
            images = sorted(images, key=os.path.getmtime, reverse=True)

            diff = len(images) - keep
            if diff >= 0:   # delete extras
                for i in range(diff):
                    os.remove(images[-1])
                    images.pop(-1)

            icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            balloon = WindowsBalloonTip()
            balloon.balloon_tip("WotD",
                                "New wallpaper of the day downloaded!",
                                icon_path=icon,
                                duration=4)
        except Exception as e:
            count += 1
            print(e)
            if count >= 10:
                break
            time.sleep(10)
            continue
        break            


if __name__ == '__main__':
    directory = sys.argv[1]
    count = int(sys.argv[2])
    downloadWallpaper(directory, count)
