# -*- coding: utf-8 -*-
from selenium import webdriver

# Download chromeDriver
# https://chromedriver.storage.googleapis.com/index.html?path=74.0.3729.6/
driver = webdriver.Chrome('C:/Users/staff/Desktop/chromedriver_win32/chromedriver.exe')
driver.get('http://jp.kabumap.com/servlets/kabumap/Action?SRC=basic/top/base&codetext=7203')
unit = driver.find_element_by_css_selector('#minUnit').text
print(unit)
driver.close()
