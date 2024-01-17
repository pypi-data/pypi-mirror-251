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

    # Save parsed clippings to json file
    # with open("clippings.json", "w", encoding="utf-8") as f:
    #     json.dump(books, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    clippings_to_json()
