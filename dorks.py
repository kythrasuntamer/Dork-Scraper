import requests
from bs4 import BeautifulSoup
import urllib.parse

# Set the base URL for the Google search
base_url = "https://www.google.com/search?q="

# Define a list of dorks you want to search for
dorks = [
    "Index of /password",
    "Index of /admin",
    "Index of /backup",
    # Add more dorks here as needed
]

# Set the number of pages of results that you want to scrape
num_pages = 20

# Initialize a list to store the results
results = []

# Iterate over each dork
for dork in dorks:
    # Iterate over the pages of results
    for page in range(num_pages):
        # Calculate the start parameter for the Google search URL
        start = page * 10
        # Encode the query string
        encoded_query = urllib.parse.quote(dork)
        # Construct the full URL for the search
        search_url = f"{base_url}{encoded_query}&start={start}"
        # Send an HTTP request to the Google search URL
        response = requests.get(search_url)
        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all of the search result links on the page
        links = soup.find_all("a")
        # Iterate over the links and store the result URLs
        for link in links:
            href = link.get("href")
            if href and href.startswith("/url?q="):
                # Extract and clean the URL
                url = urllib.parse.urlparse(href[7:]).query.split('&')[0]
                results.append(url)

# Write the results to a file
with open("results.txt", "w") as f:
    for result in results:
        f.write(result + "\n")
