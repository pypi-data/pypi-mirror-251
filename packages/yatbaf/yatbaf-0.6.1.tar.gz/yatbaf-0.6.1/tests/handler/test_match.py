from yatbaf.enums import UpdateType
from yatbaf.filters import Command
from yatbaf.filters import User
from yatbaf.handler import Handler


def test_match_empty_true(handler_func, message):
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
    )
    assert handler._match(message)


def test_is_fallback(handler_func):
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
        filters=[Command("foo")],
    )
    assert not handler._is_fallback()


def test_empty_is_fallback(handler_func):
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
    )
    assert handler._is_fallback()


def test_match_true(handler_func, message):
    message.text = "/foo"
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
        filters=[Command("foo")],
    )
    assert handler._match(message)


def test_match_true1(handler_func, message):
    message.text = "/foo"
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
        filters=[
            Command("foo"),
            User(message.from_.id),
        ]
    )
    assert handler._match(message)


def test_match_false(handler_func, message):
    message.text = "/bar"
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
        filters=[Command("foo")],
    )
    assert not handler._match(message)


def test_match_false1(handler_func, message):
    message.text = "/foo"
    handler = Handler(
        handler_func,
        update_type=UpdateType.MESSAGE,
        filters=[
            Command("bar"),
            User(1),
        ],
    )
    assert not handler._match(message)
