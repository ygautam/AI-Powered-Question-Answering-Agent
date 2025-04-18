import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_links = set()

def is_valid_url(url, base_netloc):
    parsed = urlparse(url)
    return parsed.netloc == base_netloc and url not in visited_links

def extract_main_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted sections (common in help docs)
    for tag in soup(['nav', 'header', 'footer', 'aside', 'script', 'style']):
        tag.decompose()

    # Get visible text
    text = soup.get_text(separator=' ', strip=True)
    return text

def crawl_website(base_url, max_links=50):
    parsed_base = urlparse(base_url)
    base_netloc = parsed_base.netloc

    to_visit = [base_url]
    crawled_data = []

    while to_visit and len(visited_links) < max_links:
        url = to_visit.pop(0)

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                continue

            visited_links.add(url)
            html = response.text
            main_text = extract_main_text(html)

            crawled_data.append({'url': url, 'content': main_text})
            print(f"[✓] Crawled: {url} ({len(visited_links)}/{max_links})")

            # Find more links to crawl
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if is_valid_url(next_url, base_netloc):
                    to_visit.append(next_url)

        except Exception as e:
            print(f"[!] Failed to crawl {url}: {e}")

    return crawled_data
