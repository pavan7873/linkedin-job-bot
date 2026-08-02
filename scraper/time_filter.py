import re

def post_age_in_minutes(posted: str):

    if not posted:
        return None

    posted = posted.lower().strip()

    match = re.match(r"(\d+)\s?(m|h|d|w|mo|yr)", posted)

    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    mapping = {
        "m": 1,
        "h": 60,
        "d": 1440,
        "w": 10080,
        "mo": 43200,
        "yr": 525600,
    }

    return value * mapping[unit]


def is_within_last_hour(posted):

    minutes = post_age_in_minutes(posted)

    if minutes is None:
        return False

    return minutes <= 300