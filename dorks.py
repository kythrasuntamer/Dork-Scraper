import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def search_google(query, num_pages):
    base_url = "https://www.google.com/search?q="
    results = []

    for page in range(num_pages):
        start = page * 10
        encoded_query = urllib.parse.quote(query)
        search_url = f"{base_url}{encoded_query}&start={start}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            links = soup.find_all("a")
            for link in links:
                href = link.get("href")
                if href and href.startswith("/url?q="):
                    url = urllib.parse.urlparse(href[7:]).query.split('&')[0]
                    results.append(url)
        except requests.exceptions.RequestException as e:
            print("Error:", e)
        
        time.sleep(15)  # Add a 15-second delay between requests

    return results

def save_results(results, filename):
    with open(filename, "w") as f:
        for result in results:
            f.write(result + "\n")

if __name__ == "__main__":
    dorks = [
        "Index of /password",
        "Index of /admin",
        "Index of /backup",
        # Add more dorks here as needed
    ]
    num_pages = 20

    all_results = []
    for dork in dorks:
        dork_results = search_google(dork, num_pages)
        all_results.extend(dork_results)

    save_results(all_results, "results.txt")
