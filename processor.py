# processor.py

from bs4 import BeautifulSoup

def clean_html(html: str) -> str:
    """
    Cleans HTML content by removing scripts, styles, and unnecessary tags.
    Returns plain readable text.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Get clean text
    text = soup.get_text(separator=" ", strip=True)

    # Optional: further cleanup like collapsing whitespace
    cleaned_text = " ".join(text.split())
    return cleaned_text


def process_documents(data: list[dict]) -> list[dict]:
    """
    Applies clean_html to each document's content.
    """
    processed = []
    for item in data:
        cleaned = clean_html(item["content"])
        processed.append({
            "url": item["url"],
            "content": cleaned
        })
    return processed
