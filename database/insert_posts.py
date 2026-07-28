import json

from psycopg.types.json import Json

from database.connection import get_connection


def insert_posts(posts):
    """
    Inserts LinkedIn posts into PostgreSQL.

    Duplicate posts are ignored based on the primary key (id).
    """

    conn = get_connection()

    inserted = 0
    duplicates = 0

    query = """
    INSERT INTO linkedin_posts (
        id,
        author,
        headline,
        posted,
        post_url,
        text,
        emails,
        hashtags,
        search_keyword,
        scraped_at
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    ON CONFLICT (id)
    DO NOTHING;
    """

    with conn.cursor() as cur:

        for post in posts:

            cur.execute(
                query,
                (
                    post["id"],
                    post.get("author"),
                    post.get("headline"),
                    post.get("posted"),
                    post.get("post_url"),
                    post.get("text"),
                    Json(post.get("emails", [])),
                    Json(post.get("hashtags", [])),
                    post.get("search_keyword"),
                    post.get("scraped_at"),
                ),
            )

            if cur.rowcount == 1:
                inserted += 1
            else:
                duplicates += 1

    conn.commit()
    conn.close()

    return {
        "total": len(posts),
        "inserted": inserted,
        "duplicates": duplicates,
    }