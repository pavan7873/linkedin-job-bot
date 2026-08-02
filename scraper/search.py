# scraper/search.py
from scraper.time_filter import is_within_last_hour
# scraper/search.py

from urllib.parse import quote
from scraper.parser import parse_post
from config import WAIT_TIME
from scraper.url_builder import build_search_url
from scraper.scroller import auto_scroll
from datetime import datetime

def search_keyword(page, keyword):

    posts_data = []

    url = build_search_url(keyword)

    page.goto(
        url,
        wait_until="domcontentloaded"
    )

    # Wait until the page has at least one post
    page.locator('[role="listitem"]').first.wait_for(timeout=15000)

    # Small buffer to let LinkedIn finish rendering
    page.wait_for_timeout(1000)
    
    print(page.evaluate("window.innerHeight"))
    print(page.evaluate("document.body.scrollHeight"))
    print(page.evaluate("window.scrollY"))
    # page.pause()
    # Scroll until no more posts load
    scroll_stats = auto_scroll(page)

    print(scroll_stats)
    page.wait_for_timeout(WAIT_TIME)

    posts = page.locator('[role="listitem"]')

    print(f"Parsing {posts.count()} posts...\n")

    for i in range(posts.count()):

        text = posts.nth(i).inner_text()
        post = parse_post(text)
        posted = post.get("posted")

        if posted and is_within_last_hour(posted):
            post["search_keyword"] = keyword
            post["scraped_at"] = datetime.now().isoformat(timespec="seconds")
            posts_data.append(post)   
    return posts_data