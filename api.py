from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, constr
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

def count_occurrences(url, search_word):
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

class WordCountRequest(BaseModel):
    url: HttpUrl  # HttpUrl type enforces valid URL format
    search_word: constr(min_length=1)  # Ensure search_word is not empty

@app.post("/count_word_occurrences/")
async def count_word_occurrences(request_data: WordCountRequest):
    url = request_data.url
    search_word = request_data.search_word

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a')
        ls = []
        result = {}
        
        # Iterate through the links and count occurrences on linked pages
        for link in links:
            href = link.get('href')
            if href and href.startswith(url):
                if href not in ls:
                    ls.append(href)
                    count = count_occurrences(href, search_word)
                    if count > 0:
                        result[href] = count
        
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="No matching links found")
    else:
        raise HTTPException(status_code=400, detail="Invalid URL provided")
