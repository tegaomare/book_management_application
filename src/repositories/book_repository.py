import json
from typing import List, Optional, Dict
from src.domain.book import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol
import os


class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str = "books.json"):
        self.filepath = filepath

    def _read_file(self) -> List[Dict]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
        except (json.JSONDecodeError, IOError):
            return []

    def _write_file(self, data: List[Dict]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_all_books(self) -> List[Book]:
        data = self._read_file()
        return [Book.from_dict(item) for item in data]

    def add_book(self, book: Book) -> str:
        data = self._read_file()
        data.append(book.to_dict())
        self._write_file(data)
        return book.book_id

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        for item in self._read_file():
            if item.get("book_id") == book_id:
                return Book.from_dict(item)
        return None

    def update_book(self, book_id: str, data: Dict) -> Optional[Book]:
        items = self._read_file()
        for idx, item in enumerate(items):
            if item.get("book_id") == book_id:
                # update allowed fields
                item.update(data)
                items[idx] = item
                self._write_file(items)
                return Book.from_dict(item)
        return None

    def delete_book(self, book_id: str) -> bool:
        items = self._read_file()
        new_items = [it for it in items if it.get("book_id") != book_id]
        if len(new_items) == len(items):
            return False
        self._write_file(new_items)
        return True

    def find_book_by_name(self, query: str) -> List[Book]:
        if not isinstance(query, str):
            return []
        q = query.lower()
        return [b for b in self.get_all_books() if b.title and q in b.title.lower()]

    def append_checkout_history(self, book_id: str, entry: Dict) -> None:
        items = self._read_file()
        for idx, item in enumerate(items):
            if item.get("book_id") == book_id:
                history = item.get("checkout_history") or []
                history.append(entry)
                item["checkout_history"] = history
                items[idx] = item
                self._write_file(items)
                return
