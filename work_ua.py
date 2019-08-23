import requests
from bs4 import BeautifulSoup as bs
import csv
import time

headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url = 'https://www.work.ua/jobs-kyiv-python/?page=1'
def parser(headers, base_url):
    parse_time_start = time.time()
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find('span', attrs={'class' : 'text-default'}).text
            pagination_id = list(pagination)
            count = int(pagination_id[-1]) + 1
            for i in range(1, count):
                url = f'https://www.work.ua/jobs-kyiv-python/?page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class' : 'card card-hover card-visited wordwrap job-link'})
        for div in divs:
            title = div.find('a').text
            href = 'http://work.ua' + div.find('a')['href']
            info = div.find('p', attrs={'class' : 'overflow'}).text
            jobs.append({
                'title' : title,
                'href' : href,
                'info' : info,
            })
        print(len(jobs))
    else:
        print('Error or done ' + str(request.status_code))
        parse_time_finish = time.time()
        parse_time_result = parse_time_finish - parse_time_start
        print('Parsed in ', str(parse_time_result), 'seconds')
    return jobs

def files_writer(jobs):
    with open('parsed_csv/work_ua_parsed.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Title', 'URL', 'Info'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['info']))



jobs = parser(headers, base_url)
files_writer(jobs)
