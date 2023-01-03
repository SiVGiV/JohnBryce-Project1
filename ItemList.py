import csv
import os
from loans import Loan, LoanIdClashException
from books import Book, BookType, BookIdClashException
from customers import Customer, CustomerIdClashException
import warnings
import util


def create_item(**kwargs):
    """
    Creates item of type specified by 'item_type'
    :param kwargs: 'item_type' - Type of item to create. Additional arguments as needed by type's init method.
    :return: Object of type specified
    """
    if 'item_type' not in kwargs:
        raise ValueError('create_item() must receive "item_type" as argument')
    if kwargs['item_type'] is Book:
        new_item = Book(
            name=kwargs['name'],
            author=kwargs['author'],
            year=int(kwargs['year']),
            total_quantity=int(kwargs['total_quantity']),
            book_type=BookType(int(kwargs['type'])),
            ID=int(kwargs['id'])
        )
        return new_item
    elif kwargs['item_type'] is Customer:
        new_item = Customer(
            name=kwargs['name'],
            city=kwargs['city'],
            birth_year=int(kwargs['birth_year']),
            ID=int(kwargs['id'])
        )
        return new_item
    elif kwargs['item_type'] is Loan:
        new_item = Loan(
            custID=int(kwargs['custID']),
            bookID=int(kwargs['bookID']),
            loandate=kwargs['loan_date'],
            returndate=kwargs['return_date'],
            ID=int(kwargs['id'])
        )
        return new_item
    else:
        raise ValueError("Argument item type does not match any supported classes.")


class ItemList:
    def __init__(self, item_type, db_path):
        self.__list = {}
        self.__item_type = item_type
        self.__db_path = db_path
        self.__init_file()
        self.load_from_csv(db_path)

    def __init_file(self):
        """
        Creates a new csv file if one doesn't exist.
        :return: None
        """
        util.verify_path(self.__db_path)
        if not os.path.exists(self.__db_path):
            with open(self.__db_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile,
                                        fieldnames=self.__item_type.fields(),
                                        quoting=csv.QUOTE_ALL)
                writer.writeheader()

    def load_from_csv(self, path):
        """
        Loads items from a csv file.
        :param path: Path to a csv file
        :return: None
        """
        file_res = util.csv_to_arr(path)
        fail_count = 0
        success_count = 0
        for data in file_res:
            try:
                new_item = create_item(item_type=self.__item_type, **data)
                self.add(new_item, to_file=False)
            except (ValueError, TypeError) as e:
                warnings.warn("Line parse failed. " + str(e))
                fail_count += 1
            except (LoanIdClashException, BookIdClashException, CustomerIdClashException):
                warnings.warn("Cannot create 2 items with identical IDs")
                fail_count += 1
            else:
                success_count += 1
        print("{0} items of type {2} imported from CSV ({0} succeeded, {1} failed)".format(success_count,
                                                                                           fail_count,
                                                                                           self.__item_type))

    def rewrite_db(self):
        items = []
        for item in self.__list.values():
            items.append(item.get_dict())
        util.arr_to_csv(items, self.__item_type.fields(), self.__db_path)

    def add(self, new_item, to_file: bool = True):
        """
        Adds an object to the list
        :param new_item: A Loan object to add
        :param to_file: whether the new loan should be written to file or not.
        :return: None
        """
        if new_item.ID in self.__list:
            raise ItemExistsError
        self.__list[new_item.ID] = new_item
        if to_file:
            try:
                util.append_csv(new_item.get_dict(), self.__db_path)
            except FileNotFoundError:
                self.rewrite_db()

    def remove(self, rem):
        """
        Removes an item from the list, raises ItemDoesNotExistError if not found.
        :param rem: the item object to remove or its ID
        :return: None
        """
        if isinstance(rem, int):  # remove by ID
            if rem in self.__list:
                removed = self.__list.pop(rem)
                self.rewrite_db()
                return removed
            else:
                raise ItemDoesNotExistError
        elif isinstance(rem, self.__item_type):
            if rem in self.__list.values():
                removed = self.__list.pop(rem.ID)
                self.rewrite_db()
                return removed
            else:
                raise ItemDoesNotExistError
        else:
            raise TypeError("ItemList.remove() only accepts objects of the type they are assigned to or IDs")

    def get_by_property(self, search_field: str, search_value):
        """
        Returns all items that match a search.
        :param search_field: property name to search
        :param search_value: property value to match
        :return: list of all matches
        """
        results = []
        fields = self.__item_type.fields()
        if search_field not in fields:
            raise ValueError("Search field does not exist.")
        for item in self:
            item_dict = item.get_dict()
            if isinstance(item_dict[search_field], str):
                if str(search_value.lower()) in item_dict[search_field].lower():
                    results.append(item)
            elif isinstance(item_dict[search_field], int):
                if search_value == item_dict[search_field]:
                    results.append(item)
        return results

    def get_list_type(self):
        return self.__item_type

    def __iter__(self):
        for ID, item in self.__list.items():
            yield item

    def __repr__(self):
        return f"<{len(self.__list)} items of type {self.__item_type}>"

    def __str__(self):
        return f"List of {len(self.__list)} {self.__item_type}s"

    def __iadd__(self, other):
        """
        Adds another list or loan to self using the add() method
        :param other: A LoanList or Loan object
        :return: self (object on the left of the symbol)
        """
        if isinstance(other, ItemList):
            if isinstance(other.get_list_type(), self.__item_type):
                for item in other:
                    self.add(item)
                return self
            raise TypeError("Cannot add list of type " +
                            str(type(other.__item_type)) +
                            " to list of type " +
                            str(type(self.__item_type)))
        if isinstance(other, self.__item_type):
            self.add(other)
            return self
        raise TypeError("Cannot add " + str(type(other)) + " to ItemList")


class ItemListException(Exception):
    pass


class ItemExistsError(ItemListException):
    def __str__(self):
        return f"Item already exists in the list"


class ItemDoesNotExistError(ItemListException):
    def __str__(self):
        return "Trying to access a non existing item"
