import re
genre_regex = r"^[A-Za-z '\-]+$"
fiction_regex = r'fiction|non-fiction|Fiction|Non-Fiction'

class SetterException(Exception):
    '''Exception raised when setter fails to meet regex requirements'''
    pass

class Genre:
    def __init__(self, genre_name, fict_or_nonfict, description):
        self.__genre_name = genre_name
        self.__fict_or_nonfict = fict_or_nonfict
        self.__description = description
        self.__books_in_genre = []
    
    def get_genre_name(self):
        return self.__genre_name
    
    def get_fict_or_nonfict(self):
        return self.__fict_or_nonfict
    
    def get_description(self):
        return self.__description
    
    def get_books_in_genre(self):
        return self.__books_in_genre
    
    def set_genre_name(self, new_genre):
        if re.match(genre_regex, new_genre):
            self.__genre_name = new_genre
        else:
            raise SetterException("Invalid genre name, please use primarily letters, hyphens, apostrophes and spaces")
        
    def set_fict_or_nonfict(self, new_type):
        if re.match(fiction_regex, new_type):
            self.__fict_or_nonfict = new_type
        else:
            raise SetterException("Please enter only Fiction or Non-Fiction")
        
    def set_desctiption(self, edit_description):
        self.__description = edit_description
    
    def add_books_in_genre(self, new_book):
        self.get_books_in_genre().append(new_book)

    def display_genre_details(self):
        print(f"Genre Name: {self.get_genre_name()}\nGenre Type: {self.get_fict_or_nonfict()}\nDescripton: {self.get_description()}")
        print("Books from this Genre:")
        if not self.get_books_in_genre():
            print("No books have been added with this genre yet")
        else:
            for book in self.get_books_in_genre():
                print(book)