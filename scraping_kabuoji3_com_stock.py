import urllib3
from bs4 import BeautifulSoup
import certifi
import csv
import re
import time

# ①最初に取得できる証券コードを取得する（ページ数の取得）
# アクセスするURL(初期URL)
from get_csv_file import get_stock_price

url = "https://kabuoji3.com/stock/"

# httpsの証明書検証を実行している
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

# URLにアクセスする htmlが返ってくる
r = http.request('GET', url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(r.data, "html.parser")

# タイトル要素を取得する
title_tag = soup.title

print(title_tag)

table = soup.findAll("table", {"class":"stock_table"})[0]
rows = table.findAll("tr")

with open("test.csv", "w", encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        if (len(csvRow) > 0):
            writer.writerow(csvRow)
            # print(cell.get_text())

# page記述のあるa タグを抽出
ul = soup.find_all("a", href=re.compile("\?page="))
print(ul)
page_list = []
for a in ul:
    page_list.append(a.string)
    # print(a.string)

params =[]

# ②取得データページ数で、各ページで証券コードを取得する
for page in page_list:
    url = "https://kabuoji3.com/stock/?page=" + page
    
    # httpsの証明書検証を実行している
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    
    # URLにアクセスする htmlが返ってくる
    r = http.request('GET', url)
    
    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(r.data, "html.parser")
    time.sleep(10)
    
    # タイトル要素を取得する
    title_tag = soup.title
    
    # print(title_tag)
    
    table = soup.findAll("table", {"class":"stock_table"})[0]
    rows = table.findAll("tr")

    # if page == '2':
    #     break
    
    with open("stock_page_" + page + ".csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            csvRow = []
            col = 0
            market = ""
            code = ""
            name = ""
            for cell in row.findAll(['td', 'th']):
                if col == 0:
                    code = cell.get_text()[:4]
                    name = cell.get_text()[5:]
                elif col == 1:
                    market = cell.get_text()
                else:
                    print('code: ' + code + ';' + 'name: ' + name + '; market: ' + market)
                    params.append([code, name, market])
                    # csvRow.append([code, name, market])
                    writer.writerow([code, name, market])
                    # csvRow.append(cell.get_text())
                    # if len(csvRow) > 0:
                    #     # writer.writerow(csvRow)
                    #
                    break
                col = col + 1

# 各取得できた内容から、各個別の証券コードのデータを取得する
# https://kabuoji3.com/stock/1543/

for param in params:
    print(param)
    if param[0].isnumeric() and len(param[0]) == 4:
        if int(param[0]) > 4044:
            print(param[0])  # 証券コード
            print(param[1])  # 名称
            print(param[2])  # 市場
            # if param[2] == '東証1部':
            url = 'https://kabuoji3.com/stock/' + param[0] + '/'
    
            # httpsの証明書検証を実行している
            http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where())
            time.sleep(10)
    
            # URLにアクセスする htmlが返ってくる
            r = http.request('GET', url)
            
            # htmlをBeautifulSoupで扱う
            soup = BeautifulSoup(r.data, "html.parser")
            
            year_list = []
            ul = soup.find_all("a", href=re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+/stock/[0-9]{4}/[0-9]{4}/"))
            print(ul)
            for year in ul:
                year_list.append(year.string)
                get_stock_price(param[0], year)
            print(year_list)
            time.sleep(10)
            
            