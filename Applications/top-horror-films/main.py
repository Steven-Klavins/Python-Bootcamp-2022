from bs4 import BeautifulSoup
import requests

URL = "https://www.imdb.com/list/ls062635494/"

# Format the data into a text file.

def format_and_add_to_txt(index, title_data):
    movie = title_data.find("a").string
    year = title_data.find(class_="lister-item-year").string

    with open("top-horror-films.txt", "a") as file:
        file.write(f"{index}) {movie} {year}\n")


try:
    response = requests.get(URL)
except requests.exceptions.RequestException as e:
    print(e)

if response:
    # Make response data into a soup object.
    imdb_web_page = response.text
    soup = BeautifulSoup(imdb_web_page, "html.parser")
    titles = soup.find_all(class_="lister-item-header")

    # Iterate over the data and add the movies to the text file.
    for i, title in enumerate(titles):
        format_and_add_to_txt(i + 1, title)
