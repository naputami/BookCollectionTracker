import os
import pandas as pd

DEFAULT_IMAGE = "https://d827xgdhgqbnd.cloudfront.net/wp-content/uploads/2016/04/09121712/book-cover-placeholder.png"
CSV_FILE = "books.csv"

class Book:
    def __init__(self, book_id, title, author, genre, status="Unread", rating=3, comment="", cover_url=""):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status
        self.rating = rating
        self.comment = comment
        self.cover_url = cover_url if cover_url else DEFAULT_IMAGE

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "status": self.status,
            "rating": self.rating,
            "comment": self.comment,
            "cover_url": self.cover_url
        }


class BookManager:
    def __init__(self, csv_file=CSV_FILE):
        self.csv_file = csv_file
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.csv_file):
            df = pd.read_csv(self.csv_file)
            books = [Book(**row) for _, row in df.iterrows()]
        else:
            books = []
        return books

    def save_books(self):
        df = pd.DataFrame([book.to_dict() for book in self.books])
        df.to_csv(self.csv_file, index=False)

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def delete_book(self, book_id):
        self.books = [book for book in self.books if book.book_id != book_id]
        self.save_books()
    
    def update_book(self, updated_book: Book):
        for i, book in enumerate(self.books):
            if book.book_id == updated_book.book_id:
                self.books[i] = updated_book
                self.save_books()

    def get_books(self):
        return self.books
