from collections import namedtuple

TitleAndAuthorTestCase = namedtuple("TestCase", "input title author")
title_and_author_tests = [
    TitleAndAuthorTestCase(
        "The Ultimate Hitchhiker's Guide to the Galaxy: Five Novels in One Outrageous Volume",
        "The Ultimate Hitchhiker's Guide to the Galaxy: Five Novels in One Outrageous Volume",
        "",
    ),
    TitleAndAuthorTestCase(
        "Meditations (Marcus Aurelius)", "Meditations", "Marcus Aurelius"
    ),
    TitleAndAuthorTestCase(
        "To Kill A Mockingbird (Harper Lee)", "To Kill A Mockingbird", "Harper Lee"
    ),
    TitleAndAuthorTestCase(
        "A Mind For Numbers (Barbara Oakley)", "A Mind For Numbers", "Barbara Oakley"
    ),
    TitleAndAuthorTestCase(
        "The Autobiography of Benjamin Franklin (AmazonClassics Edition) (Franklin, Benjamin)",
        "The Autobiography of Benjamin Franklin (AmazonClassics Edition)",
        "Franklin, Benjamin",
    ),
    TitleAndAuthorTestCase(
        "Altered Traits (Daniel Goleman;Richard Davidson)",
        "Altered Traits",
        "Daniel Goleman;Richard Davidson",
    ),
    TitleAndAuthorTestCase(
        "Madhouse at the End of the Earth: The Belgica's Journey into the Dark Antarctic Night (Julian Sancton)",
        "Madhouse at the End of the Earth: The Belgica's Journey into the Dark Antarctic Night",
        "Julian Sancton",
    ),
    TitleAndAuthorTestCase(
        "Joel on Software: And on Diverse and Occasionally Related Matters That Will Prove of Interest to Software Developers, Designers, and Managers, and to Those Who, Whether by Good Fortune or Ill Luck, Work with Them in Some Capacity (Joel Spolsky)",
        "Joel on Software: And on Diverse and Occasionally Related Matters That Will Prove of Interest to Software Developers, Designers, and Managers, and to Those Who, Whether by Good Fortune or Ill Luck, Work with Them in Some Capacity",
        "Joel Spolsky",
    ),
    TitleAndAuthorTestCase(
        "Alex's Adventures in Numberland (Bellos, Alex)",
        "Alex's Adventures in Numberland",
        "Bellos, Alex",
    ),
    TitleAndAuthorTestCase(
        "Code Complete, Second Edition eBook - Steve McConnell",
        "Code Complete, Second Edition eBook",
        "Steve McConnell",
    ),
    TitleAndAuthorTestCase("", "", ""),
]

MetadataTestCase = namedtuple("TestCase", "input note_type location date")
metadata_tests = [
    MetadataTestCase(
        "Your Highlight on page 31 | Location 447-448 | Added on Saturday, January 6, 2024",
        "highlight",
        (447, 448),
        "2024-01-06",
    ),
    MetadataTestCase(
        "Your Highlight on page 47 | Location 723 | Added on Sunday, January 7, 2024 10:25:48 AM",
        "highlight",
        (723),
        "2024-01-07",
    ),
    MetadataTestCase(
        "Your Highlight on page 107 | Location 1709-1711 | Added on Wednesday, January 10, 2024 1:20:25 PM",
        "highlight",
        (1709, 1711),
        "2024-01-10",
    ),
    MetadataTestCase(
        "Your Highlight on page 107 | Added on Wednesday, January 10, 2024 1:20:25 PM",
        "highlight",
        None,
        "2024-01-10",
    ),
    MetadataTestCase(
        "La subrayado en la página 236 | posición 3614-3615 | Añadido el lunes, 10 de julio de 2023 13:23:06",
        "highlight",
        (3614, 3615),
        "2023-07-10",
    ),
    MetadataTestCase(
        "La subrayado en la página 236 | posición 3614-3615 | Añadido el lunes, 10 de julio de 2023 13:23:06",
        "highlight",
        (3614, 3615),
        "2023-07-10",
    ),
]

DateTestCase = namedtuple("TestCase", "input date")
date_tests = [
    DateTestCase("Added on Sunday, January 7, 2024 10:25:48 AM", "2024-01-07"),
    DateTestCase("Added on Wednesday, January 10, 2024 1:20:25 PM", "2024-01-10"),
    DateTestCase("Added on Wednesday, January 10, 2024 1:20:25 PM", "2024-01-10"),
    DateTestCase("Added on Monday, January 8, 2024 1:20:25 PM", "2024-01-08"),
    DateTestCase("Añadido el lunes, 10 de julio de 2023 13:23:06", "2023-07-10"),
    DateTestCase("", None),
]

NoteTypeTestCase = namedtuple("TestCase", "input note_type")
note_type_tests = [
    NoteTypeTestCase("Your Highlight on page 31", "highlight"),
    NoteTypeTestCase("La subrayado en la página 236", "highlight"),
    NoteTypeTestCase("", None),
]
