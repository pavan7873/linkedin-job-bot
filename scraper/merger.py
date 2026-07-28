import hashlib
import json
import os

from config import OUTPUT_DIR


def generate_post_id(post):

    unique_string = (
        post.get("author", "").strip().lower()
        + post.get("posted", "").strip().lower()
        + post.get("text", "").strip().lower()
    )

    return hashlib.sha256(
        unique_string.encode("utf-8")
    ).hexdigest()

def merge_results(posts):

    seen = set()
    unique_posts = []

    for post in posts:

        post_id = generate_post_id(post)

        if post_id not in seen:

            seen.add(post_id)

            new_post = {
                **post,
                "id": post_id
            }

            unique_posts.append(new_post)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_DIR,
        "merged_posts.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            unique_posts,
            f,
            indent=4,
            ensure_ascii=False
        )

    return unique_posts