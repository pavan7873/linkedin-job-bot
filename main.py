from playwright.sync_api import sync_playwright

from config import SEARCH_PREFIX, SEARCH_KEYWORDS, HEADLESS
from scraper.search import search_keyword
from scraper.merger import merge_results
from database.insert_posts import insert_posts
from webhook import trigger_n8n

from datetime import datetime
import os

def log(msg):
    with open(r"C:\Users\pavan\Projects\linkedin-job-bot\debug.txt", "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")


def main():

    total_scraped = 0
    total_unique = 0
    total_inserted = 0
    total_duplicates = 0

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=HEADLESS)

        context = browser.new_context(
            storage_state="./auth/state.json"
        )

        page = context.new_page()

        for skill in SEARCH_KEYWORDS:

            keyword = f"{SEARCH_PREFIX} {skill}"

            log("\n" + "=" * 70)
            log(f"Searching: {keyword}")
            log("=" * 70)

            try:
                posts = search_keyword(page, keyword)

                log(f"Posts Scraped : {len(posts)}")

                if not posts:
                    log("No posts found.")
                    continue

                unique_posts = merge_results(posts)

                log(f"Unique Posts  : {len(unique_posts)}")

                stats = insert_posts(unique_posts)

                log(f"Inserted      : {stats['inserted']}")
                log(f"Duplicates    : {stats['duplicates']}")

                total_scraped += len(posts)
                total_unique += len(unique_posts)
                total_inserted += stats["inserted"]
                total_duplicates += stats["duplicates"]

            except Exception as e:
                log(f"\nError while processing '{keyword}'")
                log(e)
                log("Continuing with next keyword...\n")
                continue

        browser.close()

    log("\n" + "=" * 70)
    log("FINAL SUMMARY")
    log("=" * 70)
    log(f"Total Scraped    : {total_scraped}")
    log(f"Total Unique     : {total_unique}")
    log(f"Inserted         : {total_inserted}")
    log(f"Duplicates       : {total_duplicates}")
    log("=" * 70)
    summary = {
        "total_scraped": total_scraped,
        "inserted": total_inserted,
        "duplicates": total_duplicates,
    }

    trigger_n8n(summary)
    log(30*"###")

if __name__ == "__main__":
    main()
    