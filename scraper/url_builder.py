from urllib.parse import quote

from config import SORT_BY, DATE_POSTED


def build_search_url(keyword):

    return (
        "https://www.linkedin.com/search/results/content/"
        f"?keywords={quote(keyword)}"
        "&origin=FACETED_SEARCH"
        f'&sortBy=["{SORT_BY}"]'
        f'&datePosted=["{DATE_POSTED}"]'
    )