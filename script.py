import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url = 'https://kiev.hh.ua/search/vacancy?L_is_autosearch=false&area=115&clusters=true&currency_code=UAH&enable_snippets=true&text=python&page=0'

def parser(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa' : 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://kiev.hh.ua/search/vacancy?L_is_autosearch=false&area=115&clusters=true&currency_code=UAH&enable_snippets=true&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class' : 'vacancy-serp-item'})
        divs = soup.find_all('div', attrs={'data-qa' : 'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-employer'}).text
            text1 = div.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = text1 + ' ' + text2
            jobs.append({
                'title' : title,
                'href' : href,
                'company' : company,
                'content' : content,
            })
        print(len(jobs))
    else:
        print('ERROR or Done', request.status_code)
    return jobs


def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow((('Vacancy', 'URL', 'Company', 'Info')))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))


jobs = parser(base_url, headers)
files_writer(jobs)