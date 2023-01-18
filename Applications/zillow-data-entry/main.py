from bs4 import BeautifulSoup
from selenium import webdriver
import requests

# Add the location of Chrome Driver here.
CHROMEDRIVER_PATH = r'C:\Users\your\ChromeDriver\path\chromedriver.exe'
# Add the URL of your Google form here.
GOOGLE_FORM_URL = "https://docs.google.com/your-form"
# Add the URL of your Zillow search here
ZILLOW_PAGE = "https://www.zillow.com/your-search"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.131 Safari/537.36'
}

try:
    response = requests.get(ZILLOW_PAGE, headers=headers)
except requests.exceptions.RequestException as e:
    print(e)

all_properties = []

# If the response is successful format the data into a dictionary.
if response:
    soup = BeautifulSoup(response.text, "html.parser")
    list_items = soup.find(id="search-page-list-container").find(name="ul").find_all(name="li")

    for item in list_items:
        property_data = item.find(name="a")
        if property_data:
            all_properties.append({"address": property_data.text, "price": item.find(name="span").text,
                                   "link": f"https://www.zillow.com{property_data['href']}"})

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

    # For each property listing fill in the form with selenium.
    for property_listing in all_properties:
        driver.get(GOOGLE_FORM_URL)
        form = driver.find_elements_by_xpath('//input[@type="text"]')
        form[0].send_keys(property_listing["address"])
        form[1].send_keys(property_listing["price"])
        form[2].send_keys(property_listing["link"])
        driver.find_element_by_xpath('//span[text()="Submit"]').click()

    driver.close()
    driver.quit()
