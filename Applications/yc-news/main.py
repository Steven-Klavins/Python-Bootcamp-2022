from bs4 import BeautifulSoup
import requests

URL = "https://news.ycombinator.com/"

try:
    response = requests.get(URL)
except requests.exceptions.RequestException as e:
    print(e)

if response:
    # Make response data into a soup object.
    yc_web_page = response.text
    soup = BeautifulSoup(yc_web_page, "html.parser")

    rows = soup.find_all(class_="titleline")
    sub_text = soup.find_all(class_="subtext")
    scores = []

    # Gather the scores from the sub text, if score is undefined set it to 0.
    for text in sub_text:
        if text.find(class_="score"):
            scores.append(int(text.find(class_="score").text.split()[0]))
        else:
            scores.append(0)

    # Find the highest scored article and print it out
    hs_index = scores.index(max(scores))
    selected_row = rows[hs_index].find(name="a")
    print(f"{max(scores)} points\n{selected_row.string}\n{selected_row.get('href')}")
