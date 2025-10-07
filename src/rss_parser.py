import feedparser


KAGI_BASE_URL = 'https://kite.kagi.com'
KAGI_SECTIONS = ['world', 'usa', 'business', 'technology', 'science', 'sports', 'entertainment']


def fetch_all_sections():
    all_articles = {}

    for section_name in KAGI_SECTIONS:
        print(f"Fetching {section_name} section...")
        feed = feedparser.parse(f'{KAGI_BASE_URL}/{section_name}.xml')

        articles = []
        for entry in feed.entries:
            content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else entry.get('summary', '')

            articles.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'content': content
            })

        all_articles[section_name] = articles
        print(f"  Found {len(articles)} articles")

    return all_articles
