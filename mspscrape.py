from bs4 import BeautifulSoup
import requests

url = 'https://farmer.gov.in/mspstatements.aspx'
r = requests.get(url, verify=False)
c = r.content
soup = BeautifulSoup(c, 'html.parser')

def fetch_crop_row(crop_name):
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
            if cell.get_text().strip() == crop_name:
                return str(row)


