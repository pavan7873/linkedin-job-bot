import random
import time

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
    Scroll LinkedIn search results until no more content is loaded.

    Returns:
        dict: Scrolling statistics.
    """

    print("\n========== Starting Auto Scroll ==========\n")

    start_time = time.time()

    scroll_count = 0
    empty_scrolls = 0

    main = page.locator("main")

    while True:

        posts = page.locator('[role="listitem"]').count()

        current_top = main.evaluate("el => el.scrollTop")
        current_height = main.evaluate("el => el.scrollHeight")

        step = random.randint(
            SCROLL_STEP_MIN,
            SCROLL_STEP_MAX,
        )

        wait_time = random.randint(
            SCROLL_WAIT_MIN,
            SCROLL_WAIT_MAX,
        )

        main.evaluate(
            f"(el) => el.scrollBy(0, {step})"
        )

        page.wait_for_timeout(wait_time)

        new_top = main.evaluate("el => el.scrollTop")
        new_height = main.evaluate("el => el.scrollHeight")

        moved = abs(new_top - current_top) > 5
        loaded_new_content = new_height > current_height

        # Double check before considering end of feed
        if not moved and not loaded_new_content:

            page.wait_for_timeout(RECHECK_WAIT)

            new_top = main.evaluate("el => el.scrollTop")
            new_height = main.evaluate("el => el.scrollHeight")

            moved = abs(new_top - current_top) > 5
            loaded_new_content = new_height > current_height

        scroll_count += 1

        print("-" * 55)
        print(f"Scroll #{scroll_count}")
        print(f"Visible Posts : {posts}")
        print(f"Scroll Top    : {int(new_top)}")
        print(f"Scroll Height : {int(new_height)}")

        if moved or loaded_new_content:
            empty_scrolls = 0

            if loaded_new_content:
                status = "New content loaded"
            else:
                status = "Scrolling"

        else:
            empty_scrolls += 1
            status = f"No new content ({empty_scrolls}/{MAX_EMPTY_SCROLLS})"

        print(f"Status        : {status}")
        print("-" * 55)

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