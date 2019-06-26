import requests
import os

# https://qiita.com/5zm/items/366f10fcde5d3435b417

def get_stock_price(code, year):
    response = requests.post(
        'https://kabuoji3.com/stock/file.php',
        {'code': code, 'year': year})
    contentDisposition = response.headers['Content-Disposition']
    # print(contentDisposition)
    ATTRIBUTE = 'filename='
    filename = contentDisposition[contentDisposition.find(ATTRIBUTE) + len(ATTRIBUTE):]
    filename = filename.replace("\"", "")
    if not os.path.exists('.\\stock_data'):
        os.mkdir('.\\stock_data')
    filename = '.\\stock_data' + "\\" + filename
    f = open(filename, 'w')
    f.write(response.text)
    f.close()


if __name__ == "__main__":
    get_stock_price(1301, 2019)
