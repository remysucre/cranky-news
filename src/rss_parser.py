"""RSS feed parser for Christian Science Monitor articles."""

import feedparser


def fetch_rss_feed(feed_url="https://rss.csmonitor.com/feeds/all"):
    """
    Fetch and parse the CSM RSS feed.

    Args:
        feed_url: URL of the RSS feed

    Returns:
        List of article entries with title, link, published date
    """
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'published': entry.get('published', ''),
            'summary': entry.get('summary', '')
        })

    return articles


def convert_to_text_edition_url(url):
    """
    Convert a standard CSM URL to its text edition equivalent.

    Args:
        url: Standard CSM article URL

    Returns:
        Text edition URL
    """
    if 'www.csmonitor.com' not in url:
        return url

    # Insert /text_edition after www.csmonitor.com
    return url.replace('www.csmonitor.com/', 'www.csmonitor.com/text_edition/')
