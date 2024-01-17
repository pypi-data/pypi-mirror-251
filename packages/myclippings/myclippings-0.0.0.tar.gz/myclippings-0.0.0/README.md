# kindle-clippings

---

Converts `My Clippings.txt` file into a JSON format like below:

```json
[
    "Clean Code: A Handbook of Agile Software Craftsmanship": [
      {
        "id": "66698d9e",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Martin, Robert C.",
        "note_type": "highlight",
        "location": [892, 893],
        "date": "2022-10-12",
        "content": "Leave the campground cleaner than you found it."
      }
    ]
]
```

Currently, it supports English and Spanish languages.

## Usage

As a CLI tool:

```bash
python my_clippings/main.py
```

As a module:

```python
from my_clippings import clippings_to_json
```
