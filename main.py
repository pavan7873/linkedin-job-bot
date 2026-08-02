from playwright.sync_api import sync_playwright

from config import SEARCH_PREFIX, SEARCH_KEYWORDS, HEADLESS
from scraper.search import search_keyword
from scraper.merger import merge_results
from database.insert_posts import insert_posts
from webhook import trigger_n8n

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

            print("\n" + "=" * 70)
            print(f"Searching: {keyword}")
            print("=" * 70)

            try:
                posts = search_keyword(page, keyword)

                print(f"Posts Scraped : {len(posts)}")

                if not posts:
                    print("No posts found.")
                    continue

                unique_posts = merge_results(posts)

                print(f"Unique Posts  : {len(unique_posts)}")

                stats = insert_posts(unique_posts)

                print(f"Inserted      : {stats['inserted']}")
                print(f"Duplicates    : {stats['duplicates']}")

                total_scraped += len(posts)
                total_unique += len(unique_posts)
                total_inserted += stats["inserted"]
                total_duplicates += stats["duplicates"]

            except Exception as e:
                print(f"\nError while processing '{keyword}'")
                print(e)
                print("Continuing with next keyword...\n")
                continue

        browser.close()

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Total Scraped    : {total_scraped}")
    print(f"Total Unique     : {total_unique}")
    print(f"Inserted         : {total_inserted}")
    print(f"Duplicates       : {total_duplicates}")
    print("=" * 70)
    summary = {
        "total_scraped": total_scraped,
        "inserted": total_inserted,
        "duplicates": total_duplicates,
    }

    trigger_n8n(summary)

if __name__ == "__main__":
    main()