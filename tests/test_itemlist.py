import csv
import os
import unittest
import ItemList
import books
import customers
import loans
from importlib import reload


class TestItemListInit(unittest.TestCase):
    def setUp(self) -> None:
        reload(books)
        reload(customers)
        reload(loans)
        reload(ItemList)

    def test_create_item_errors(self):
        with self.subTest("No item type passed"):
            self.assertRaises(ValueError, lambda: ItemList.create_item())
        with self.subTest("item_type isn't supported"):
            self.assertRaises(ValueError, lambda: ItemList.create_item(item_type=int))

    def test_create_item_returns(self):
        with self.subTest("create_item() of type Book"):
            self.assertIsInstance(ItemList.create_item(
                item_type=books.Book,
                name="Name Name",
                author="Author Author",
                year=1999,
                total_quantity=10,
                type=books.BookType.RET_IN_5,
                id=0
            ), books.Book)
        with self.subTest("create_item() of type Customer"):
            self.assertIsInstance(ItemList.create_item(
                item_type=customers.Customer,
                name="Name Name",
                city="City",
                birth_year=1999,
                id=0
            ), customers.Customer)
        with self.subTest("create_item() of type Loan"):
            self.assertIsInstance(ItemList.create_item(
                item_type=loans.Loan,
                custID=0,
                bookID=0,
                loan_date="01/01/2021",
                return_date="06/01/2021",
                id=0
            ), loans.Loan)

    def test_item_list_init(self):
        with self.subTest("init Book list"):
            self.assertIsInstance(ItemList.ItemList(books.Book, './testfiles/test_list.csv'), ItemList.ItemList)
        with self.subTest("init Customer list"):
            self.assertIsInstance(ItemList.ItemList(customers.Customer, './testfiles/test_list.csv'), ItemList.ItemList)
        with self.subTest("init Loan list"):
            self.assertIsInstance(ItemList.ItemList(loans.Loan, "./testfiles/test_list.csv"), ItemList.ItemList)


class TestItemListMethods(unittest.TestCase):
    def setUp(self):
        reload(books)
        reload(customers)
        reload(loans)
        reload(ItemList)
        self.folder_path = "./testfiles/"
        self.list = ItemList.ItemList(books.Book, "./testfiles/book_list.csv")

    def tearDown(self):
        os.remove("./testfiles/book_list.csv")

    def test_load_from_csv(self):
        create_test_csv(self.folder_path)
        self.list.load_from_csv(f"{self.folder_path}/test_book_list.csv")
        self.assertEqual(len(self.list), 3)

    def test_rewrite_db(self):
        create_test_csv(self.folder_path)
        self.list.load_from_csv(f"{self.folder_path}/test_book_list.csv")
        self.list.rewrite_db()
        res = []
        with open("./testfiles/book_list.csv") as csvfile:
            reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
            for row in reader:
                res.append(row)

        expected_res = [
            {'id': '1',
             'name': 'Pride and Prejudice',
             'author': 'Austen Jane',
             'year': '1998',
             'type': '2',
             'total_quantity': '30'
             },
            {'id': '2',
             'name': 'The Yellow Wallpaper',
             'author': 'Gilman Charlotte Perkins',
             'year': '1999',
             'type': '3',
             'total_quantity': '28'
             },
            {'id': '3',
             'name': 'Alices Adventures in Wonderland',
             'author': 'Carroll Lewis',
             'year': '1994',
             'type': '2',
             'total_quantity': '17'
             }
        ]
        self.assertListEqual(res, expected_res)

    def test_add(self):
        new_book = books.Book(
            name="Name",
            author="Author",
            year=1999,
            total_quantity=5,
            book_type=books.BookType.RET_IN_10
        )
        self.list.add(new_book)
        self.assertEqual(new_book, next(self.list.__iter__()))

    def test_add_exists_error(self):
        book1 = books.Book(
            name="Name",
            author="Author",
            year=1999,
            total_quantity=5,
            book_type=books.BookType.RET_IN_10,
            ID=0
        )
        self.list.add(book1)
        self.assertRaises(ItemList.ItemExistsError, lambda: self.list.add(book1))

    def test_add_with_missing_file(self):
        os.remove("./testfiles/book_list.csv")
        book1 = books.Book(
            name="Name",
            author="Author",
            year=1999,
            total_quantity=5,
            book_type=books.BookType.RET_IN_10,
            ID=0
        )
        self.list.add(book1)
        res = []
        with open("./testfiles/book_list.csv") as csvfile:
            reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
            for row in reader:
                res.append(row)
        expected_res = [
            {'id': '0',
             'name': 'Name',
             'author': 'Author',
             'year': '1999',
             'type': '1',
             'total_quantity': '5'
             }
        ]
        self.assertListEqual(res, expected_res)

    def test_remove(self):
        book1 = books.Book(
            name="Name",
            author="Author",
            year=1999,
            total_quantity=5,
            book_type=books.BookType.RET_IN_10,
            ID=0
        )
        self.list.add(book1)
        with self.subTest("Removal by object"):
            self.assertEqual(book1, self.list.remove(book1))
        self.list.add(book1)
        with self.subTest("Removal by ID"):
            self.assertEqual(book1, self.list.remove(0))

    def test_remove_item_doesnt_exist(self):
        book1 = books.Book(
            name="Name",
            author="Author",
            year=1999,
            total_quantity=5,
            book_type=books.BookType.RET_IN_10,
            ID=0
        )
        with self.subTest("Removal by object"):
            self.assertRaises(ItemList.ItemDoesNotExistError,
                              lambda: self.list.remove(book1))
        with self.subTest("Removal by ID"):
            self.assertRaises(ItemList.ItemDoesNotExistError,
                              lambda: self.list.remove(0))

    def test_remove_invalid_type(self):
        customer1 = customers.Customer(
            name="Name",
            city="City",
            birth_year=1999
        )
        self.assertRaises(TypeError, lambda: self.list.remove(customer1))

    def test_get_by(self):
        book1 = books.Book(
            name="Animal Farm",
            author="George Orwell",
            year=1984,
            total_quantity=50,
            book_type=books.BookType.RET_IN_5
        )
        self.list.add(book1)
        with self.subTest("Search for string"):
            self.assertListEqual([book1], self.list.get_by_property("name", "animal"))
        with self.subTest("Search for integer"):
            self.assertListEqual([book1], self.list.get_by_property("year", 1984))

    def test_get_by_errors(self):
        with self.subTest("Test in non existent search field"):
            self.assertRaises(ValueError, lambda: self.list.get_by_property("Lorem", "Ipsum"))

    def test_get_list_type(self):
        self.assertIs(self.list.get_list_type(), books.Book)


def create_test_csv(folder_path):
    """
    Creates a csv file matching a Book object at "{PATH}/test_book_list.csv"
    :param folder_path: A folder to create the file in
    :return: None
    """
    with open(f"{folder_path}/test_book_list.csv", "w") as file:
        file.writelines([
            '"id","name","author","year","type","total_quantity"\n',
            '"1","Pride and Prejudice","Austen Jane","1998","2","30"\n',
            '"2","The Yellow Wallpaper","Gilman Charlotte Perkins","1999","3","28"\n',
            '"3","Alices Adventures in Wonderland","Carroll Lewis","1994","2","17"\n'
        ])
