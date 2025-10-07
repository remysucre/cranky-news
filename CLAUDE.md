# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project mirrors articles from Kagi News (kite.kagi.com) and converts them to the [particle](https://browser.particlestudios.eu/#particle-formatting) web format for display in the [Constellation browser](https://browser.particlestudios.eu) on the [Playdate console](https://play.date).

## Data Flow

1. **Source**: Kagi News RSS feeds at https://kite.kagi.com/{section}.xml
2. **Sections**: world, usa, business, technology, science, sports, gaming
3. **Processing**: RSS feeds contain full article text in HTML format - parse with BeautifulSoup
4. **Output**: Each section gets its own directory with a single `index.json` containing all articles

## Architecture

**Key Characteristics:**
- RSS feeds contain **full article content** in HTML format - no web scraping required
- All articles for a section are combined into one `index.json` file per section
- Source tags like `[reuters.com#2][firstpost.com#1]` are stripped from article text
- Published dates are formatted as "07 Oct 2025" instead of full RFC 2822 format

**Key Files:**
- `src/rss_parser.py` - Fetches RSS feeds from all 7 sections
- `src/particle_converter.py` - Converts HTML content to particle format, strips source tags, formats dates
- `src/main.py` - Main orchestrator that creates `{section}/index.json` for each section
- `.github/workflows/fetch-kagi-news.yml` - GitHub Action scheduled for 12:30 UTC daily

**Output Structure:**
- `output/world/index.json` - All world articles
- `output/usa/index.json` - All USA articles
- `output/business/index.json` - All business articles
- etc.

## Automation

- GitHub Action cron job scheduled for 12:30 UTC daily (30 minutes past noon)
- Outputs resulting JSON files to GitHub Pages project site

## Particle Format

Output must conform to the particle web format specification. Reference the particle documentation at https://browser.particlestudios.eu/#particle-formatting for format details.
