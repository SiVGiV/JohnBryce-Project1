import re
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Loan:
    """
    A class representing a single book loan transaction
    """
    __ID_MNGR = {"NEXT-ID": 0, "EXISTING-IDS": set()}
    custID: int
    bookID: int
    loandate: str
    returndate: str
    ID: int = -1

    def __post_init__(self):
        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", self.loandate):
            raise InvalidLoanDateException

        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", self.returndate):
            raise InvalidLoanDateException

        if datetime.strptime(self.loandate, "%d/%m/%Y") > datetime.strptime(self.returndate, "%d/%m/%Y"):
            raise DateOrderException

        if self.ID in Loan.__ID_MNGR['EXISTING-IDS']:  # check if the Loan id exists already
            raise LoanIdClashException

        if self.ID != -1:  # check if id wasn't left blank
            Loan.__ID_MNGR['EXISTING-IDS'].add(self.ID)
            return

        while Loan.__ID_MNGR['NEXT-ID'] in Loan.__ID_MNGR['EXISTING-IDS']:  # find new unique id for Loan
            Loan.__ID_MNGR['NEXT-ID'] += 1
        self.ID = Loan.__ID_MNGR['NEXT-ID']
        Loan.__ID_MNGR['NEXT-ID'] += 1

    def is_late(self):
        return datetime.strptime(self.returndate, "%d/%m/%Y") < datetime.now()

    def get_dict(self):
        """
        returns a dict of the loan
        :return: dict
        """
        loan_dict = {
            "id": self.ID,
            "custID": self.custID,
            "bookID": self.bookID,
            "loan_date": self.loandate,
            "return_date": self.returndate
        }
        return loan_dict

    @staticmethod
    def fields():
        return ['id', 'custID', 'bookID', 'loan_date', 'return_date']

    def __str__(self):
        return f"{self.ID}: {self.bookID} -> {self.custID} on {self.loandate} until {self.returndate}"


class LoanException(Exception):
    pass


class LoanIdClashException(LoanException):
    def __str__(self):
        return "Loan ID already exists"


class LoanDateException(LoanException):
    pass


class InvalidLoanDateException(LoanDateException):
    def __str__(self):
        return "Date format does not match DD/MM/YYYY"


class DateOrderException(LoanDateException):
    def __str__(self):
        return "Return date cannot be before loan date"
