import builtins
import csv
import os
import unittest

import util
from unittest.mock import patch


class TestUtilMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.folder_path = "./testfiles"
        self.file_path = create_test_csv(self.folder_path)

    def tearDown(self) -> None:
        try:
            os.remove(self.file_path)
        except IOError:
            pass

    def test_csv2arr(self):
        result = util.csv_to_arr(self.file_path)
        self.assertListEqual(result, get_test_list())

    def test_csv2arr_warnings(self):
        os.remove(self.file_path)
        with self.assertWarns(Warning):
            util.csv_to_arr(self.file_path)

    def test_arr2csv(self):
        fields = list(get_test_list()[0].keys())
        testpath = self.folder_path + "/test_arr2csv.csv"
        util.arr_to_csv(arr=get_test_list(),
                        fields=fields,
                        filepath=testpath)
        with open(self.file_path) as expected:
            with open(testpath) as test:
                expected_res = expected.readlines()
                test_res = test.readlines()
                self.assertListEqual(expected_res, test_res)
        os.remove(testpath)

    def test_arr2csv_warnings(self):
        fields = list(get_test_list()[0].keys())
        testpath = self.folder_path + "/test_arr2csv.csv"
        with patch.object(builtins, 'open', side_effect=IOError):
            self.assertWarns(UserWarning, util.arr_to_csv, arr=[{}], fields=fields, filepath=testpath)

    def test_append_csv(self):
        test_dict = {
            'id': '4',
            'name': 'Test Name',
            'author': 'Test Author',
            'year': '2010',
            'type': '2',
            'total_quantity': '100'
        }
        util.append_csv(test_dict, self.file_path)
        with open(self.file_path, mode='r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
            for iteration in range(3):
                next(reader)
            self.assertDictEqual(next(reader), test_dict)

    def test_append_csv_empty(self):
        os.remove(self.file_path)
        test_dict = {
            'id': '4',
            'name': 'Test Name',
            'author': 'Test Author',
            'year': '2010',
            'type': '2',
            'total_quantity': '100'
        }
        util.append_csv(test_dict, self.file_path)
        with open(self.file_path, mode='r', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, quoting=csv.QUOTE_ALL)
            with self.subTest("First Row"):
                self.assertDictEqual(next(reader), test_dict)

    def test_append_csv_error(self):
        with patch.object(builtins, 'open', side_effect=IOError):
            self.assertRaises(IOError, util.append_csv, item={}, filepath=self.file_path)


def create_test_csv(folder_path):
    """
    Creates a csv file matching a Book object at "{PATH}/test_book_list.csv"
    :param folder_path: A folder to create the file in
    :return: file path
    """
    with open(f"{folder_path}/test_book_list.csv", "w") as file:
        file.writelines([
            '"id","name","author","year","type","total_quantity"\n',
            '"1","Pride and Prejudice","Austen Jane","1998","2","30"\n',
            '"2","The Yellow Wallpaper","Gilman Charlotte Perkins","1999","3","28"\n',
            '"3","Alices Adventures in Wonderland","Carroll Lewis","1994","2","17"\n'
        ])
    return f"{folder_path}/test_book_list.csv"


def get_test_list():
    res = [
        {
            "id": "1",
            "name": "Pride and Prejudice",
            "author": "Austen Jane",
            "year": "1998",
            "type": "2",
            "total_quantity": "30"
        },
        {
            "id": "2",
            "name": "The Yellow Wallpaper",
            "author": "Gilman Charlotte Perkins",
            "year": "1999",
            "type": "3",
            "total_quantity": "28"
        },
        {
            "id": "3",
            "name": "Alices Adventures in Wonderland",
            "author": "Carroll Lewis",
            "year": "1994",
            "type": "2",
            "total_quantity": "17"
        }
    ]
    return res
