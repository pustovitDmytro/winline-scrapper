# -*- encoding: utf-8 -*-
from selenium import webdriver
import winline
import screenshot
import database as DB
import time
import os

MONTH="Aug"
BASE_URL="http://www.winlinebet.ru/"
HISTORY_URL=BASE_URL+"auth/istoria/"
BASE_SCREENS_DIR = "screens/"

def prepare_folder(path):
        if not os.path.isdir(path):
                os.makedirs(path)

#if __name__ == "__main__":
prepare_folder(MONTH);
prepare_folder(BASE_SCREENS_DIR+'/'+MONTH)
driver = webdriver.Chrome("/home/dmytro/Documents/python/seleniumDrivers/chromedriver")
driver.get(HISTORY_URL)
winline.autorization(driver)
time.sleep(3)
driver.save_screenshot(BASE_SCREENS_DIR+'Last_autorization.png')
calendar = winline.get_calendar(driver,MONTH)
driver.save_screenshot(BASE_SCREENS_DIR+'/'+MONTH+'/'+'available.png')
screenshot.get_element(calendar,BASE_SCREENS_DIR+'/'+MONTH+'/'+'available.png')
k=0;
while 1:
        arr=calendar.find_elements_by_xpath("//td[contains(@class,'available')]")[:-1]
        if k>=len(arr):
                break
        a=arr[k]
        current = DB.get_current_stat(MONTH)
        txt=a.text.strip()
        if txt in current:
                pass
        else:
                a.click();
                time.sleep(1)
                mybets=driver.find_element_by_css_selector(".my-bet")#exception msg: По данному запросу ставок не найдено. Попробуйте изменить критерии поиска.
                if mybets.text.find("не найдено")<0:
                        driver.save_screenshot(BASE_SCREENS_DIR+'/'+MONTH+'/'+txt+'_bets.png')
                        DB.save_bets(driver.page_source,MONTH,txt)
                calendar = winline.get_calendar(driver,MONTH)
                k+=1                        
driver.save_screenshot(BASE_SCREENS_DIR+'Last_final_screen.png')
driver.close()
