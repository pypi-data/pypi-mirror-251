import re

import dateparser

TRANSLATIONS = {
    "note_type": {
        "note": ["note", "nota", "的笔记"],
        "highlight": ["highlight", "subrayado"],
        "bookmark": ["bookmark", "marcador"],
        "dividers": ["页"],
    },
    "location": ["Location", "posición"],
}

title_author_regex = re.compile(
    r"(?P<title>.+)(?:\(|\[|\-)(?P<author>(?<=\(|\[|\-).+?(?=\)|\]|$))"
)
position_regex = re.compile(r"(\d+)-?(\d+)?")


def parse_title_and_author(title_and_author: str):
    """Parse title and author from the raw clipping."""
    result = title_author_regex.findall(title_and_author)
    if result:
        title, author = result[0]
        title = title.strip()
        author = author.strip()
        return title, author
    else:
        for word in TRANSLATIONS["location"]:
            if word in title_and_author.lower():
                return "", ""

        return title_and_author, ""


def parse_metadata(metadata: str):
    """Parse metadata from the raw clipping."""
    result = metadata.split("|")

    note_type = parse_note_type(result[0])
    location = parse_location(result[1]) if len(result) == 3 else None
    date = parse_date(result[2]) if len(result) == 3 else parse_date(result[1])

    return note_type, location, date


def parse_location(raw_location: str):
    """Parse location into a tuple."""
    try:
        result = position_regex.findall(raw_location)
        if result:
            start, end = result[0]
            start = int(start)
            end = int(end) if end else None
            return (start, end) if start and end else (start)
    except Exception:
        return None


def parse_date(raw_date: str):
    """Parse date into a tuple."""
    try:
        result = raw_date.replace(",", "").split(" ")

        # Remove two letter words from the list that are not numbers
        result = [word for word in result if len(word) > 2 or word.isdigit()]

        month = result[2]
        day = result[3]
        year = result[4]

        date = day + " " + month + " " + year
        date = dateparser.parse(date).strftime("%Y-%m-%d")
        return date
    except Exception:
        return None


def parse_note_type(raw_note_type: str):
    """Parse note type into a string."""
    try:
        for key, value in TRANSLATIONS["note_type"].items():
            if any(word in raw_note_type.lower() for word in value):
                return key
    except Exception:
        return None
