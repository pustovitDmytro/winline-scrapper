# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
import credentials


def check_month(calendar,s):
    selected=calendar.find_element_by_xpath("//select[@class='monthselect']/option[@selected='selected']")
    #як варіант просто відправляти send_keys назву місяця на monthselect
    if selected.text!=s:
        select = calendar.find_element_by_class_name("monthselect")
        select.send_keys(s)
        select.send_keys(Keys.ENTER)   

def get_calendar(driver, month):
    driver.find_element_by_id("daterangepicker").click()
    time.sleep(1)
    calendar = driver.find_element_by_class_name("calendar-table")
    check_month(calendar,month)
    return calendar


def get_records(page):
    bs = BeautifulSoup(page,"html.parser")
    table = bs.find("table", { "class" : "bet-table"})
    records=[]
    for row in table.findAll('tbody'):
        columns=row.findAll('td')
        rec={}
        rec['event_id'] = re.findall(r'\d{8}',columns[0].text)[0]
        divs = columns[1].div.findAll('div')
        rec['team_host'] = re.findall(r'(.*) -',divs[0].text)[0]
        rec['team_away'] = re.findall(r'- (.*)',divs[0].text)[0]
        rec['league'] = 0
        rec['bet_type'] = divs[1].text
        rec['expected_result'] = divs[2].text
        rec['coefficient'] = columns[2].text.strip()
        rec['actual_result'] = columns[3].text.strip()
        if columns[5].text.find('-')>0:
            rec['win_status'] = 0 
        else:
            if columns[5].text.find('+')>0:
                rec['win_status'] = 1
            else:
                rec['win_status'] ='undefined'
        records.append(rec)
    return records

def autorization(driver):
   form = driver.find_element_by_css_selector(".user__enter")
   elements = form.find_elements_by_tag_name("input")
   for e in elements:
       if e.get_attribute("placeholder"):
           if e.get_attribute("type") == "password":
               e.send_keys(MY_PSW)
               e.send_keys(Keys.ENTER)
           else:
               e.send_keys(MY_LOGIN)
