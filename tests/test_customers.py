import unittest
import customers

from importlib import reload


class TestCustomerInit(unittest.TestCase):
    def setUp(self) -> None:
        reload(customers)

    def test_customer_init_birthyear(self):
        """
        Tests for BirthYearException error on future years.
        """
        def init():
            customers.Customer("Name", "City", 2500)
        self.assertRaises(customers.BirthYearException, init)

    def test_customer_init_existing_id(self):
        """
        Tests for CustomerIdClashException on creation of 2 Customers with the same ID
        """
        def init():
            customers.Customer("Name2", "City2", 1999, ID=1)
        customers.Customer("Name", "City", 2000, ID=1)
        self.assertRaises(customers.CustomerIdClashException, init)

    def test_customer_init_passed_id(self):
        """
        Tests for initialization with a pre-set ID
        """
        self.assertIsInstance(customers.Customer("Name", "City", 2000, ID=1), customers.Customer)

    def test_customers_init_blank_id(self):
        """
        Tests for initialization with no ID
        """
        self.assertIsInstance(customers.Customer("Name", "City", 2000), customers.Customer)


class TestCustomerMethods(unittest.TestCase):
    def setUp(self) -> None:
        reload(customers)
        self.customer_obj = customers.Customer("Name Name", "City", 2000, 1)

    def test_get_dict(self):
        """
        Test for a correct return from get_dict()
        """
        dict_return = self.customer_obj.get_dict()
        expected = {
            "id": 1,
            "name": "Name Name",
            "city": "City",
            "birth_year": 2000
        }
        self.assertDictEqual(dict_return, expected)

    def test_str(self):
        """
        Test for a correct __str__ return
        """
        test_str = str(self.customer_obj)
        expected_str = f"1: Name Name"
        self.assertEqual(test_str, expected_str)

    def test_fields(self):
        """
        Tests static fields() method
        """
        test_list = self.customer_obj.fields()
        expected_list = ['id', 'name', 'city', 'birth_year']
        self.assertListEqual(test_list, expected_list)
