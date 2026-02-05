from src.services.book_generator_service import generate_books
from src.domain.book import Book
from src.services.book_service import BookService
from src.services.book_analytics_service import BookAnalyticsService
from src.repositories.book_repository import BookRepository
import requests


class BookREPL:
    def __init__(self, book_svc, book_analytics_svc):
        self.running = True
        self.book_svc = book_svc
        self.book_analytics_svc = book_analytics_svc

    def start(self):
        print("Welcome to the book app! Type 'Help' for a list of commands!")
        while self.running:
            cmd = input(">>>").strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == "exit":
            self.running = False
            print("Goodbye!")
        elif cmd == "getAllRecords":
            self.get_all_records()
        elif cmd == "addBook":
            self.add_book()
        elif cmd == "findByName":
            self.find_book_by_name()
        elif cmd == "getJoke":
            self.get_joke()
        elif cmd == "getAveragePrice":
            self.get_average_price()
        elif cmd == "getTopBooks":
            self.get_top_books()
        elif cmd == "getValueScores":
            self.get_value_scores()
        elif cmd == "checkOut":
            self.check_out()
        elif cmd == "checkIn":
            self.check_in()
        elif cmd == "updateBook":
            self.update_book()
        elif cmd == "deleteBook":
            self.delete_book()
        elif cmd == "getHistory":
            self.get_history()
        elif cmd == "help":
            print(
                "Available commands: addBook, getAllRecords, findByName, getJoke, getAveragePrice, getTopBooks, getValueScores, checkOut, checkIn, updateBook, deleteBook, getHistory, help, exit"
            )
        else:
            print("Please use a valid command!")

    def get_average_price(self):
        books = self.book_svc.get_all_books()
        avg_price = self.book_analytics_svc.average_price(books)
        print(avg_price)

    def get_top_books(self):
        books = self.book_svc.get_all_books()
        top_rated_books = self.book_analytics_svc.top_rated(books)
        print(top_rated_books)

    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        value_scores = self.book_analytics_svc.value_scores(books)
        print(value_scores)

    def get_joke(self):
        try:
            url = "https://api.chucknorris.io/jokes/random"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json()["value"])
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Something else went wrong: {e}")

    def find_book_by_name(self):
        query = input("Please enter book name: ")
        books = self.book_svc.find_book_by_name(query)
        print(books)

    def check_out(self):
        book_id = input("Book ID to check out: ")
        email = input("Your email: ")
        due_date = input("Due date (optional ISO): ")
        try:
            updated = self.book_svc.check_out(
                book_id, user_email=email or None, due_date=due_date or None
            )
            print("Checked out:", updated)
        except Exception as e:
            print(f"Error: {e}")

    def check_in(self):
        book_id = input("Book ID to check in: ")
        email = input("Your email (optional): ")
        try:
            updated = self.book_svc.check_in(book_id, user_email=email or None)
            print("Checked in:", updated)
        except Exception as e:
            print(f"Error: {e}")

    def update_book(self):
        book_id = input("Book ID to update: ")
        field = input("Field to update (e.g., title): ")
        value = input("New value: ")
        try:
            updated = self.book_svc.update_book(book_id, {field: value})
            print("Updated:", updated)
        except Exception as e:
            print(f"Error: {e}")

    def delete_book(self):
        book_id = input("Book ID to delete: ")
        try:
            ok = self.book_svc.delete_book(book_id)
            print("Deleted" if ok else "Not found")
        except Exception as e:
            print(f"Error: {e}")

    def get_history(self):
        book_id = input("Book ID for history: ")
        book = self.book_svc.get_book_by_id(book_id)
        if not book:
            print("Book not found")
        else:
            print(book.checkout_history)

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        print(books)

    def add_book(self):
        try:
            print("Enter Book Details:")
            title = input("Title: ")
            author = input("Author: ")
            book = Book(title=title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")


if __name__ == "__main__":
    generate_books()
    repo = BookRepository("books.json")
    book_service = BookService(repo)
    book_analytics_service = BookAnalyticsService()
    repl = BookREPL(book_service, book_analytics_service)
    repl.start()
