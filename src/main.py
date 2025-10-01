#!/usr/bin/env python3
"""Main script to fetch CSM articles and convert to particle format."""

import os
import sys
from pathlib import Path
from datetime import datetime

from rss_parser import fetch_rss_feed, convert_to_text_edition_url
from html_parser import fetch_article_content
from particle_converter import convert_to_particle, save_particle_json


def main():
    """Main processing pipeline."""
    print("Fetching CSM RSS feed...")
    articles = fetch_rss_feed()
    print(f"Found {len(articles)} articles in feed")

    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    articles_dir = output_dir / "articles"
    articles_dir.mkdir(exist_ok=True)

    # Track processing stats
    successful = 0
    failed = 0
    index_entries = []

    # Process each article
    for i, article_meta in enumerate(articles[:10], 1):  # Limit to 10 for testing
        print(f"\n[{i}/{min(10, len(articles))}] Processing: {article_meta['title'][:50]}...")

        # Convert to text edition URL
        text_url = convert_to_text_edition_url(article_meta['link'])
        print(f"  URL: {text_url}")

        # Fetch article content
        article = fetch_article_content(text_url)

        if not article:
            print("  ❌ Failed to fetch article")
            failed += 1
            continue

        if not article['paragraphs']:
            print("  ⚠️  No content found")
            failed += 1
            continue

        # Convert to particle format
        particle = convert_to_particle(article)

        # Generate filename from URL slug
        url_parts = article_meta['link'].rstrip('/').split('/')
        slug = url_parts[-1] if url_parts else f"article_{i}"
        # Strip query parameters like ?icid=rss
        slug = slug.split('?')[0]
        filename = f"{slug}.json"
        output_path = articles_dir / filename

        # Save to file
        save_particle_json(particle, output_path)
        print(f"  ✓ Saved to {output_path}")
        successful += 1

        # Add to index
        index_entries.append({
            "title": article_meta['title'],
            "summary": article_meta.get('summary', ''),
            "slug": slug
        })

    # Create index.json
    create_index(output_dir, index_entries)

    # Summary
    print(f"\n{'='*50}")
    print(f"Processing complete:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📁 Output directory: {output_dir.absolute()}")


def create_index(output_dir, entries):
    """
    Create an index.json file with article listings.

    Args:
        output_dir: Directory to save index.json
        entries: List of article metadata dictionaries
    """
    import json

    # Build particle format index page
    index = {
        "format": "particle",
        "title": "Christian Science Monitor Articles",
        "content": []
    }

    # Add each article entry
    for entry in entries:
        # Article title (bold)
        index['content'].append({
            "type": "paragraph",
            "text": f"*{entry['title']}*"
        })

        # Summary
        if entry['summary']:
            index['content'].append({
                "type": "paragraph",
                "text": entry['summary']
            })

        # Link button
        index['content'].append({
            "type": "button",
            "label": "Read full article",
            "action": f"/articles/{entry['slug']}"
        })

        # Spacer
        index['content'].append({
            "type": "paragraph",
            "text": ""
        })

    # Save index
    index_path = output_dir / "index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Created index at {index_path}")


if __name__ == "__main__":
    main()
