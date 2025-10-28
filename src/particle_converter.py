import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

def extract_images(html_content):
    """Extract image URLs from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src.startswith('http'):
            images.append(src)
    return images


def html_to_paragraphs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    # Constellation browser's font does not display the non-breaking hyphen "‑" properly.
    # Once that's fixed remove the replace call.
    cleaned = [p.get_text(strip=True).replace('‑', '-') for p in paragraphs if p.get_text(strip=True)]
    return [p for p in cleaned if p]


def format_date(date_string):
    try:
        dt = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        return dt.strftime('%d %b %Y')
    except:
        return date_string


def save_particle_json(particle_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(particle_data, f, indent=2, ensure_ascii=False)
