import re
from Genre import Genre

isbn_regex = r'\d{13}'
date_regex = r'^\d{2}-\d{2}-\d{4}'
name_regex = r"^[A-Z][a-zA-Z'-]+ [A-Z][a-zA-Z'-]+$"
book_title_regex = r"^[A-Za-z0-9\s\-_,\.;:()]+$"

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class Book(Genre):
    def __init__(self, genre_name, fict_or_nonfict, description, title, author, isbn, publication_date):
        super().__init__(genre_name, fict_or_nonfict, description)
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__publication_date = publication_date
        self.__availability_status = True

    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author
    
    def get_isbn(self):
        return self.__isbn
    
    def get_publication_date(self):
        return self.__publication_date
    
    def get_availability_status(self):
        return self.__availability_status
    
    def set_title(self, new_title):
        if re.match(book_title_regex, new_title):
            self.__title = new_title
        else:
            raise SetterException("Invalid book title when using setter")
        
    def set_author(self, new_author):
        if re.match(name_regex, new_author):
            self.__author = new_author
        else:
            raise SetterException("Invalid author name format when using setter")
        
    def set_isbn(self, new_isbn):
        if re.match(isbn_regex, new_isbn):
            self.__isbn = new_isbn
        else:
            raise SetterException("Invalid ISBN format when using setter")
    
    def set_publication_date(self, new_pub_date):
        if re.match(date_regex, new_pub_date):
            self.__publication_date = new_pub_date
        else:
            raise SetterException("Invalid date format when using setter")
    
    def set_availability_status(self, new_status):
        if isinstance(new_status, bool) == True:
            self.__availability_status = new_status
        else:
            raise SetterException("Please use boolean when adjusting availability status")
    
        

    def borrow_book(self):
        if self.get_availability_status() == True:
            self.set_availability_status(False)
            print(f"{self.get_title()} by {self.get_author()} has succesfully been borrowed")
            return True
        else:
            print(f"All copies of {self.get_title()} by {self.get_author()} have already been borrowed and are currently unavailable for rental")
            return False
        
    def return_book(self):
        if self.get_availability_status() == False:
            self.set_availability_status(True)
            print(f"{self.get_title()} by {self.get_author()} has been returned and is now availavle to be borrowed")
            return True
        else:
            print(f"{self.get_title()} was already available and had not been borrowed, thus it can't be returned.")
            return False
        
    def display_details(self):
        print(f"Title: {self.get_title()}\nAuthor: {self.get_author()}\nISBN: {self.get_isbn()}\nPublication Date: {self.get_publication_date()}\nAvailable to Borrow: {self.get_availability_status()}\nGenre: {self.get_genre_name()}\nGenre Type: {self.get_fict_or_nonfict()}\nGenre Description: {self.get_description()}")
