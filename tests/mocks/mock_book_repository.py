from src.domain.book import Book


class MockBookRepo:
    def __init__(self):
        # start with a single book like previous mock
        self.items = [Book(title="test", author="author")]

    def get_all_books(self):
        return list(self.items)

    def add_book(self, book: Book):
        self.items.append(book)
        return book.book_id

    def find_book_by_name(self, query):
        q = query.lower() if isinstance(query, str) else None
        if q is None:
            return []
        return [b for b in self.items if b.title and q in b.title.lower()]

    def get_book_by_id(self, book_id: str):
        for b in self.items:
            if b.book_id == book_id:
                return b
        return None

    def update_book(self, book_id: str, data: dict):
        for idx, item in enumerate(self.items):
            if item.book_id == book_id:
                # apply dict updates
                updated = Book.from_dict({**item.to_dict(), **data})
                self.items[idx] = updated
                return updated
        return None

    def delete_book(self, book_id: str):
        before = len(self.items)
        self.items = [b for b in self.items if b.book_id != book_id]
        return len(self.items) < before
