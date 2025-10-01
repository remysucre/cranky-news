"""HTML parser for CSM text edition articles."""

import requests
from bs4 import BeautifulSoup


def fetch_article_content(url):
    """
    Fetch and parse a CSM text edition article.

    Args:
        url: Text edition URL

    Returns:
        Dictionary with article metadata and content
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    article = {
        'url': url,
        'title': '',
        'byline': '',
        'date': '',
        'paragraphs': []
    }

    # Extract title - typically in an h1 or article title element
    title_elem = soup.find('h1') or soup.find('title')
    if title_elem:
        article['title'] = title_elem.get_text(strip=True)

    # Extract byline
    byline_elem = soup.find(class_='byline') or soup.find('span', class_='author')
    if byline_elem:
        article['byline'] = byline_elem.get_text(strip=True)

    # Extract date
    date_elem = soup.find('time') or soup.find(class_='date')
    if date_elem:
        article['date'] = date_elem.get_text(strip=True)

    # Extract article body paragraphs
    # The text edition likely has a simple structure with paragraphs in article body
    article_body = soup.find('article') or soup.find('div', class_='story-body') or soup.find('div', class_='body')

    if article_body:
        paragraphs = article_body.find_all('p')
        article['paragraphs'] = [_convert_paragraph_with_formatting(p) for p in paragraphs if p.get_text(strip=True)]
    else:
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        article['paragraphs'] = [_convert_paragraph_with_formatting(p) for p in paragraphs if p.get_text(strip=True)]

    return article


def _convert_paragraph_with_formatting(paragraph):
    """
    Convert a paragraph element to text, preserving italic formatting.

    Args:
        paragraph: BeautifulSoup paragraph element

    Returns:
        String with _italic_ markup for <em> and <i> tags
    """
    result = []

    for element in paragraph.descendants:
        if element.name in ['em', 'i']:
            text = element.get_text()
            if text:
                result.append(f"_{text}_")
        elif isinstance(element, str):
            # Check if this text is not already inside an em/i tag
            if element.parent.name not in ['em', 'i']:
                result.append(element)

    return ''.join(result).strip()
