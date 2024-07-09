import re
from Book import Book

class InputNamingException(Exception):
    '''Exception raised when user inputs fail to meet regex requirements'''
    pass

input_regex = r'^\d{1}$'
isbn_regex = r'\d{13}'
date_regex = r'^\d{2}-\d{2}-\d{4}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"

def book_operations_menu():
    global input_regex
    global date_regex
    global name_regex
    global isbn_regex
    library_dictionary = {}
    while True:
        book_title_message = "Books Operations:"
        print(book_title_message)
        book_menu_input = input("1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books\n6. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, book_menu_input):
            if book_menu_input == "1":
                book_title = input("Enter title of book you are adding to library: ")
                if not re.match(book_title_regex, book_title):
                    raise InputNamingException("Please ensure a valid book title has been entered")
                author_name = input("Enter author of book: ")
                if not re.match(name_regex, author_name):
                    raise InputNamingException("Enter first and last name with capitalization")
                isbn = input("Enter ISBN number (remove hyphens): ")
                if not re.match(isbn_regex, isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                publication_date = input("Enter publication date (MM-DD-YYYY): ")
                if not re.match(date_regex, publication_date):
                    raise InputNamingException("Please enter date in format of MM-DD-YYYY")
                if isbn not in library_dictionary.keys():
                    library_dictionary[isbn] = Book(book_title, author_name, isbn, publication_date)
                    print(f"{book_title} by {author_name} with ISBN number {isbn} has been added to Library Management System database")
                else:
                    print(f"{book_title} by {author_name} with ISBN number {isbn} has already been added to our system")
            elif book_menu_input == "2":
                rental_isbn = input("Enter ISBN of book you wish to rent: ")
                if not re.match(isbn_regex, rental_isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                if rental_isbn in library_dictionary.keys():
                    library_dictionary[rental_isbn].borrow_book()
                else:
                    print("Please ensure book with this ISBN number has been added to library before attempting to borrow it")
            elif book_menu_input == "3":
                return_isbn = input("Enter ISBN for book you wish to return to library: ")
                if not re.match(isbn_regex, return_isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                if return_isbn in library_dictionary.keys():
                    library_dictionary[return_isbn].return_book()
            elif book_menu_input == "4":
                search_criteria = input("Please enter criteria you wish to search by (title or ISBN): ").lower()
                if search_criteria == "title":
                    search_title = input("Enter title of book you are searching for: ")
                    if re.match(book_title_regex, search_title):
                        for book in library_dictionary.values():
                            if book.get_title() == search_title:
                                print("\n")
                                book.display_details()
                                print("\n")
                    else:
                        raise InputNamingException("Pleae ensure a valid book title has been entered")
                elif search_criteria == "isbn":
                    search_isbn = input("Enter ISBN number (remove hyphens): ")
                    if re.match(isbn_regex, search_isbn):
                        for isbn_key in library_dictionary.keys():
                            if search_isbn == isbn_key:
                                print("\n")
                                library_dictionary[isbn_key].display_details() 
                                print("\n")                           
                    else:
                        raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
            elif book_menu_input == "5":
                for index, book in enumerate(library_dictionary.values(), 1):
                    print(f"\n{index}."), book.display_details()
                print('\n')
            elif book_menu_input == "6":
                break
            else:
                print("Invalid input, please enter a digit 1 to 6\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")
    
def user_operations_menu():
    global input_regex
    while True:
        user_title_message = "User Operations"
        print(user_title_message)
        user_menu_input = input("1. Add a new user\n2. View user details\n3. Display all users\n4. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, user_menu_input):
            if user_menu_input == "1":
                pass
            elif user_menu_input == "2":
                pass
            elif user_menu_input == "3":
                pass
            elif user_menu_input == "4":
                break
            else:
                print("Invalid input, please enter a digit 1 to 4\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")

def author_operations_menu():
    global input_regex
    while True:
        author_title_message = "Author Operations"
        print(author_title_message)
        author_menu_input = input("1. Add a new author\n2. View author details\n3. Display all authors\n4. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, author_menu_input):
            if author_menu_input == "1":
                pass
            elif author_menu_input == "2":
                pass
            elif author_menu_input == "3":
                pass
            elif author_menu_input == "4":
                break
            else:
                print("Invalid input, please enter a digit 1 to 4\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")

def genre_operations_menu():
    global input_regex
    while True:
        genre_title_message = "Genre Operations"
        print(genre_title_message)
        genre_menu_input = input("1. Add a new genre\n2. View genre details\n3. Display all genres\n4. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, genre_menu_input):
            if genre_menu_input == "1":
                pass
            elif genre_menu_input == "2":
                pass
            elif genre_menu_input == "3":
                pass
            elif genre_menu_input == "4":
                break
            else:
                print("Invalid input, please enter a digit 1 to 4\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")



def main_menu():
    global input_regex
    welcome_message = "Welcome To The Library Management System!\n"
    print(welcome_message)
    while True:
        menu_input = input("Main Menu:\n1. Book Operations\n2. User Operations\n3. Author Operations\n4. Genre Operations\n5. Quit\nEnter choice here: ")
        if re.match(input_regex, menu_input):
            if menu_input == "1":
                print("\n")
                book_operations_menu()
            elif menu_input == "2":
                print("\n")
                user_operations_menu()
            elif menu_input == "3":
                print("\n")
                author_operations_menu()
            elif menu_input == "4":
                print("\n")
                genre_operations_menu
            elif menu_input == "5":
                break
            else:
                print("Invalid input, please enter a digit 1 to 5\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")


main_menu()