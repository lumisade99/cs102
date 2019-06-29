import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    tbl_list = parser.table.findAll('table')
    inner_table = tbl_list[1]
    rows = inner_table.findAll('tr')
    L = [rows[3 * i:3 + 3 * i] for i in range(30)]
    for i in range(len(L)): 
        a = L[i][1].findAll('a')[0].text
        b = L[i][1].findAll('a')[5].text
        c = L[i][1].findAll('span')[0].text
        d = L[i][0].findAll('a')[1].text
        if len(L[i][0].findAll('a')) == 3:
            e = L[i][0].findAll('a')[2].text
            di = {'author': a, 'comments': b, 'points': c, 'title': d, 'url':e}
            news_list.append(di)
        else:
            di = {'author': a, 'comments': b, 'points': c, 'title': d, 'url':'Ссылки нет'}
            news_list.append(di)
        time.sleep(0.333333334)
    return news_list



def extract_next_page(parser):
    """ Extract next page URL """
    tbl_list = parser.table.findAll('table')
    inner_table = tbl_list[1]
    rows = inner_table.findAll('tr')
    k = rows[-1].a['href']
    return k

   

def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news