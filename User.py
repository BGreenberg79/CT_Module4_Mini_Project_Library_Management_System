import re

name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class User():
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
        self.__borrowed_and_returned_books = []
        self.__currently_borrowed_books = []

    def get_name(self):
        return self.__name
    
    def get_library_id(self):
        return self.__library_id
    
    def get_borrowed_and_returned_books(self):
        return self.__borrowed_and_returned_books
    
    def get_currently_borrowed_books(self):
        return self.__currently_borrowed_books
    
    def set_name(self, new_name):
        if re.match(name_regex, new_name):
            self.__name = new_name
        else:
            raise SetterException("Invalid name formatting entered")
    
    def set_library_id(self, new_id):
        self.__library_id = new_id

    def add_to_returned_list(self, book):
        self.get_borrowed_and_returned_books().append(book)
        self.get_currently_borrowed_books().remove(book)
    
    def add_to_currently_borrowed_list(self, book):
        self.get_currently_borrowed_books().append(book)

    def display_user_details(self):
        print(f"User Name: {self.get_name()}\nLibrary ID: {self.get_library_id()}")
        print("Returned Books:")
        if not self.get_borrowed_and_returned_books():
            print("No books have been returned yet by this user")
        else:
            for returned_book in self.get_borrowed_and_returned_books():
                print(f"{returned_book.get_title()}")
        print("Currently Borrowing:")
        if not self.get_currently_borrowed_books():
            print("No books currently borrowed by this user")
        else:
            for current_book in self.get_currently_borrowed_books():
                print(f"{current_book.get_title()}")
    