def get_paper_date_and_authors(html_soup):
    author_elements = html_soup.select(
        "body > div.container.content.content-buffer > main > div.paper-title > div > div > div > p > span.author-span")
    paper_authors = []
    paper_date = None
    for i in range(0, len(author_elements)):
        if i == 0:
            paper_date = author_elements[i].text.strip().lower()
        else:
            paper_authors.append(author_elements[i].text.strip().lower())
    return paper_date, paper_authors


def get_paper_tasks(html_soup):
    task_elements = html_soup.select(
        "#tasks > div > div.paper-tasks > div > div > a")
    paper_tasks = []
    for ele in task_elements:
        paper_tasks.append(ele.text.strip().lower())
    return paper_tasks
