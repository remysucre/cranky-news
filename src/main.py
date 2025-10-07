#!/usr/bin/env python3

import json
from pathlib import Path
from rss_parser import fetch_all_sections
from particle_converter import convert_to_particle, save_particle_json, html_to_paragraphs, format_date


def main():
    print("Fetching Kagi News feeds...")
    all_sections = fetch_all_sections()

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for section_name, articles in all_sections.items():
        section_dir = output_dir / section_name
        section_dir.mkdir(exist_ok=True)

        section_content = {
            "format": "particle",
            "title": f"Kagi News - {section_name.title()}",
            "content": []
        }

        for article in articles:
            section_content['content'].append({
                "type": "paragraph",
                "text": f"*{article['title']}*"
            })

            if article.get('published'):
                section_content['content'].append({
                    "type": "paragraph",
                    "text": format_date(article['published'])
                })

            content = article.get('content', '')
            if content:
                paragraphs = html_to_paragraphs(content)
                for para in paragraphs:
                    section_content['content'].append({
                        "type": "paragraph",
                        "text": para
                    })

            section_content['content'].append({
                "type": "paragraph",
                "text": ""
            })

        index_path = section_dir / "index.json"
        save_particle_json(section_content, index_path)
        print(f"  ✓ Saved {section_name} to {index_path}")

    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"📁 Output directory: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
