import time
import requests
from bs4 import BeautifulSoup
import json

from utils import get_paper_date_and_authors, get_paper_tasks

def get_url(index):
    return f"https://paperswithcode.com/?page={index}"

def get_paper_url(paper_id):
    return f"https://paperswithcode.com{paper_id}"

papers = []
paper_ids = []
should_break = False

for i in range(1, 2001):
    print(f"======== Index: {i} ========")
    response = requests.get(get_url(i))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paper_elements = soup.find_all("div", class_="paper-card")
        for paper_element in paper_elements:
            paper_id = paper_element.select_one('.item-content > h1 > a')["href"]
            if paper_id in paper_ids:
                should_break = True
            if should_break: break
            paper_ids.append(paper_id)
            time.sleep(1)
            print(get_paper_url(paper_id))
            response = requests.get(get_paper_url(paper_id))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                paper_title = soup.select_one("body > div.container.content.content-buffer > main > div.paper-title > div > div > h1").text.strip().lower()
                paper_date, paper_authors = get_paper_date_and_authors(soup)
                paper_tasks = get_paper_tasks(soup)
                papers.append({
                    "id": paper_id,
                    "title": paper_title,
                    "date": paper_date,
                    "authors": paper_authors,
                    "categories": paper_tasks,
                })
            else:
                print(response.text)
                print(f"Failed on paper: {paper_id}")
    else:
        print(f"Failed on index: {i}")
        break
    time.sleep(1)
    if should_break: break

print(f"Total papers crawled: {len(papers)}")
with open("request-crawled-data.json", "w") as file:
    json.dump(papers, file)