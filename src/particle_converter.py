import json
import re
from bs4 import BeautifulSoup
from datetime import datetime


def strip_source_tags(text):
    return re.sub(r'\s*(?:\[[^\]]+\])+', '', text)


def html_to_paragraphs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    cleaned = [strip_source_tags(p.get_text(strip=True)) for p in paragraphs if p.get_text(strip=True)]
    return [p for p in cleaned if p]


def format_date(date_string):
    try:
        dt = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        return dt.strftime('%d %b %Y')
    except:
        return date_string


def convert_to_particle(article):
    title = article.get('title', 'Untitled')

    if len(title) > 40:
        title = title[:37] + "..."
    title = title.encode('ascii', 'ignore').decode('ascii')

    particle = {
        "format": "particle",
        "title": title,
        "content": []
    }

    particle['content'].append({
        "type": "paragraph",
        "text": f"*{article['title']}*"
    })

    if article.get('published'):
        particle['content'].append({
            "type": "paragraph",
            "text": format_date(article['published'])
        })

    content = article.get('content', '')
    if content:
        paragraphs = html_to_paragraphs(content)
        for para in paragraphs:
            particle['content'].append({
                "type": "paragraph",
                "text": para
            })

    return particle


def save_particle_json(particle_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(particle_data, f, indent=2, ensure_ascii=False)
