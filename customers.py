import datetime
from dataclasses import dataclass


@dataclass
class Customer:
    """
    A class representing a customer
    """
    __ID_MNGR = {"NEXT-ID": 0, "EXISTING-IDS": set()}
    name: str
    city: str
    birth_year: int
    ID: int = -1

    def __post_init__(self):
        now = datetime.date.today()
        if self.birth_year > now.year:
            raise BirthYearException

        if self.ID in Customer.__ID_MNGR['EXISTING-IDS']:  # check if the customer id exists already
            raise CustomerIdClashException

        if self.ID != -1:  # check if id was passed as a parameter
            Customer.__ID_MNGR['EXISTING-IDS'].add(self.ID)
            return

        while Customer.__ID_MNGR['NEXT-ID'] in Customer.__ID_MNGR['EXISTING-IDS']:  # find new unique id for customer
            Customer.__ID_MNGR['NEXT-ID'] += 1
        self.ID = Customer.__ID_MNGR['NEXT-ID']
        Customer.__ID_MNGR['NEXT-ID'] += 1

    def get_dict(self):
        loan_dict = {
            "id": self.ID,
            "name": self.name,
            "city": self.city,
            "birth_year": self.birth_year
        }
        return loan_dict

    @staticmethod
    def fields():
        return ['id', 'name', 'city', 'birth_year']

    def __str__(self):
        return f"{self.ID}: {self.name}"


class CustomerException(Exception):
    pass


class CustomerIdClashException(CustomerException):
    def __str__(self):
        return "Customer ID already exists."


class BirthYearException(CustomerException):
    def __str__(self):
        return "Customer birth year is invalid."
