import urllib3
from bs4 import BeautifulSoup
import certifi
import csv
import re

# アクセスするURL(初期URL)
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
    print(a.string)


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
    
    # タイトル要素を取得する
    title_tag = soup.title
    
    print(title_tag)
    
    table = soup.findAll("table", {"class":"stock_table"})[0]
    rows = table.findAll("tr")
    
    with open("test" + page + ".csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            if (len(csvRow) > 0):
                writer.writerow(csvRow)

    
 



# class MyTestCase(unittest.TestCase):
#   def test_something(self):
#     self.assertEqual(True, False)

# if __name__ == '__main__':
  # unittest.main()
