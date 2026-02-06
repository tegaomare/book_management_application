import pytest

from src.domain.book import Book
import src.services.book_service as book_service
from tests.mocks.mock_book_repository import MockBookRepo


@pytest.fixture()
def repo():
    return MockBookRepo()


@pytest.fixture()
def svc(repo):
    return book_service.BookService(repo)


def test_add_get_update_delete_flow(svc):
    new = Book(title="New Book", author="New Author")
    new_id = svc.add_book(new)
    assert isinstance(new_id, str)

    fetched = svc.get_book_by_id(new_id)
    assert fetched is not None
    assert fetched.title == "New Book"

    updated = svc.update_book(new_id, {"title": "Updated Title"})
    assert updated is not None
    assert updated.title == "Updated Title"

    deleted = svc.delete_book(new_id)
    assert deleted is True
    assert svc.get_book_by_id(new_id) is None


def test_check_out_and_in_persists_changes(repo, svc):
    existing = repo.get_all_books()[0]
    book_id = existing.book_id

    checked = svc.check_out(book_id, user_email="user@example.com", due_date="2026-12-31")
    assert checked is not None
    assert checked.available is False
    assert checked.checked_out_by == "user@example.com"

    checked_in = svc.check_in(book_id, user_email="user@example.com")
    assert checked_in is not None
    assert checked_in.available is True
