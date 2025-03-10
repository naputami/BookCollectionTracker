import uuid
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lib import Book, BookManager

LIST_GENRE = ["Fantasy", "Romance", "Classic", "Mistery", "Scifi", "Self Help", "Religion & Spirituality", "Thriller & Suspense", "Parenting & Family", "Science & Technology", "Social Science", "Other"]

manager = BookManager()

if 'editing' not in st.session_state:
    st.session_state.editing = None

st.title("📚 Book Collection Tracker")

page = st.sidebar.selectbox("Menu", ["Add Book", "Book List", "Statistics"], 1)


if page == "Add Book":
    st.subheader("➕ Add New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", LIST_GENRE)
    status = st.selectbox("Status", ["Unread", "Reading", "Read"])
    rating = st.slider("Rating (1-5)", 1, 5, 3)
    comment = st.text_area("Comment (Optional)")
    cover_url = st.text_input("Cover Image URL (Optional)")



    if st.button("Add Book"):
        if all([title, author, genre, status]):
            new_id = uuid.uuid4()
            new_book = Book(new_id, title, author, genre, status, rating, comment, cover_url)
            manager.add_book(new_book)
            st.success("Book successfully added")
        else:
            st.error("Please fill in all required fields.")

elif page == "Book List":

    st.subheader("📖 Your Book Collection")

    if manager.books:
        for book in manager.books:
            col1, col2 = st.columns([1, 3])

            col1.image(book.cover_url, width=100)


            col2.write(f"**{book.title}** by {book.author}")
            col2.write(f"📖 Genre: {book.genre} | ⭐ Rating: {book.rating} | 🏷️ Status: {book.status}")
            col2.write(f"💬 {'No comment' if pd.isna(book.comment) else book.comment}")

            cols = col2.columns(4)
            
            if cols[0].button("✏️ Edit", key=f"edit_{book.book_id}"):
                st.session_state.editing = book.book_id
                st.rerun()
            
            if cols[1].button("🗑️ Delete", key=f"delete_{book.book_id}"):
                manager.delete_book(book.book_id)
                st.rerun()
                
            if st.session_state.editing == book.book_id:
                with st.container():
                    new_title = st.text_input("Update Title", book.title, key=f"title_{book.book_id}")
                    new_author = st.text_input("Update Author", book.author, key=f"author_{book.book_id}")
                    new_genre = st.selectbox(
                        "Update Genre",
                        LIST_GENRE,
                        index=LIST_GENRE.index(book.genre),
                        key=f"genre_{book.book_id}"
                        )
                    new_status = st.selectbox(
                        "Update Status", 
                        ["Unread", "Reading", "Read"], 
                        index=["Unread", "Reading", "Read"].index(book.status),
                        key=f"status_{book.book_id}"
                    )
                    new_rating = st.slider(
                        "Update Rating (1-5)", 
                        1, 5, 
                        book.rating if book.rating else 3,
                        key=f"rating_{book.book_id}"
                    )
                    new_comment = st.text_area(
                        "Update Comment", 
                        'No comment' if pd.isna(book.comment) else book.comment,
                        key=f"comment_{book.book_id}"
                    )
                    new_cover = st.text_input("Update Cover", book.cover_url, key=f"cover_{book.book_id}")

                    col1, col2 = st.columns(2)
                    
                    if col1.button("💾 Save Changes", key=f"save_{book.book_id}"):
                        if all([new_title, new_status, new_author, new_comment, new_cover, new_genre, new_rating]):
                            book.title = new_title
                            book.author = new_author
                            book.genre = new_genre
                            book.status = new_status
                            book.rating = new_rating
                            book.comment = new_comment
                            book.cover_url = new_cover
                            manager.update_book(book)
         
                            st.session_state.editing = None
                            st.success("Book updated successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields.")
                    
                    if col2.button("❌ Cancel", key=f"cancel_{book.book_id}"):
                        st.session_state.editing = None
                        st.rerun()
                
            st.divider() 
    else:
        st.info("No books found. Try adding some!")

elif page == "Statistics":
    st.subheader("📊 Statistics")
    df = pd.DataFrame([book.to_dict() for book in manager.books])

    if not df.empty:
        st.write("#### Your books' genre")
        genre_counts = df['genre'].value_counts()
        genre_fig, ax = plt.subplots()
        ax.pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(genre_fig)

        st.write("### Your books' status")
        status_counts = df['status'].value_counts()

        status_fig, ax = plt.subplots()
        ax.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(status_fig)


    else:
        st.info("No data available for visualization.")

  

  

