import unittest
import books

from importlib import reload


class TestBookInit(unittest.TestCase):
    def setUp(self) -> None:
        reload(books)

    def test_book_init_quantity(self):
        """
        Tests for ValueError error on negative init quantity.
        """
        def init():
            books.Book("Name", "Author", 2000, -1)
        self.assertRaises(ValueError, init)

    def test_book_init_existing_id(self):
        """
        Tests for BookIdClashException on creation of 2 Books with the same ID
        """
        def init():
            books.Book("Name2", "Author2", 1999, 2, ID=1)
        books.Book("Name", "Author", 2000, 1, ID=1)
        self.assertRaises(books.BookIdClashException, init)

    def test_book_init_passed_id(self):
        """
        Tests for initialization with a pre-set ID
        """
        self.assertIsInstance(books.Book("Name", "Author", 2000, 1, ID=1), books.Book)

    def test_book_init_blank_id(self):
        """
        Tests for initialization with no ID
        """
        self.assertIsInstance(books.Book("Name", "Author", 2000, 1), books.Book)


class TestBookMethods(unittest.TestCase):
    def setUp(self) -> None:
        reload(books)
        self.book_obj = books.Book("Name Name", "Author Author", 2000, 10, books.BookType(1), 1)

    def test_get_dict(self):
        """
        Test for a correct return from get_dict()
        """
        dict_return = self.book_obj.get_dict()
        expected = {
            "id": 1,
            "name": "Name Name",
            "author": "Author Author",
            "year": 2000,
            "total_quantity": 10,
            "type": 1
        }
        self.assertDictEqual(dict_return, expected)

    def test_str(self):
        """
        Test for a correct __str__ return
        """
        test_str = str(self.book_obj)
        expected_str = f"1: 10 of Name Name (2000) by Author Author"
        self.assertEqual(test_str, expected_str)

    def test_fields(self):
        """
        Tests static fields() method
        """
        test_list = self.book_obj.fields()
        expected_list = ['id', 'name', 'author', 'year', 'type', 'total_quantity']
        self.assertListEqual(test_list, expected_list)
