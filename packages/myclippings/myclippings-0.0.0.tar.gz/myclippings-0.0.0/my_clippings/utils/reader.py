import ftfy

SEPARATOR = "=========="
SECTIONS = {0: "title_and_author", 1: "metadata", 2: "content"}


def read_clippings_file_into_array(my_clippings_file):
    """Pre-process clippings file into array of clippings"""
    clippings = [{}]

    with open(my_clippings_file, "r", encoding="utf-8") as clippings_file:
        curr_line = 0
        index = 0

        for line in clippings_file:
            # If separator, start new clipping
            if line.strip() == SEPARATOR:
                curr_line = 0
                index += 1
                clippings.append({})
            # Skip empty lines
            elif line.strip() == "":
                continue
            # Clipping lines
            else:
                section = SECTIONS.get(curr_line, "Invalid")
                line = ftfy.fixes.remove_control_chars(line).strip()
                clippings[index][section] = line
                curr_line += 1

    # Remove empty clippings
    filtered_clippings = [clipping for clipping in clippings if clipping]

    return filtered_clippings
