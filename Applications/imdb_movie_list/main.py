from selenium import webdriver

# Add the location of Chrome Driver here.
CHROMEDRIVER_PATH = r'C:\Users\your\ChromeDriver\path\chromedriver.exe'
# Add the URL of your chosen list here.
IMDB_LIST_URL = "https://www.imdb.com/list/your-chosen-list"


# Append the move to the file
def write_to_list(movie):
    with open("movie-list.txt", "a") as file:
        file.write(f"{movie}\n")


# Create the movie list text file.
with open("movie-list.txt", "w") as file:
    file.write("++++++++++++\nMovies List\n++++++++++++\n")

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
driver.get(IMDB_LIST_URL)
next_page = True

while next_page:
    # Check if the next link is not disabled.
    next_page = not "disabled" in driver.find_element_by_class_name("next-page").get_attribute('class')
    movies = driver.find_elements_by_class_name("lister-item-header")

    # Iterate over the movies and add them to the list
    [write_to_list(movie.text) for movie in movies]

    # If there is not a next page break the loop.
    if not next_page:
        break
    else:
        # Get the next page.
        driver.get(driver.find_element_by_class_name("next-page").get_attribute("href"))

driver.close()
driver.quit()
print("Process complete!")
