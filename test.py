import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/pg1'

def parser(headers, base_url):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('article', attrs={'class' : 'f-vacancylist-vacancyblock'})
        for div in divs:
            href = 'https://rabota.ua' + div.find('a')['href']
            print(href)

    else:
        print('Error')

parser(headers, base_url)