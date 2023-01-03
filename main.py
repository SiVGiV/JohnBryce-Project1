# Menu imports
from menu import ConsoleMenu
import menuOptions
# Class imports
from ItemList import ItemList
from books import Book
from customers import Customer
from loans import Loan

if __name__ == "__main__":
    # Create lists
    bl = ItemList(Book, "./CSVs/books.csv")
    cl = ItemList(Customer, "./CSVs/customers.csv")
    ll = ItemList(Loan, "./CSVs/loans.csv")

    # Create menu
    menu_handler = ConsoleMenu(
        {
            'Add a new customer': menuOptions.new_customer,
            'Add a new book': menuOptions.new_book,
            'Loan a book': menuOptions.new_loan,
            'Return a book': menuOptions.rem_loan,
            'Display all books': menuOptions.show_books,
            'Display all customers': menuOptions.show_customers,
            'Display all loans': menuOptions.show_loans,
            'Display late loans': menuOptions.show_late,
            'Find book by name': menuOptions.book_by_name,
            'Find customer by name': menuOptions.customer_by_name,
            'Remove book': menuOptions.rem_book,
            'Remove customer': menuOptions.rem_customer
        }
    )

    # Run menu
    while True:
        menu_handler.display_main(customer_list=cl, book_list=bl, loan_list=ll)
