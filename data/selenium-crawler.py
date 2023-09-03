import time
from selenium import webdriver
from bs4 import BeautifulSoup
import json

from utils import get_paper_date_and_authors, get_paper_tasks

HOME_DOMAIN = "https://paperswithcode.com"
NUM_SCROLL = 10

# Create a WebDriver instance (make sure you have the appropriate webdriver installed)
# For example, if using Chrome, you need ChromeDriver: https://chromedriver.chromium.org/
# Specify the path to your webdriver executable here
driver = webdriver.Chrome()

# Navigate to the Papers with Code website
driver.get(HOME_DOMAIN)

global prev_scroll_height
prev_scroll_height = 0


def can_scroll(driver):
    # Function to check if the page can still be scrolled
    global prev_scroll_height
    current_scroll_height = int(driver.execute_script(
        "return document.body.scrollHeight"))
    if current_scroll_height == prev_scroll_height:
        return False
    prev_scroll_height = current_scroll_height
    return True


def scroll_to_bottom(driver):
    # Function to scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)  # You may need to adjust the sleep duration


# Scroll down to load more data (repeat as needed)
# for _ in range(NUM_SCROLL):  # You can adjust the number of times you want to scroll
#     scroll_to_bottom(driver)
# Scroll to the bottom of the page until it cannot be scrolled anymore
while can_scroll(driver):
    scroll_to_bottom(driver)
    NUM_SCROLL -= 1
    if NUM_SCROLL == 0:
        break

# Extract the page source after scrolling
page_source = driver.page_source

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, "html.parser")

# Extract paper information
papers = []
paper_elements = soup.find_all("div", class_="paper-card")

for paper_element in paper_elements:
    paper_id = paper_element.select_one('.item-content > h1 > a')["href"]
    print(paper_id)
    driver.execute_script(
        "window.open('" + HOME_DOMAIN + paper_id + "', '_blank')")
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    time.sleep(1)
    page_source = driver.page_source
    new_soup = BeautifulSoup(page_source, "html.parser")

    paper_title = new_soup.select_one(
        "body > div.container.content.content-buffer > main > div.paper-title > div > div > h1").text.strip().lower()
    paper_date, paper_authors = get_paper_date_and_authors(new_soup)
    paper_tasks = get_paper_tasks(new_soup)

    papers.append({
        "id": paper_id,
        "title": paper_title,
        "date": paper_date,
        "authors": paper_authors,
        "categories": paper_tasks,
    })

    driver.close()
    prev_window = driver.window_handles[0]
    driver.switch_to.window(prev_window)

print(f"Total papers crawled: {len(papers)}")
with open("crawled-data.json", "w") as file:
    json.dump(papers, file)

# Close the WebDriver
driver.quit()
