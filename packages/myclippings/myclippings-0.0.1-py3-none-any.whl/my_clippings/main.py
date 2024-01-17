import json
import sys

from my_clippings.classes.clipping import Clipping
from my_clippings.utils.reader import read_clippings_file_into_array


def clippings_to_json(my_clippings_file: str):
    """ """
    books = {}

    for raw_clipping in read_clippings_file_into_array(my_clippings_file):
        try:
            parsed_clipping = Clipping(raw_clipping).parsed
            current_book = parsed_clipping.get("title")

            if current_book not in books:
                books[current_book] = [parsed_clipping]
            else:
                books[current_book].append(parsed_clipping)

        except Exception as e:
            print(f"An error occurred: {e}")

    return books


if __name__ == "__main__":
    print("hello")
    print(sys.argv[1])
    file_name = sys.argv[1] if len(sys.argv) > 1 else "My Clippings.txt"
    books = clippings_to_json(file_name)

    with open("books.json", "w") as fp:
        json.dump(books, fp)
