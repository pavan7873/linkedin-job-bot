from database.connection import get_connection


def create_tables():
    """
    Creates all required database tables.
    """

    create_posts_table = """
    CREATE TABLE IF NOT EXISTS linkedin_posts (

        id TEXT PRIMARY KEY,

        author TEXT,
        headline TEXT,
        posted TEXT,

        post_url TEXT,

        text TEXT,

        emails JSONB,
        hashtags JSONB,

        search_keyword TEXT,
        scraped_at TIMESTAMP,

        company TEXT,
        job_title TEXT,
        location TEXT,

        is_hiring BOOLEAN,

        match_score INTEGER,

        email_generated BOOLEAN DEFAULT FALSE,
        email_sent BOOLEAN DEFAULT FALSE,

        status TEXT DEFAULT 'SCRAPED',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );
    """

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(create_posts_table)

    conn.commit()
    conn.close()

    print("linkedin_posts table created successfully.")