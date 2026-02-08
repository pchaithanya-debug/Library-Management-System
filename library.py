import sqlite3
from datetime import datetime, timedelta
from database import create_connection
from models import Book, Member
def add_book(book):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
    conn.commit()
    conn.close()
    print(f"Book '{book.title}' added successfully.")
def add_member(member):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (name) VALUES (?)", (member.name,))
    conn.commit()
    conn.close()
    print(f"Member '{member.name}' added successfully.")
def list_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    print("\nBooks in Library:")
    print("ID | Title | Author | Available")
    for b in books:
        available = "Yes" if b[3] == 1 else "No"
        print(f"{b[0]} | {b[1]} | {b[2]} | {available}")
def issue_book(book_id, member_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT available FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("Book not found.")
        return
    if book[0] == 0:
        print("Book is already issued.")
        return
    issue_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (?, ?, ?)",
                   (book_id, member_id, issue_date))
    cursor.execute("UPDATE books SET available=0 WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()
    print(f"Book ID {book_id} issued to Member ID {member_id}.")
def return_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT transaction_id FROM transactions
    WHERE book_id=? AND return_date IS NULL
    """, (book_id,))
    transaction = cursor.fetchone()
    if not transaction:
        print("Book is not issued.")
        return
    return_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE transactions SET return_date=? WHERE transaction_id=?", (return_date, transaction[0]))
    cursor.execute("UPDATE books SET available=1 WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()
    print(f"Book ID {book_id} returned successfully.")
def search_books(keyword):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    books = cursor.fetchall()
    conn.close()
    print("\nSearch Results:")
    print("ID | Title | Author | Available")
    for b in books:
        available = "Yes" if b[3] == 1 else "No"
        print(f"{b[0]} | {b[1]} | {b[2]} | {available}")
def list_overdue():
    conn = create_connection()
    cursor = conn.cursor()
    overdue_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    cursor.execute("""
    SELECT t.transaction_id, b.title, m.name, t.issue_date
    FROM transactions t
    JOIN books b ON t.book_id = b.book_id
    JOIN members m ON t.member_id = m.member_id
    WHERE t.return_date IS NULL AND t.issue_date <= ?
    """, (overdue_date,))
    overdue = cursor.fetchall()
    conn.close()
    print("\nOverdue Books:")
    print("TransactionID | Book Title | Member Name | Issue Date")
    for o in overdue:
        print(f"{o[0]} | {o[1]} | {o[2]} | {o[3]}")
