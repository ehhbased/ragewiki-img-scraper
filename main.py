""" downloaded images belong to https://wiki.rage.mp/ under the  'Creative Commons Attribution Non-Commercial Share Alike' license"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import os
import shutil

from pck_chkr import install_packages
install_packages()


WIKI_XPATH = '//*[@id="mw-content-text"]/div/ul/li/div/div[1]/div/a/img'


paths = [
    'Masks',
    'Hair_Styles',
    'Torsos',
    'Legs',
    'Shoes',
    'Accessories',
    'Undershirts',
    'Tops',

    # props
    'Props_Hats',
    'Props_Glasses',
    'Props_Ears',
    'Props_Watches',
    'Props_Bracelets',
]

gens = [
    'Female',
    'Male'
]


def italic(txt):
    return f"\033[3m{txt}\033[0m"


def doTheThang(driver: webdriver, path: str):
    results = driver.find_elements(By.XPATH, WIKI_XPATH)

    for f in results:
        link = f.get_attribute('src')

        # get the image content
        pos = link.find('px-')
        imageName = link[pos+3:]
        imgPath = path + '/'+imageName

        if (os.path.isfile(imgPath) is False):
            f = open(imgPath, 'wb')
            res = requests.get(link, stream=True)
            shutil.copyfileobj(res.raw, f)
            f.close()


def imgDownloader(driver: webdriver):
    for x in paths:
        if (x == 'Masks'):
            driver.get(f"https://wiki.rage.mp/index.php?title={x}")
            path = os.path.join(os.getcwd(), f"imgs/{x.lower()}")
            if (os.path.exists(path) is False):
                os.mkdir(path)

            doTheThang(driver, path)
        else:
            for gen in gens:
                urlpath = x[6:] if "Props_" in x else x

                driver.get(
                    f"https://wiki.rage.mp/index.php?title={gen}_{urlpath}")

                folderName = f"props_{gen}_{urlpath}" if "Props_" in x else f"{gen}_{x}"

                path = os.path.join(os.getcwd(), f"imgs/{folderName.lower()}")

                if (os.path.exists(path) is False):
                    os.mkdir(path)

                print(f' * parsing {gen} : {x}')
                doTheThang(driver, path)


def main() -> None:
    timerStart = time.perf_counter()
    driver: webdriver

    try:
        driver = webdriver.Chrome()
    except:
        exit(' * error starting web driver')

    try:
        imgDownloader(driver)
        timerEnd = time.perf_counter()

        print('[~] SUCCESS!', italic(
            f"time taken : {timerEnd - timerStart:0.4f}s"), end='\n\n')
    except:
        exit(' * error while downloading images!')


if __name__ == '__main__':
    main()
