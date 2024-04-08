import requests
from bs4 import BeautifulSoup

def scrape_schemes():
    url = "https://pib.gov.in/PressReleaseIframePage.aspx?PRID=2002012"
    r = requests.get(url, verify=False)
    c = r.content

    soup = BeautifulSoup(c, 'html.parser')  # Parse the HTML content

    schemes = []  # List to store the scraped schemes

    # Find all table elements
    tables = soup.find_all('table')

    for table in tables:
        # Find all table rows (tr) within the current table
        rows = table.find_all('tr')

        # Skip the first row as it likely contains header information
        for row in rows[1:]:
            # Find all table data (td) within the current row
            cols = row.find_all('td')

            # Ensure there are at least 3 columns in the row
            if len(cols) >= 3:  # Adjusted to check for at least 3 columns
                name = cols[1].text.strip()
                purpose = cols[2].text.strip()

                # Append the scheme details to the list of schemes
                schemes.append({"name": name, "purpose": purpose})

    return schemes
