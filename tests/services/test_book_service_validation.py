import pytest

import src.services.book_service as book_service
from tests.mocks.mock_book_repository import MockBookRepo


@pytest.fixture()
def svc():
    return book_service.BookService(MockBookRepo())


def test_get_all_books_positive(svc):
    books = svc.get_all_books()
    assert len(books) >= 1


@pytest.mark.parametrize("bad_name", [None, 3, 3.14, [], {}, object()])
def test_find_book_name_negative(svc, bad_name):
    with pytest.raises(TypeError, match=r"Expected str, got"):
        svc.find_book_by_name(bad_name)
