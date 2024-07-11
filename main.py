import re
from Book import Book
from User import User
from Author import Author

class InputNamingException(Exception):
    '''Exception raised when user inputs fail to meet regex requirements'''
    pass

input_regex = r'^\d{1}$'
isbn_regex = r'\d{13}'
date_regex = r'^\d{2}-\d{2}-\d{4}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"

library_dictionary = {}
user_dictionary = {}
author_list = []

def book_operations_menu():
    global input_regex
    global date_regex
    global name_regex
    global isbn_regex
    global library_dictionary
    global user_dictionary
    global author_list
    while True:
        book_title_message = "\nBooks Operations:"
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
                isbn = input("Enter 13 digit ISBN number (remove hyphens): ")
                if not re.match(isbn_regex, isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                publication_date = input("Enter publication date (MM-DD-YYYY): ")
                if not re.match(date_regex, publication_date):
                    raise InputNamingException("Please enter date in format of MM-DD-YYYY")
                if isbn not in library_dictionary.keys():
                    library_dictionary[isbn] = Book(book_title, author_name, isbn, publication_date)
                    print(f"{book_title} by {author_name} with ISBN number {isbn} has been added to Library Management System database")
                    author_name_list = [author.get_author_name() for author in author_list]
                    if author_name not in author_name_list:
                        author_home_country = input("Please enter their country of birth: ")
                        author_new_dob = input("Now please enter their date of birth in MM-DD-YYYY format: ")
                        if not re.match(date_regex, author_new_dob):
                            raise InputNamingException("Please enter date in format of MM-DD-YYYY")
                        else:
                            new_author = Author(author_name, author_home_country, author_new_dob)
                            author_list.append(new_author)
                            new_author.add_authored_book(library_dictionary[isbn])
                    elif author_name in author_name_list:
                        for author in author_list:
                            if author.get_author_name() == author_name:
                                author.add_authored_book(library_dictionary[isbn])                       
                else:
                    print(f"{book_title} by {author_name} with ISBN number {isbn} has already been added to our system")
            elif book_menu_input == "2":
                rental_isbn = input("Enter ISBN of book you wish to rent: ")
                if not re.match(isbn_regex, rental_isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                if rental_isbn in library_dictionary.keys():
                    if library_dictionary[rental_isbn].get_availability_status() == True:
                        library_dictionary[rental_isbn].borrow_book()
                        renter_id = input("Enter (or create) your Library ID number here: ")
                        if renter_id in user_dictionary.keys():
                            user_dictionary[renter_id].add_to_currently_borrowed_list(library_dictionary[rental_isbn])
                        else:
                            renter_name = input("We are setting up your new account, please enter your name here: ")
                            user_dictionary[renter_id] = User(renter_name, renter_id)
                            user_dictionary[renter_id].add_to_currently_borrowed_list(library_dictionary[rental_isbn])
                    else:
                        print("Book is unavailable for rental")
                else:
                    print("Please ensure book with this ISBN number has been added to library before attempting to borrow it")
            elif book_menu_input == "3":
                return_isbn = input("Enter ISBN for book you wish to return to library: ")
                if not re.match(isbn_regex, return_isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                if return_isbn in library_dictionary.keys():
                    if library_dictionary[return_isbn].get_availability_status() == False:
                        return_id = input("Please enter your Library ID number here: ")
                        library_dictionary[return_isbn].return_book()
                        if return_id in user_dictionary.keys():
                            user_dictionary[return_id].add_to_returned_list(library_dictionary[return_isbn])
                        else:
                            print("Please ensure user has been registered to our system already.")
                    else:
                        print("Book is not currently borrowed")
                else:
                    print("Please ensure book with this ISBN number has been added to library before attempting to return it")
            elif book_menu_input == "4":
                search_criteria = input("Please enter criteria you wish to search by (title or ISBN): ").lower()
                if search_criteria == "title":
                    search_title = input("Enter title of book you are searching for: ")
                    if re.match(book_title_regex, search_title):
                        for book in library_dictionary.values():
                            if book.get_title() == search_title:
                                print("\n")
                                book.display_details()
                    else:
                        raise InputNamingException("Pleae ensure a valid book title has been entered")
                elif search_criteria == "isbn":
                    search_isbn = input("Enter ISBN number (remove hyphens): ")
                    if re.match(isbn_regex, search_isbn):
                        for isbn_key in library_dictionary.keys():
                            if search_isbn == isbn_key:
                                print("\n")
                                library_dictionary[isbn_key].display_details()                         
                    else:
                        raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
            elif book_menu_input == "5":
                for index, book in enumerate(library_dictionary.values(), 1):
                    print(f"\n{index}."), book.display_details()
            elif book_menu_input == "6":
                break
            else:
                print("Invalid input, please enter a digit 1 to 6\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")
    
def user_operations_menu():
    global input_regex
    global name_regex
    global user_dictionary
    global library_dictionary
    while True:
        user_title_message = "\nUser Operations"
        print(user_title_message)
        user_menu_input = input("1. Add a new user\n2. View user details\n3. Display all users\n4. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, user_menu_input):
            if user_menu_input == "1":
                new_user_name = input("Please enter your name: ")
                new_user_id = input("Please enter your new Library ID: ")
                if re.match(name_regex,new_user_name):
                    user_dictionary[new_user_id] = User(new_user_name, new_user_id)
                else:
                    raise InputNamingException("Please enter your name in valid first and last name format.")
            elif user_menu_input == "2":
                user_search_criteria = input("Please enter if you wish to search by 'Name' or 'Library ID': ").lower()
                if user_search_criteria == 'name':
                    search_user_name = input("Please enter your name here: ")
                    if re.match(name_regex, search_user_name):
                        for user in user_dictionary.values():
                            if user.get_name() == search_user_name:
                                print("\n")
                                user.display_user_details()
                    else:
                        raise InputNamingException("Please enter your name in valid first and last name format.")
                elif user_search_criteria == 'library id' or user_search_criteria == 'id':
                    search_library_id = input("Please enter your Library ID here: ")
                    for library_id_key in user_dictionary.keys():
                        if search_library_id == library_id_key:
                            print("\n")
                            user_dictionary[library_id_key].display_user_details()
                else:
                    print("Invalid input please respond with 'Name' or 'Library ID'")
            elif user_menu_input == "3":
                for index, user in enumerate(user_dictionary.values(), 1):
                    print(f"\n{index}:"), user.display_user_details()
            elif user_menu_input == "4":
                break
            else:
                print("Invalid input, please enter a digit 1 to 4\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")

def author_operations_menu():
    global input_regex
    global name_regex
    global date_regex
    global book_title_regex
    global author_list
    global library_dictionary
    while True:
        author_title_message = "\nAuthor Operations"
        print(author_title_message)
        author_menu_input = input("1. Add a new author\n2. View author bioraphy\n3. Display all author biographies\n4. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, author_menu_input):
            if author_menu_input == "1":
                new_author_name = input("Please enter the name of the author you wish to add to the system: ")
                if not re.match(name_regex, new_author_name):
                    raise InputNamingException("Invalid input, please enter valid first and last name format")
                new_country_of_birth = input("Please enter the country of birth for this author: ")
                new_author_dob = input("Please enter the date of brth for this author in MM-DD-YYYY format: ")
                if not re.match(date_regex, new_author_dob):
                    raise InputNamingException("Invalid input. Enter DOB in valid format of MM-DD-YYYY")
                adding_author = Author(new_author_name, new_country_of_birth, new_author_dob)
                author_list.append(adding_author)
            elif author_menu_input == "2":
                search_author_name = input("Please enter the name of the author you wish to view a biography of: ")
                if not re.match(name_regex, search_author_name):
                    raise InputNamingException("Invalid input, please enter valid first and last name format")
                for author in author_list:
                    if author.get_author_name() == search_author_name:
                        print("\n")
                        author.display_biography()
            elif author_menu_input == "3":
                for index, author in enumerate(author_list, 1):
                    print(f"\n{index}:"), author.display_biography()
            elif author_menu_input == "4":
                break
            else:
                print("Invalid input, please enter a digit 1 to 4\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")

def genre_operations_menu():
    global input_regex
    while True:
        genre_title_message = "\nGenre Operations"
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
        menu_input = input("\nMain Menu:\n1. Book Operations\n2. User Operations\n3. Author Operations\n4. Genre Operations\n5. Quit\nEnter choice here: ")
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