# scraper/parser.py

import re
from scraper.enricher import extract_skills

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"


def parse_post(text: str):

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    author = ""
    headline = ""
    posted = ""

    if len(lines) > 1:
        author = lines[1]

    # Find timestamp
    match = re.search(r"\b(\d+\s?(?:m|h|d|w|mo|yr))\b", text)

    if match:
        posted = match.group(1)

    # Headline is usually after "• 1st/2nd/3rd+"
    for i, line in enumerate(lines):

        if "•" in line and i + 1 < len(lines):
            headline = lines[i + 1]
            break

    skills = extract_skills(text)
    
    emails = re.findall(EMAIL_REGEX, text)

    hashtags = re.findall(r"#(\w+)", text)

    return {
        "author": author,
        "headline": headline,
        "posted": posted,
        "emails": emails,
        "hashtags": hashtags,
        "text": text,
    }