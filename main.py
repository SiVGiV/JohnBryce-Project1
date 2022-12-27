# Menu imports
from menu import ConsoleMenu
import menuOptions as options
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
            'Add a new customer': options.new_customer,
            'Add a new book': options.new_book,
            'Loan a book': options.new_loan,
            'Return a book': options.rem_loan,
            'Display all books': options.show_books,
            'Display all customers': options.show_customers,
            'Display all loans': options.show_loans,
            'Display late loans': options.show_late,
            'Find book by name': options.book_by_name,
            'Find customer by name': options.customer_by_name,
            'Remove book': options.rem_book,
            'Remove customer': options.rem_customer
        }
    )

    # Run menu
    while True:
        menu_handler.disp_main(customer_list=cl, book_list=bl, loan_list=ll)
