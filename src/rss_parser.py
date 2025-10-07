import feedparser


KAGI_NEWS = 'https://kite.kagi.com'
NEWS_SECTIONS = ['world', 'usa', 'business', 'technology', 'science', 'sports', 'gaming']


def fetch_articles():
    all_articles = {}

    for section in NEWS_SECTIONS:
        print(f"Fetching {section} news...")
        feed = feedparser.parse(f'{KAGI_NEWS}/{section}.xml')

        articles = []
        for entry in feed.entries:
            content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else entry.get('summary', '')

            articles.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'content': content
            })

        all_articles[section] = articles
        print(f"  Fetched {len(articles)} articles")

    return all_articles
