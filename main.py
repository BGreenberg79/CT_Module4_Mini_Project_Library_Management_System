import re
from Book import Book
from User import User
from Author import Author
from Genre import Genre

''' Here we import each module for each of the 4 classes our main program will feature: Book, User, Author, and Genre. We also import the regular expression module.'''

class InputNamingException(Exception):
    '''Exception raised when user inputs fail to meet regex requirements'''
    pass

''' Here I define a class for a custom InputNamingException that will catch incorrect inputs via regex throughout the system.'''

input_regex = r'^\d{1}$'
isbn_regex = r'\d{13}'
date_regex = r'^\d{2}-\d{2}-\d{4}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"
genre_regex = r"^[A-Za-z '\-]+$"
fiction_regex = r'fiction|non-fiction|Fiction|Non-Fiction'

library_dictionary = {}
user_dictionary = {}
author_list = []
genre_list = []

''' 
Here I globally define regular expressions for menu input, ISBN numbers, publishing an birthdates, author and user names, book title, genres, and fiction vs. non-fiction'.
I also initialize our library and uer dictionaries and author and genre lists. Library dictionary uses ISBN as a unqique key identifier, while Users will use thie rlibrary ID as keys for their unique identifier.
'''

def book_operations_menu():
    global input_regex
    global date_regex
    global name_regex
    global isbn_regex
    global book_title_regex
    global genre_regex
    global fiction_regex
    global library_dictionary
    global user_dictionary
    global author_list
    global genre_list
    while True:
        book_title_message = "\nBooks Operations:"
        print(book_title_message)
        book_menu_input = input("1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books\n6. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, book_menu_input):
            if book_menu_input == "1":
                book_title = input("Enter title of book you are adding to library: ")
                if not re.match(book_title_regex, book_title):
                    raise InputNamingException("Please ensure a valid book title has been entered")
                author_name = input("Enter author of book: ").title()
                if not re.match(name_regex, author_name):
                    raise InputNamingException("Enter first and last name with capitalization")
                isbn = input("Enter 13 digit ISBN number (remove hyphens): ")
                if not re.match(isbn_regex, isbn):
                    raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                publication_date = input("Enter publication date (MM-DD-YYYY): ")
                if not re.match(date_regex, publication_date):
                    raise InputNamingException("Please enter date in format of MM-DD-YYYY")
                genre_name = input("What is this book's genre: ").title()
                if not re.match(genre_regex, genre_name):
                    raise InputNamingException("Please enter a valid genre naming format composed primarily of letters, spaces, hyphens, and apostrophes")
                genre_name_list = [genre.get_genre_name() for genre in genre_list]
                if genre_name in genre_name_list:
                    for genre in genre_list:
                        if genre.get_genre_name() == genre_name:
                            genre_type = genre.get_fict_or_nonfict()
                            genre_descript = genre.get_description()
                            if book_title not in genre_list[genre_list.index(genre)].get_books_in_genre():
                                genre_list[genre_list.index(genre)].add_books_in_genre(book_title)
                                print(f"{book_title} was added to {genre_list[genre_list.index(genre)].get_genre_name()} book list")
                if genre_name not in genre_name_list:
                    genre_type = input("Please enter if this genre is best categorized as Fiction or Non-Fiction: ").title()
                    if not re.match(fiction_regex, genre_type):
                        raise InputNamingException("Please enter Fiction or Non-Fiction")
                    genre_descript = input("Please enter a brief description of this genre: ")
                    new_genre = Genre(genre_name, genre_type, genre_descript)
                    if new_genre not in genre_list:
                        genre_list.append(new_genre)
                        if book_title not in new_genre.get_books_in_genre():
                            new_genre.add_books_in_genre(book_title)
                            print(f"{book_title} was added to {new_genre.get_genre_name()} book list")
                if isbn not in library_dictionary.keys():
                    library_dictionary[isbn] = Book(genre_name, genre_type, genre_descript, book_title, author_name, isbn, publication_date)
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
                try:
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
                                if re.match(name_regex, renter_name):
                                    user_dictionary[renter_id] = User(renter_name, renter_id)
                                    user_dictionary[renter_id].add_to_currently_borrowed_list(library_dictionary[rental_isbn])
                        else:
                            print("Book is unavailable for rental")
                    else:
                        print("Please ensure book with this ISBN number has been added to library before attempting to borrow it")
                except KeyError:
                    print("Please ensure book with this ISBN number has been added to the library.")
            elif book_menu_input == "3":
                try:
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
                except KeyError:
                    print("Please ensure book with this ISBN number had been added to the library.")
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
                    try:
                        search_isbn = input("Enter ISBN number (remove hyphens): ")
                        if re.match(isbn_regex, search_isbn):
                            for isbn_key in library_dictionary.keys():
                                if search_isbn == isbn_key:
                                    print("\n")
                                    library_dictionary[isbn_key].display_details()                         
                        else:
                            raise InputNamingException("Please enter exactly 13 digits without hyphens for ISBN")
                    except KeyError:
                        print("Please ensure book with this ISBN number has been added.")
            elif book_menu_input == "5":
                for index, book in enumerate(library_dictionary.values(), 1):
                    print(f"\n{index}."), book.display_details()
            elif book_menu_input == "6":
                break
            else:
                print("Invalid input, please enter a digit 1 to 6\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")
    

'''
The book_operations function is the most complicated function in the program and it needs to reference global variables for all of its regular expression handling as well as for its use of the library dictionary,
user dictionary, author list, and genre list. It's starts by asking users if they wish to add, rent, return, search for a book, or print all books.
If the user decides to add a book they will be prompted for the book's title, the author's name, the isbn number, the publication date, and the genre name all checke dby regular expressions.
Once the genre name is input the logic beins by checking if this genre's name is already in the global genre list through a list comphrehension using the genre name getter method. 
if this genre name is already in the genre name list w ebuilt through the comprehension, we then loop through the genre list, match the users input to its existing genre and use getters to assign genre type and description to inherit our previous entry.
At that point we check if this book title has already been added to the list of books in this genre at the index location of the genre list for the genre object that matched our users' input.
Once we have ensured that this title has not been added we use our Genre classes' .add_books_in_genre() method to append it to that genre objects list of book titles. This is the one instance in the entire program I decided to use our users' string input
instead of appending an object to a list inside another class because Genre is a parent class for Book and I experienced some trouble trying to append a child class object to a list that is part of its parents class attributes. When using the similar, if not more simplistic logic for
my Author class that was not part of a parent-child relationship with Book I experienced no issues.
If the genre the user is inputting for this Book object has not been previous added the user is prompted for inputs for a type (fiction vs. non-fiction) that is alo authenticated by regex and and is prompted for a brief description. The genre's name, type, and description is then used to create an object for the Genre class
and this object instance is appended to our global genre list and the book title is appended to this instance's list of books for that genre.
Once all of the logic for the Genre class is handled we check if this isbn number is in our global library dictionary's list of keys and if it is not we assign a Book object instance with user inputs for genre name, genre type, genre description, title, author name, isbn, and publishing date as the value for the key of that isbn number.
I then do a list comprehension using the .get_author_name() method to get a list of author names from the author list. If the author's name is not in that list comprehension we get inputs for author's home country and Date of birth (verified by regex) and instantiate a new Author object for
the new author we are adding to our author list. We then append that author to the global author list and add the book at this ISBN key location to the list of books written by that author using the .add_authored_book() method
If the author's name is aleady in the author_name_list list comprehension we loop through the list of objects in author_list and the object with a matching getter for name to the user input has the book object located at that ISBN key location added to that Author's book list by using the add_authored_book() method on that author object.
In choice 2 we first ask the user of the ISBN number they wish to rent out, verifying that number via regex, and after checking that the ISBN number is in our dictionary's list of keys and 
checking that at this key location the .get_availability_status() method produces a True result, we run .borrow_book() method on the book object at that ISBN location.
We then prompt the user for their Library ID and if it is in the user_distcionary.keys() list we use the .add_to_currently_borrowed_books() method to update their user record.
If that Library ID does not show up in the list of keys we take another input for the user's name and set up their new account by instantiating a User object with that Library ID number and the name they just entered into the input.
We then run the .add_to_currently_borrowed_books() method for the new user's object with the book object at that ISBN key location.
In choice 3 we similarly start by asking for the ISBN number of the book they wish to return and checking if that ISBN number is in the library_dictionary.keys() list as well as not currently available to borrow.
If so,  we ask the user for their library ID number and if that number is in the user_dicionary we  run the .return_book() method and the .add_to_returned_list method to appropriately update the book's availability status, as well as the users current borrowed book list and list of returned books.
Choice 4 takes a search criteria to check if the user wishes to display the details for a book searching by title or by ISBN. If they choose title we use the library_dictionary.values() list and the get_title() method to match the title of the book object to the user's input and 
and then run the .display_details() method on the book object that has that exact match. Similarly for searching by isbn we match the isbn they search for to the library_dictionary.keys() list and at that key location we run the .display_details() method to display the details of the book object at that key location
I also built a KeyError exception in at this point in case the user searches for a book that hasn't been added to the library_dictionary. At choice 5 I use the enumerate function to number each object in the library_dictionary.values() list
and then run the .display_details() method on each of those objects. At choice 6 we have the option to return to the main menu by breaking this menu's while loop.

'''

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
                    try:
                        search_library_id = input("Please enter your Library ID here: ")
                        for library_id_key in user_dictionary.keys():
                            if search_library_id == library_id_key:
                                print("\n")
                                user_dictionary[library_id_key].display_user_details()
                    except KeyError:
                        print("Please ensure user with this Library ID has been added prior to search")
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
    global author_list
    global library_dictionary
    while True:
        author_title_message = "\nAuthor Operations"
        print(author_title_message)
        author_menu_input = input("1. Add a new author\n2. View author bioraphy\n3. Display all author biographies\n4. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, author_menu_input):
            if author_menu_input == "1":
                new_author_name = input("Please enter the name of the author you wish to add to the system: ").title()
                if not re.match(name_regex, new_author_name):
                    raise InputNamingException("Invalid input, please enter valid first and last name format")
                new_country_of_birth = input("Please enter the country of birth for this author: ")
                new_author_dob = input("Please enter the date of brth for this author in MM-DD-YYYY format: ")
                if not re.match(date_regex, new_author_dob):
                    raise InputNamingException("Invalid input. Enter DOB in valid format of MM-DD-YYYY")
                adding_author = Author(new_author_name, new_country_of_birth, new_author_dob)
                if adding_author not in author_list:
                    author_list.append(adding_author)
                    print(f"{new_author_name} has been added to the author list.")
                elif adding_author in author_list:
                    print(f"{new_author_name} is already in the author list and a duplicate entry has not been added.")
            elif author_menu_input == "2":
                search_author_name = input("Please enter the name of the author you wish to view a biography of: ")
                if not re.match(name_regex, search_author_name):
                    raise InputNamingException("Invalid input, please enter valid first and last name format")
                try:
                    for author in author_list:
                        if author.get_author_name() == search_author_name:
                            print("\n")
                            author.display_biography()
                except IndexError:
                    print("Please ensure author with this name has already been added to the author list before attempting to view details.")
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
    global genre_list
    global genre_regex
    global fiction_regex
    global library_dictionary
    while True:
        genre_title_message = "\nGenre Operations"
        print(genre_title_message)
        genre_menu_input = input("1. Add a new genre\n2. Edit description of a genre\n3. View genre details\n4. Display all genres\n5. Return to main menu\nEnter choice here: ")
        if re.match(input_regex, genre_menu_input):
            if genre_menu_input == "1":
                new_genre_name = input("Please enter the name of the genre you wish to add: ").title()
                if not re.match(genre_regex, new_genre_name):
                    raise InputNamingException("Invalid input, please enter a valid genre name composed of letters, spaces, hyphens, and apostrophes")
                genre_name_list = [genre.get_genre_name() for genre in genre_list]
                if new_genre_name not in genre_name_list:
                    genre_fict_nonfict = input("Is this genre best classified as Fiction or Non-Fiction: ").title()
                    if not re.match(fiction_regex, genre_fict_nonfict):
                        raise InputNamingException("Invalid input please enter only Fiction or Non-Fiction")
                    describe_genre = input("Please enter a brief description of this genre: ")
                    adding_genre = Genre(new_genre_name, genre_fict_nonfict, describe_genre)
                    genre_list.append(adding_genre)
                    print(f"{new_genre_name} has been added to the genre list.")
                elif new_genre_name in genre_name_list:
                    print("This genre has already been added to our genre list. Please choose options 2 or 3 to read more about it.")
            elif genre_menu_input == "2":
                genre_input_descript = input("For which genre do you wish to update its description: ").title()
                if not re.match(genre_regex, genre_input_descript):
                    raise InputNamingException("Please enter a valid input for genre composed of letters, spaces, hyphens, and apostrophes")
                try:
                    for genre in genre_list:
                        if genre_input_descript == genre.get_genre_name():
                            new_description = input("Please enter your updated description here: ")
                            genre.set_description(new_description)
                            print(f"The genre, {genre.get_genre_name()} has been updated to have the following description: {new_description}")
                        else:
                            print("Please ensure the genre you wish to update has been already added to the list")
                except IndexError:
                    print("Please ensure this genre has been added to the genre list before attempting to edit its description")
            elif genre_menu_input == "3":
                search_genre_name = input("For which genre do you wish to see its details: ").title()
                if not re.match(genre_regex, search_genre_name):
                    raise InputNamingException("Please enter a valid input for genre composed of lettrs, spaces, hyphens, and apostrophes")
                try:
                    for genre in genre_list:
                        if search_genre_name == genre.get_genre_name():
                            print("\n")
                            genre.display_genre_details()
                except IndexError:
                    print("Please ensure genre you are searching for has already been added to the genre list")
            elif genre_menu_input == "4":
                for index, genre in enumerate(genre_list, 1):
                    print(f"\n{index}:"), genre.display_genre_details()
            elif genre_menu_input == "5":
                break
            else:
                print("Invalid input, please enter a digit 1 to 5\n")
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
                genre_operations_menu()
            elif menu_input == "5":
                break
            else:
                print("Invalid input, please enter a digit 1 to 5\n")
        else:
            raise InputNamingException("Invalid input, please enter an individual digit\n")


main_menu()