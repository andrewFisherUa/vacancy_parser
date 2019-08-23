import requests
from bs4 import BeautifulSoup as bs

headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url = 'https://www.work.ua/jobs-kyiv-python/?page=1'
def parser(headers, base_url):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        pagination = soup.find('span', attrs={'class': 'text-default'}).text
        pagination_id = list(pagination)
        count = int(pagination_id[-1]) + 1
        for i in range(1, count):
            url = f'https://www.work.ua/jobs-kyiv-python/?page={i}'
            print(url)
    else:
        print('error')

parser(headers, base_url)