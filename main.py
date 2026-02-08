from database import setup_database
from library import add_book, add_member, list_books, issue_book, return_book, search_books, list_overdue
from models import Book, Member
def menu():
    setup_database()
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. Add Member")
        print("3. List All Books")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Search Books")
        print("7. List Overdue Books")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            add_book(Book(title, author))
        elif choice == "2":
            name = input("Enter member name: ")
            add_member(Member(name))
        elif choice == "3":
            list_books()
        elif choice == "4":
            book_id = int(input("Enter Book ID: "))
            member_id = int(input("Enter Member ID: "))
            issue_book(book_id, member_id)
        elif choice == "5":
            book_id = int(input("Enter Book ID: "))
            return_book(book_id)
        elif choice == "6":
            keyword = input("Enter book title or author to search: ")
            search_books(keyword)
        elif choice == "7":
            list_overdue()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
if __name__ == "__main__":
    menu()
