from typing import List, Optional, Dict
from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.domain.book import Book


class BookService:
    def __init__(self, repo: BookRepositoryProtocol):
        self.repo = repo

    def get_all_books(self) -> List[Book]:
        return self.repo.get_all_books()

    def add_book(self, book: Book) -> str:
        if not book.title or not book.author:
            raise ValueError("Book must have title and author")
        return self.repo.add_book(book)

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return self.repo.get_book_by_id(book_id)

    def update_book(self, book_id: str, data: Dict) -> Optional[Book]:
        return self.repo.update_book(book_id, data)

    def delete_book(self, book_id: str) -> bool:
        return self.repo.delete_book(book_id)

    def find_book_by_name(self, query: str) -> List[Book]:
        if not isinstance(query, str):
            raise TypeError("Expected str, got something else.")
        return self.repo.find_book_by_name(query)

    def check_out(
        self,
        book_id: str,
        user_email: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> Optional[Book]:
        book = self.repo.get_book_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        book.check_out(user_email=user_email, due_date=due_date)
        # persist changes
        updated = self.repo.update_book(book_id, book.to_dict())
        return updated

    def check_in(
        self, book_id: str, user_email: Optional[str] = None
    ) -> Optional[Book]:
        book = self.repo.get_book_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        book.check_in(user_email=user_email)
        updated = self.repo.update_book(book_id, book.to_dict())
        return updated
