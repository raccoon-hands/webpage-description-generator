import requests
from bs4 import BeautifulSoup
import random

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

#The following are various web scraping functions:


#Given a URL, returns the links on the web page at that URL
def scrape_website_for_links(url):
    try:
        response = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links_list = []
        for link in soup.find_all('a', href=True):
            link_text = link.text.strip()
            link_url = link['href']
            links_list.append((link_text, link_url))
        return links_list
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the website: {e}")



#Filters a list of link to try and find one that links to an "about" page.
def filter_links_with_about(links_list):
    filtered_links = [(text, url) for text, url in links_list if 'about' in text.lower()]
    return filtered_links

#Attempts to extract the text content on a web page, excluding links or navigation
def extract_website_info(url):
    try:
        response = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch website: {url}")
        print(f"Error: {str(e)}")
        raise ConnectionError("Failed to fetch the website.")
        return ""
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('body')

        # Remove CSS styles and scripts from the body
        for style in body.find_all('style'):
            style.decompose()
        for script in body.find_all('script'):
            script.decompose()

        # Remove URLs from the body
        for link in body.find_all('a'):
            link.decompose()

        # Remove Any Navigation Bar Information
        for link in body.find_all('nav'):
            link.decompose()

        # Extract the text content from the body
        text = body.get_text(separator='\n')

        # Remove leading/trailing whitespaces and empty lines
        lines = (line.strip() for line in text.splitlines())
        content = ''.join(line for line in lines if line)
        return content
    except:
        print("Something went wrong when extracting web page text. The web page may be a pdf or other file.")
        raise TypeError("URL links to file other than web page.")
        return ""
        
    
    


#Examines a web page's links, attempts to locate the "about" page, and then
#extract the "about" page's text.
def scrape_aboutpage(website_url):
    links_list = scrape_website_for_links(website_url)
    filtered_links_list = filter_links_with_about(links_list)

    # Remove duplicate URLs while preserving the order of appearance.
    seen_urls = set()
    unique_filtered_links_list = []
    for link_text, link_url in filtered_links_list:
        if link_url not in seen_urls:
            seen_urls.add(link_url)
            unique_filtered_links_list.append((link_text, link_url))

    for idx, (link_text, link_url) in enumerate(unique_filtered_links_list, start=1):
        print(f"{idx}. Text: {link_text}, URL: {link_url}")
        # Access the page and scrape text from the body
        page_text = extract_website_info(link_url)
        if not page_text:
            print("Unable to scrape page text.")
        return page_text
        
            
            
            
        
