import requests
from bs4 import BeautifulSoup
import os
import sys
import msvcrt

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def download_file(url):
    local_filename = url.split('/')[-1]
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def display_content(soup):
    # Render all text content from the webpage
    for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
        print(element.get_text(separator='\n', strip=True))

def display_links(soup):
    links = soup.find_all('a')
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    for i, link in enumerate(links):
        href = link.get('href')
        text = link.get_text()
        print(f"{i + 1}: {text} ({href})")
    return links

def get_key():
    return msvcrt.getch()

def main():
    print("Welcome to the Console Web Browser!")
    history = []
    current_url = None
    home_url = "http://example.com"  # Set a default home page

    while True:
        if current_url:
            print(f"Current URL: {current_url}")
        url = input("Enter a URL (or 'back' to go back, 'home' for homepage, 'history' to view history, 'download' to download a file, 'exit' to quit): ")
        
        if url.lower() == 'exit':
            break
        elif url.lower() == 'back':
            if history:
                current_url = history.pop()
                print(f"Going back to: {current_url}")
            else:
                print("No history to go back to.")
            continue
        elif url.lower() == 'home':
            current_url = home_url
            print(f"Going to homepage: {current_url}")
        elif url.lower() == 'history':
            print("Browsing History:")
            for i, h in enumerate(history):
                print(f"{i + 1}: {h}")
            continue
        elif url.lower() == 'download':
            file_url = input("Enter the file URL to download: ")
            download_file(file_url)
            continue
        
        html = fetch_page(url)
        if html:
            soup = parse_html(html)
            history.append(url)  # Ensure the URL is added to history
            current_url = url
            
            # Display the full content of the webpage
            display_content(soup)

            links = display_links(soup)

            while True:
                key = get_key()
                if key == b'\r':  # Enter key
                    link_index = int(input("Enter the link number to navigate: ")) - 1
                    if 0 <= link_index < len(links):
                        current_url = links[link_index].get('href')
                        print(f"Navigating to: {current_url}")
                        break
                elif key.lower() == b'back':
                    break

if __name__ == "__main__":
    main()
