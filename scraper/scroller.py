import random
import time

from scraper.parser import parse_post
from scraper.time_filter import is_within_last_hour

from config import (
    SCROLL_STEP_MIN,
    SCROLL_STEP_MAX,
    SCROLL_WAIT_MIN,
    SCROLL_WAIT_MAX,
    RECHECK_WAIT,
    MAX_EMPTY_SCROLLS,
)


def auto_scroll(page):
    """
    Scroll LinkedIn search results until a post older than 1 hour
    is reached or no more content is available.
    """

    print("\n========== Starting Auto Scroll ==========\n")

    start_time = time.time()

    scroll_count = 0
    empty_scrolls = 0

    main = page.locator("main")

    while True:

        posts = page.locator('[role="listitem"]').count()

        # Stop if last visible post is older than 1 hour
        if posts > 0:
            try:
                last_post = page.locator('[role="listitem"]').nth(posts - 1)
                text = last_post.inner_text()

                post = parse_post(text)

                posted = post.get("posted")

                if posted and not is_within_last_hour(posted):
                    print(f"\nReached post older than 1 hour ({posted})")
                    print("Stopping scroll...\n")
                    break

            except Exception as e:
                print(f"Timestamp check failed: {e}")

        current_top = main.evaluate("el => el.scrollTop")
        current_height = main.evaluate("el => el.scrollHeight")

        step = random.randint(
            SCROLL_STEP_MIN,
            SCROLL_STEP_MAX,
        )

        main.evaluate(
            f"(el) => el.scrollBy(0, {step})"
        )

        # Wait until new posts appear (max 5 seconds)
        start_wait = time.time()

        while time.time() - start_wait < 5:

            page.wait_for_timeout(300)

            new_posts = page.locator('[role="listitem"]').count()

            if new_posts > posts:
                print(f"Loaded new posts: {posts} -> {new_posts}")
                break

        new_top = main.evaluate("el => el.scrollTop")
        new_height = main.evaluate("el => el.scrollHeight")

        moved = abs(new_top - current_top) > 5
        loaded_new_content = (
            new_height > current_height or
            new_posts > posts
        )

        if not moved and not loaded_new_content:

            page.wait_for_timeout(RECHECK_WAIT)

            new_top = main.evaluate("el => el.scrollTop")
            new_height = main.evaluate("el => el.scrollHeight")

            moved = abs(new_top - current_top) > 5
            loaded_new_content = (
                new_height > current_height or
                page.locator('[role="listitem"]').count() > posts
            )

        scroll_count += 1

        print("-" * 55)
        print(f"Scroll #{scroll_count}")
        print(f"Visible Posts : {page.locator('[role=\"listitem\"]').count()}")

        if moved or loaded_new_content:
            empty_scrolls = 0
        else:
            empty_scrolls += 1

        if empty_scrolls >= MAX_EMPTY_SCROLLS:
            print("\nReached end of available content.\n")
            break

    duration = round(time.time() - start_time, 2)

    stats = {
        "scrolls": scroll_count,
        "visible_posts": page.locator('[role="listitem"]').count(),
        "duration_seconds": duration,
        "end_reason": "NO_MORE_CONTENT",
    }

    print("\n========== Scrolling Summary ==========")
    print(f"Total Scrolls : {stats['scrolls']}")
    print(f"Visible Posts : {stats['visible_posts']}")
    print(f"Duration      : {stats['duration_seconds']} sec")
    print(f"End Reason    : {stats['end_reason']}")
    print("=======================================\n")

    return stats