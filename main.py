import requests
from bs4 import BeautifulSoup
import re
# this is mohit Bhai
def count_word_occurrences(url, search_word):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract the text content of the webpage
        text_content = soup.get_text()

        # Use regular expressions to find occurrences of the search word
        occurrences = re.findall(r'\b{}\b'.format(re.escape(search_word)), text_content, flags=re.IGNORECASE)

        # Count the occurrences
        count = len(occurrences)

        return count
    else:
        return 0

# URL of the initial webpage
initial_url = 'https://www.itpathsolutions.com/'

# Word to search for
search_word = "AI & ML Development"

# Send an HTTP GET request to the initial URL
response = requests.get(initial_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the initial page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all the links on the initial webpage
    links = soup.find_all('a')
    ls = []
    # Iterate through the links and count occurrences on linked pages
    for link in links:
        href = link.get('href')
        if href and href.startswith('https://www.itpathsolutions.com/'):
            if href not in ls:
                ls.append(href)
                count = count_word_occurrences(href, search_word)
                if count > 0:
                    print(f"Link: {href}")
                    print(f"Number of occurrences of '{search_word}' on the webpage: {count}")

else:
    print(f"Failed to retrieve the initial webpage. Status code: {response.status_code}")
