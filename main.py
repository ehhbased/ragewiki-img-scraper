""" downloaded images belong to https://wiki.rage.mp/ under the  'Creative Commons Attribution Non-Commercial Share Alike' license"""

from pck_chkr import install_packages
install_packages()

import shutil
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

WIKI_XPATH = '//*[@id="mw-content-text"]/div/ul/li/div/div[1]/div/a/img'

import requests

paths = [
    'Masks',
    'Hair_Styles',
    'Torsos',
    'Legs',
    'Shoes',
    'Accessories',
    'Undershirts',
    'Tops',

    #props
    'Hats',
    'Glasses',
    'Ears',
    'Watches',
    'Bracelets',
]

gens = [
    'Female_',
    'Male_'
]

def italic(txt):
    return f"\033[3m{txt}\033[0m"

def doTheThang(driver: webdriver, path: str):
    results = driver.find_elements(By.XPATH, WIKI_XPATH)

    for f in results:
        link = f.get_attribute('src')

        #get the image content
        pos = link.find('px-')
        imageName = link[pos+3:]
        imgPath = path +'/'+imageName

        if(os.path.isfile(imgPath) is False):
            f = open(imgPath, 'wb')
            res = requests.get(link, stream = True)
            shutil.copyfileobj(res.raw, f)
            f.close()
    


def imgDownloader(driver: webdriver):
    for x in paths:
        if(x == 'Masks'):
            driver.get(f"https://wiki.rage.mp/index.php?title={x}")
            path = os.path.join(os.getcwd(), f"imgs/{x}")
            if(os.path.exists(path) is False):
                os.mkdir(path)

            doTheThang(driver, path)
        else:
            for gen in gens:
                driver.get(f"https://wiki.rage.mp/index.php?title={gen}{x}")
                path = os.path.join(os.getcwd(), f"imgs/{gen}{x}")

                if(os.path.exists(path) is False):
                    os.mkdir(path)

                print(f' * parsing {gen[:-1]} : {x}')
                doTheThang(driver, path)


def main() -> None:
    timerStart = time.perf_counter()
    driver: webdriver
    
    try:
        driver = webdriver.Chrome()
        imgDownloader(driver)
        timerEnd = time.perf_counter()
        
        print('[~] SUCCESS!', italic(f"time taken : {timerEnd - timerStart:0.4f}"), end='\n\n')

    except:
        exit(' * error starting web driver')
    


if __name__ == '__main__':
    main()