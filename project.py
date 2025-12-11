import mysql.connector
from datetime import date, timedelta

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Har_Har_Mahadev",
    database="library_management"
)
cursor = db.cursor()

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    query = "INSERT INTO books (title, author) VALUES (%s, %s)"
    values = (title, author)
    cursor.execute(query, values)
    db.commit()
    print("Book added successfully!")

def display_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        print("\nList of Books:")
        for book in books:
            print("ID: " + str(book[0]) + ", Title: " + book[1] + ", Author: " + book[2] + ", Status: " + book[3])
    else:
        print("No books found.")

def search_book():
    keyword = input("Enter book title or author to search: ")
    query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
    values = ("%" + keyword + "%", "%" + keyword + "%")
    cursor.execute(query, values)
    books = cursor.fetchall()
    if books:
        print("\nSearch Results:")
        for book in books:
            print("ID: " + str(book[0]) + ", Title: " + book[1] + ", Author: " + book[2] + ", Status: " + book[3])
    else:
        print("No matching books found.")

def update_book():
    display_books()
    book_id = int(input("Enter the ID of the book to update: "))
    title = input("Enter new title: ")
    author = input("Enter new author: ")
    query = "UPDATE books SET title=%s, author=%s WHERE book_id=%s"
    values = (title, author, book_id)
    cursor.execute(query, values)
    db.commit()
    print("Book details updated successfully!")

def delete_book():
    display_books()
    book_id = int(input("Enter the ID of the book to delete: "))
    cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    db.commit()
    print("Book deleted successfully!")

def issue_book():
    display_books()
    book_id = int(input("Enter book ID to issue: "))
    member_name = input("Enter member name: ")
    contact = input("Enter member contact: ")

    cursor.execute("INSERT INTO members (name, contact) VALUES (%s, %s)", (member_name, contact))
    member_id = cursor.lastrowid

    query = "INSERT INTO issued_books (book_id, member_id, issue_date) VALUES (%s, %s, %s)"
    values = (book_id, member_id, date.today())
    cursor.execute(query, values)

    cursor.execute("UPDATE books SET status='Issued' WHERE book_id=%s", (book_id,))
    db.commit()
    print("Book issued successfully!")

def view_issued_books():
    query = """SELECT issued_books.issue_id, books.title, members.name, issued_books.issue_date
               FROM issued_books
               JOIN books ON issued_books.book_id = books.book_id
               JOIN members ON issued_books.member_id = members.member_id
               WHERE issued_books.return_date IS NULL"""
    cursor.execute(query)
    issued_books = cursor.fetchall()
    if issued_books:
        print("\nIssued Books:")
        for issue in issued_books:
            print("Issue ID: " + str(issue[0]) + ", Book: " + issue[1] + ", Issued to: " + issue[2] + ", Issue Date: " + str(issue[3]))
    else:
        print("No books currently issued.")

def return_book():
    view_issued_books()
    issue_id = int(input("Enter the Issue ID of the book to return: "))
    return_date = date.today()
    fine = calculate_fine(issue_id)

    cursor.execute("UPDATE issued_books SET return_date=%s WHERE issue_id=%s", (return_date, issue_id))
    cursor.execute("UPDATE books SET status='Available' WHERE book_id=(SELECT book_id FROM issued_books WHERE issue_id=%s)", (issue_id,))
    db.commit()

    print("Book returned successfully! Fine: Rs. " + str(fine))

def calculate_fine(issue_id):
    query = "SELECT issue_date FROM issued_books WHERE issue_id=%s"
    cursor.execute(query, (issue_id,))
    issue_date = cursor.fetchone()[0]
    today = date.today()
    days_late = (today - issue_date).days - 14
    return max(0, days_late * 5)

def display_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    if members:
        print("\nList of Members:")
        for member in members:
            print("ID: " + str(member[0]) + ", Name: " + member[1] + ", Contact: " + member[2])
    else:
        print("No members found.")

def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Issue Book")
        print("7. View Issued Books")
        print("8. Return Book")
        print("9. Display Members")
        print("10. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            display_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            update_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            issue_book()
        elif choice == '7':
            view_issued_books()
        elif choice == '8':
            return_book()
        elif choice == '9':
            display_members()
        elif choice == '10':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

main()
