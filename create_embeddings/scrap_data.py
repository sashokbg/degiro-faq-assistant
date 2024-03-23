import requests
from bs4 import BeautifulSoup
import time
from promptflow import tool
import re
import os

base_url = 'https://www.degiro.com'

sections = [
    '/uk/helpdesk/about-degiro',
    '/uk/helpdesk/account-and-personal-details',
    '/uk/helpdesk/account-and-personal-details?page=1',
    '/uk/helpdesk/become-client',
    '/uk/helpdesk/fees',
    '/uk/helpdesk/money-transfers-and-handling',
    '/uk/helpdesk/money-transfers-and-handling?page=1',
    '/uk/helpdesk/orders',
    '/uk/helpdesk/orders?page=1',
    '/uk/helpdesk/trading-platform',
    '/uk/helpdesk/trading-platform?page=1',
    '/uk/helpdesk/trading-platform?page=2',
    '/uk/helpdesk/trading-possibilities',
    '/uk/helpdesk/trading-possibilities?page=1',
    '/uk/helpdesk/trading-possibilities?page=2',
    '/uk/helpdesk/tax',
    '/uk/helpdesk/tax?page=1',
    '/uk/helpdesk/tax?page=2'
]


def extract(section):
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    }
    response = requests.get(base_url + section, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select('.faq--row a')

    for row in rows:
        link = base_url + row['href']
        sub_response = requests.get(link, headers=headers)

        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')

        content = sub_soup.find('article').get_text().replace('Answer', '').strip().replace('Accordion', '').strip()
        content = re.sub(r'\s{2,}', ' ', content)

        result_string = f"# {row.get_text()}\n\n## {link}\n\n{content}\n\n"
        data.append(result_string)

    return data


all_data = []


@tool
def scrap_data(file_path: str):
    print("Starting scraping")

    if os.path.exists(file_path):
        print(f"Skipping data scraping due to file {file_path} already existing !")

        return file_path

    for section in sections:
        all_data.extend(extract(section))
        time.sleep(0.5)

    try:
        with open(file_path, 'w') as file:
            for d in all_data:
                file.write(d)
    except Exception as e:
        print(e)

    print("Done scraping")
    return file_path
