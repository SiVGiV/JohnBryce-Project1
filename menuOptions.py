# Python built-in packages
import datetime as dt
from datetime import datetime

# Project packages
import loans
from menu import ConsoleMenu
from books import Book, BookType
from customers import Customer, CustomerException
from loans import Loan
import ItemList


def new_customer(customer_list, *_, **__):
    # Take input
    user_inp = ConsoleMenu.user_input({
        'name': "Customer's name: ",
        'city': "Customer's city of residence: ",
        'birth_year': {
            'prompt': "Customer's year of birth (4 digits): ",
            'tip': "year number (4 digits)",
            'test': lambda x: x.isdecimal() and len(x) == 4
        }
    })
    # Make customer object
    try:
        new_c = Customer(
            user_inp['name'],
            user_inp['city'],
            int(user_inp['birth_year'])
        )
    except CustomerException as e:
        print(e)
    else:
        # Print new customer
        print(new_c)
        # Add customer to list
        customer_list += new_c


def new_book(book_list, *_, **__):
    # Take input
    user_inp = ConsoleMenu.user_input({
        'name': "Book's title: ",
        'author': "Book's author(s): ",
        'year': {
            'prompt': "Book's year of publishing (4 digits): ",
            'tip': 'year number (4 digits)',
            'test': lambda x: x.isdecimal() and len(x) == 4
        },
        'total_quantity': {
            'prompt': "Amount of this book owned by the library: ",
            'tip': "Whole number",
            'test': lambda x: x.isdecimal()
        },
        'type': {
            'prompt': f"Book's loan duration ({BookType.options()}): ",
            'tip': f'book loan duration identifier ({BookType.options()})',
            'test': lambda x: x.isdecimal() and len(x) == 1 and int(x) in [item.value for item in BookType]
        }
    })
    # Create new object
    new_b = Book(
        user_inp['name'],
        user_inp['author'],
        int(user_inp['year']),
        int(user_inp['total_quantity']),
        BookType(int(user_inp['type']))
    )
    # Print new object
    print(new_b)
    # Add new object to list
    book_list += new_b


def new_loan(loan_list, customer_list, book_list, *_, **__):
    # Take input
    customer_inp = input("Loaning customer's name: ")
    chosen_customer_id = id_from_name(customer_inp, customer_list)
    book_input = input("Book loaned: ")
    # Find book by name
    chosen_book_id = id_from_name(book_input, book_list)
    chosen_book = book_list.get_by_property("id", chosen_book_id)[0]
    # Test if reached book limit
    if len(loan_list.get_by_property('bookID', chosen_book_id)) >= chosen_book.total_quantity:
        print("Book not in stock. Cannot create loan.")
        return
    loan_day = datetime.now()
    # Calculate return day
    ret_day = loan_day + dt.timedelta(days=chosen_book.book_type.days())
    # Create new loan
    new_l = Loan(
        chosen_customer_id,
        chosen_book_id,
        loan_day.strftime("%d/%m/%Y"),
        ret_day.strftime("%d/%m/%Y")
    )
    # Print new loan
    print(new_l)
    # Add loan to list
    loan_list += new_l


def rem_book(book_list, loan_list, *_, **__):
    # Take input
    user_inp = ConsoleMenu.user_input({
        'bookID': {
            'prompt': "ID of the book you want removed: ",
            'test': lambda x: x.isdecimal()
        }
    })
    # Remove book
    for_removal = book_list.get_by_property('id', int(user_inp['bookID']))
    if not for_removal:
        print("A book with that ID does not exist.")
        return
    else:
        for_removal = for_removal[0]
    # Look for related loans
    related_loans = loan_list.get_by_property('bookID', for_removal.ID)
    if related_loans:
        print("This book has existing loans, cannot delete.")
        return
    else:
        book_list.remove(for_removal)


