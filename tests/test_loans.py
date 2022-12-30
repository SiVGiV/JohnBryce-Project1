import unittest
import loans

from importlib import reload


class TestLoanInit(unittest.TestCase):
    def setUp(self) -> None:
        reload(loans)

    def test_loan_init_loandate(self):
        """
        Tests for loandate InvalidLoanDateException
        """
        def init_loandate():
            loans.Loan(0, 0, "abcd", "10/10/2020")
        self.assertRaises(loans.InvalidLoanDateException, init_loandate)

    def test_loan_init_returndate(self):
        """
        Tests for returndate InvalidLoanDateException
        """
        def init_returndate():
            loans.Loan(0, 0, "10/10/2020", "abcd")
        self.assertRaises(loans.InvalidLoanDateException, init_returndate)

    def test_loan_init_misordered_dates(self):
        """
        Tests for misordered dates: DateOrderException
        """
        def init_misordered():
            loans.Loan(0, 0, "11/10/2020", "10/10/2020")
        self.assertRaises(loans.DateOrderException, init_misordered)

    def test_loan_init_existing_id(self):
        """
        Tests for LoanIdClashException on creation of 2 IDs with the same ID
        """
        def init():
            loans.Loan(0, 0, "10/10/2020", "11/10/2020", ID=1)
        loans.Loan(0, 0, "10/10/2020", "11/10/2020", ID=1)
        self.assertRaises(loans.LoanIdClashException, init)

    def test_customer_init_passed_id(self):
        """
        Tests for initialization with a pre-set ID
        """
        self.assertIsInstance(loans.Loan(0, 0, "10/10/2020", "11/10/2020", ID=1), loans.Loan)

    def test_customers_init_blank_id(self):
        """
        Tests for initialization with no ID
        """
        self.assertIsInstance(loans.Loan(0, 0, "10/10/2020", "11/10/2020"), loans.Loan)


class TestLoanMethods(unittest.TestCase):
    def setUp(self) -> None:
        reload(loans)
        self.loan_obj = loans.Loan(0, 0, "10/10/2020", "11/10/2020")

    def test_is_late(self):
        """
        Test the .is_late() method
        """
        self.assertEqual(self.loan_obj.is_late(), True)

    def test_get_dict(self):
        """
        Test for a correct return from get_dict()
        """
        dict_return = self.loan_obj.get_dict()
        expected = {
            "id": 0,
            "custID": 0,
            "bookID": 0,
            "loan_date": "10/10/2020",
            "return_date": "11/10/2020"
        }
        self.assertDictEqual(dict_return, expected)

    def test_str(self):
        """
        Test for a correct __str__ return
        """
        test_str = str(self.loan_obj)
        expected_str = "0: 0 -> 0 on 10/10/2020 until 11/10/2020"
        self.assertEqual(test_str, expected_str)

    def test_fields(self):
        """
        Tests static fields() method
        """
        test_list = self.loan_obj.fields()
        expected_list = ['id', 'custID', 'bookID', 'loan_date', 'return_date']
        self.assertListEqual(test_list, expected_list)
