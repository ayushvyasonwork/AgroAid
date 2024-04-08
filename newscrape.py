import requests
from bs4 import BeautifulSoup

def scrape_news():
    news_list = []
    for i in range(0, 3):
        url = "https://www.icar.org.in/news-highlights?page=" + str(i)
        r = requests.get(url, verify=False)
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')
        table_rows = soup.select('tbody tr')
        for row in table_rows:
            news_title = row.select_one('.views-field-title a')
            news_list.append(news_title.text.strip())
    return news_list