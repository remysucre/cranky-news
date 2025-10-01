"""Convert parsed articles to particle format for Constellation browser."""

import json


def convert_to_particle(article):
    """
    Convert article data to particle JSON format.

    Args:
        article: Dictionary with title, byline, date, paragraphs

    Returns:
        Dictionary in particle format
    """
    # Build particle document
    # Based on particle format spec - simple text-based format
    title = article.get('title', 'Untitled')

    # Truncate title to 40 characters and convert to ASCII
    if len(title) > 40:
        title = title[:37] + "..."
    title = title.encode('ascii', 'ignore').decode('ascii')

    particle = {
        "format": "particle",
        "title": title,
        "content": []
    }

    # Add title as paragraph (bold)
    if article.get('title'):
        particle['content'].append({
            "type": "paragraph",
            "text": f"*{article['title']}*"
        })

    # Add byline and date if available
    if article.get('byline') or article.get('date'):
        metadata_text = []
        if article.get('byline'):
            metadata_text.append(article['byline'])
        if article.get('date'):
            metadata_text.append(article['date'])

        particle['content'].append({
            "type": "paragraph",
            "text": " | ".join(metadata_text)
        })

    # Add article paragraphs (exclude last paragraph which is fineprint)
    paragraphs = article.get('paragraphs', [])
    if paragraphs:
        # Discard the last paragraph
        paragraphs = paragraphs[:-1]

    for para in paragraphs:
        if para:
            particle['content'].append({
                "type": "paragraph",
                "text": para
            })

    return particle


def save_particle_json(particle_data, output_path):
    """
    Save particle data to JSON file.

    Args:
        particle_data: Particle format dictionary
        output_path: Path to save JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(particle_data, f, indent=2, ensure_ascii=False)
