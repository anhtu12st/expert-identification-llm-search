import json

with open("request-crawled-data.json", "r") as f:
    papers = json.load(f)

new_data = []

for paper in papers:
    title = paper.get('title')
    authors = ", ".join(paper.get('authors'))
    categories = ", ".join(paper.get('categories'))
    new_data.append(
        f"The paper \"{title}\" with technology {categories} is created by {authors}")

with open("dataset.json", "w") as file:
    json.dump({"text": new_data}, file)
