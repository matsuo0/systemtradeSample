# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def download_stock_csv(code_range, save_dir):

    # CSVファイルを自動で save_dir に保存するための設定
    # Chrome用に修正
    options = webdriver.ChromeOptions()
    prefs = {"browser.download.folderList": 2,
             "browser.download.manager.showWhenStarting": False,
             "browser.download.dir": save_dir,
             "browser.helperApps.neverAsk.saveToDisk": "text/csv"}
    options.add_experimental_option("prefs", prefs)
    chromedriver = 'C:/Users\staff/Desktop/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    driver.get('https://www.yahoo.co.jp/')

    # ここで手動でログインを行う。ログインしたら enter
    # VIP 倶楽部への登録が必要
    input('After login, press enter: ')

    for code in code_range:
        url = 'https://stocks.finance.yahoo.co.jp/stocks/history/?code={0}.T'.format(code)
        driver.get(url)

        try:
            driver.find_element_by_css_selector('a.stocksCsvBtn').click()
        except NoSuchElementException:
            pass

if __name__ == '__main__':
    import os
    download_stock_csv((7203, 9684), os.getcwd())