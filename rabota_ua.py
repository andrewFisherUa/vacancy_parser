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
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find('dl', attrs={'id': 'ctl00_content_vacancyList_gridList_ctl23_pagerInnerTable'}).text
            pagination_id = list(pagination)
            count = int(pagination_id[-10])
            for i in range(count):
                url = f'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/pg{i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('article', attrs={'class' : 'f-vacancylist-vacancyblock'})
        for div in divs:
            title = div.find('a')['title']
            company = div.find('a', attrs={'class' : 'f-text-dark-bluegray f-visited-enable'}).text
            info = div.find('p', attrs={'class' : 'f-vacancylist-shortdescr f-text-gray fd-craftsmen'}).text
            jobs.append({
                'title' : title,
                'company' : company,
                'info' : info,
            })
        print(len(jobs))
    else:
        print('Error or done', str(request.status_code))
    return jobs

def files_writer(jobs):
    with open('rabota_ua_parsed.csv', 'a') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Title', 'Company', 'Info'))
        try:
            for job in jobs:
                a_pen.writerow((job['title'], job['company'], job['info']))
        except:
            pass
jobs = parser(headers, base_url)
files_writer(jobs)