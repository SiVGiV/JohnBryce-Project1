from dataclasses import dataclass
from enum import IntEnum


class BookType(IntEnum):
    """
    An enumerable representing a booktype (maximum loan period)
    """
    RET_IN_10 = 1
    RET_IN_5 = 2
    RET_IN_2 = 3

    def days(self):
        if self == 1:
            return 10
        if self == 2:
            return 5
        if self == 3:
            return 2

    def __repr__(self):
        return f"<RETURN IN {self.days()} DAYS>"

    def __str__(self):
        return f"{self.days()} days"

    @staticmethod
    def options():
        """
        returns a string specifying all possible options and their value.
        :return: Option string
        """
        option_string = ""
        for i in BookType:
            option_string += f"{i.value} = {str(BookType(i))}, "
        option_string = option_string[:-2]
        return option_string


@dataclass
class Book:
    """
    A class representing a single book in the library
    """
    __ID_MNGR = {"NEXT-ID": 0, "EXISTING-IDS": set()}
    name: str
    author: str
    year: int
    book_type: BookType = BookType.RET_IN_10
    ID: int = -1

    def __post_init__(self):
        if self.ID in Book.__ID_MNGR['EXISTING-IDS']:  # check if the book id exists already
            raise BookIdClashException
        if self.ID != -1:  # check if id wasn't left blank
            Book.__ID_MNGR['EXISTING-IDS'].add(self.ID)
            return
        while Book.__ID_MNGR['NEXT-ID'] in Book.__ID_MNGR['EXISTING-IDS']:  # find a new unique id to give the book
            Book.__ID_MNGR['NEXT-ID'] += 1
        self.ID = Book.__ID_MNGR['NEXT-ID']
        Book.__ID_MNGR['NEXT-ID'] += 1

    def get_dict(self):
        """
        returns a dict of the book
        :return: dict
        """
        loan_dict = {
            "id": self.ID,
            "name": self.name,
            "author": self.author,
            "year": self.year,
            "type": self.book_type.value
        }
        return loan_dict

    @staticmethod
    def fields():
        return ['id', 'name', 'author', 'year', 'type']

    def __str__(self):
        return f"{self.ID}: {self.name} ({self.year}) by {self.author}"


class BookException(Exception):
    pass


class BookIdClashException(BookException):
    def __str__(self):
        return "Book ID already exists"
