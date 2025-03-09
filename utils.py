import os
from book import Book
import pandas as pd

CSV_FILE = "books.csv"

def load_books():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        books = [Book(**row) for _, row in df.iterrows()]
    else:
        books = []
    return books

def save_books(books):
    df = pd.DataFrame([book.to_dict() for book in books])
    df.to_csv(CSV_FILE, index=False)