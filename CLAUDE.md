# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project mirrors articles from the Christian Science Monitor's text edition and converts them to the [particle](https://browser.particlestudios.eu/#particle-formatting) web format for display in the [Constellation browser](https://browser.particlestudios.eu) on the [Playdate console](https://play.date).

## Data Flow

1. **Source**: CSM RSS feed at https://rss.csmonitor.com/feeds/all
2. **Text Edition URLs**: Regular article URLs can be converted to text edition by inserting `/text_edition` after `www.csmonitor.com`
   - Example: `https://www.csmonitor.com/World/Middle-East/2025/0930/palestinian-reaction-trump-gaza-ceasefire-plan`
   - Becomes: `https://www.csmonitor.com/text_edition/World/Middle-East/2025/0930/palestinian-reaction-trump-gaza-ceasefire-plan`
3. **Processing**: Parse the simple HTML structure from text edition pages and convert to particle format
4. **Output**: JSON files for the Constellation browser

## Automation

- GitHub Action cron job scheduled for 6am PT daily
- Outputs resulting JSON files to GitHub Pages project site

## Particle Format

Output must conform to the particle web format specification. Reference the particle documentation at https://browser.particlestudios.eu/#particle-formatting for format details.