def rem_customer(customer_list, loan_list, *_, **__):
    # Ask for input
    user_inp = ConsoleMenu.user_input({
        'custID': {
            'prompt': "ID of the customer you want removed: ",
            'test': lambda x: x.isdecimal()
        }
    })
    # Remove customer
    for_removal = customer_list.get_by_property('id', int(user_inp['custID']))
    if not for_removal:
        print("A customer with that ID does not exist.")
        return
    else:
        for_removal = for_removal[0]
    # Look for related loans
    related_loans = loan_list.get_by_property('custID', for_removal.ID)
    if related_loans:
        print("Customer has existing loans, cannot delete.")
        return
    else:
        customer_list.remove(for_removal)


def rem_loan(loan_list, customer_list, book_list, *_, **__):
    customer_query = input("Please enter the customer name: ")
    customer_id = id_from_name(customer_query, customer_list)
    book_query = input("Please enter the book name: ")
    book_id = id_from_name(book_query, book_list)
    for_removal = None
    customer_loans = loan_list.get_by_property('custID', customer_id)
    for loan in customer_loans:
        if loan.bookID == book_id:
            for_removal = loan
            break
    # Remove loan
    try:
        if for_removal is None:
            raise ItemList.ItemDoesNotExistError
        removed = loan_list.remove(for_removal)
    except ItemList.ItemDoesNotExistError:
        print('Loan not found.')
    else:
        print(str(removed), " was removed")


def show_books(book_list, *_, **__):
    for book in book_list:
        print(book)


def show_customers(customer_list, *_, **__):
    for customer in customer_list:
        print(customer)


def show_loans(loan_list, book_list, customer_list, *_, **__):
    for loan in loan_list:
        loan_book = book_list.get_by_property('id', loan.bookID)  # Find loaned book
        loan_customer = customer_list.get_by_property('id', loan.custID)  # Find loaning customer

        # If neither found
        if len(loan_book) == 0 and len(loan_customer) == 0:
            print(loan, " - couldn't find book or customer. Consider deleting this loan.")
            continue

        # If only book found
        if len(loan_book) == 0:
            print(loan, " - couldn't find book. Consider deleting this loan.")
            continue

        # If only customer found
        if len(loan_customer) == 0:
            print(loan, " - couldn't find customer. Consider deleting this loan.")
            continue

        # Print full loan with book and customer details
        print(f"{loan.ID}: <{loan_book[0]}> loaned to <{loan_customer[0]}> on"
              f" {loan.loandate} until {loan.returndate}")


def show_late(loan_list, *_, **__):
    # Print all late loans
    late_gen = (loan for loan in loan_list if loan.is_late())
    for loan in late_gen:
        print(loan)


def book_by_name(book_list, *_, **__):
    # Ask for input
    user_inp = ConsoleMenu.user_input({
        'name': "Book's name: "
    })
    # Get all books that match the query
    search_results = book_list.get_by_property('name', user_inp['name'])
    if not search_results:
        print('No books found.')
        return
    for res in search_results:
        print(res)


def customer_by_name(customer_list, *_, **__):
    # Ask for input
    user_inp = ConsoleMenu.user_input({
        'name': "Customer's name: "
    })
    # Get all customers that match the query
    search_results = customer_list.get_by_property('name', user_inp['name'])
    if not search_results:
        print('No customers found.')
        return
    for res in search_results:
        print(res)


def id_from_name(name, item_list):
    if item_list.get_list_type() is Loan:
        raise TypeError("item_list can only be Book or Customer.")
    search = item_list.get_by_property('name', name)
    query_type = 'customer' if item_list.get_list_type() is Customer else 'book'
    if not search:
        print("Customer not found. Aborting.")
        return
    if len(search) > 1:
        id_list = []
        for item in search:
            print(item)
            id_list.append(item.ID)
        item_id = ConsoleMenu.user_input({
            "id": {
                'prompt': f'Please enter your choice of {query_type}: ',
                'tip': 'ID number of the list above',
                'test': lambda x: x.isdecimal() and int(x) in id_list
            }
        })['id']
        return int(item_id)
    else:
        return search[0].ID
