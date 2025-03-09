DEFAULT_IMAGE = "https://d827xgdhgqbnd.cloudfront.net/wp-content/uploads/2016/04/09121712/book-cover-placeholder.png"
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