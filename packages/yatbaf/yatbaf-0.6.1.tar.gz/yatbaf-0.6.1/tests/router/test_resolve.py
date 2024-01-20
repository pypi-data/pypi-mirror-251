import unittest.mock as mock

import pytest

from yatbaf.filters import Command
from yatbaf.handler import Handler
from yatbaf.middleware import Middleware
from yatbaf.router import OnMessage


@pytest.mark.asyncio
async def test_resolve_no_handlers(router, update_info):
    router._on_registration()
    assert not await router._resolve(update_info)


@pytest.mark.asyncio
async def test_resolve_catch_all(router, update_info, handler_func):
    router.add_handler(handler_func)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_resolve_none(router, update_info, handler_func):
    filter = Command("foo")
    router.add_handler(handler_func, filters=[filter])
    router._on_registration()
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_nested_vert(update_info, handler_func):

    def find_router(router):
        r = router
        while r._routers:
            r = r._routers[-1]
        return r

    router = OnMessage()
    for _ in range(5):
        find_router(router).add_router(OnMessage())

    filter = Command("foo")
    update_info.content.text = "/foo"
    find_router(router).add_handler(handler_func, filters=[filter])
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_resolve_nested_horiz(update_info, handler_func):
    router = OnMessage(
        routers=[
            OnMessage(
                handlers=[
                    Handler(
                        mock.AsyncMock(),
                        filters=[Command(f"bar{i}")],
                        update_type="message",
                    ),
                ]
            ) for i in range(5)
        ],
    )
    router.add_router(
        OnMessage(
            handlers=[
                Handler(
                    handler_func,
                    filters=[Command("foo")],
                    update_type="message",
                ),
            ]
        )
    )
    router._on_registration()
    update_info.content.text = "/foo"
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_guard_false(handler_func, router, update_info, asyncdef):
    router.add_guard(asyncdef(False))
    router.add_handler(handler_func)
    router._on_registration()
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.mark.asyncio
async def test_guard_true(handler_func, router, update_info, asyncdef):
    router.add_guard(asyncdef(True))
    router.add_handler(handler_func)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_parent_guard_true(handler_func, update_info, asyncdef):
    router = OnMessage()
    router.add_guard(asyncdef(True))
    router.add_handler(handler_func)

    router1 = OnMessage()
    router1.add_handler(asyncdef())

    router.add_router(router1)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_parent_guard_false(handler_func, update_info, asyncdef):
    router = OnMessage()
    router.add_guard(asyncdef(False))
    router.add_handler(asyncdef())

    router1 = OnMessage()
    router1.add_handler(handler_func)

    router.add_router(router1)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_guard_false_both(handler_func, update_info, asyncdef):
    router = OnMessage()
    router.add_guard(asyncdef(False))
    router.add_handler(asyncdef())

    router1 = OnMessage()
    router1.add_guard(asyncdef(False))
    router1.add_handler(handler_func)

    router.add_router(router1)
    router._on_registration()
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.mark.asyncio
async def test_guard_skip_nested(handler_func, update_info, asyncdef):
    router = OnMessage(skip_with_nested=True)
    router.add_guard(asyncdef(False))

    router1 = OnMessage()
    router1.add_guard(asyncdef(True))
    router1.add_handler(handler_func)

    router.add_router(router1)
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


# yapf: disable
def middleware_factory(mark):
    def middleware(handler):
        async def wrapper(update):
            mark()
            await handler(update)
        return wrapper
    return middleware
# yapf: enable


@pytest.mark.asyncio
async def test_resolve_wrap_router_middlewares(
    router, update_info, handler_func
):
    m = mock.Mock()
    router.add_handler(handler_func)
    for _ in range(5):
        router.add_middleware(
            Middleware(
                middleware_factory(m),
                is_handler=True,
            )
        )
    assert len(router._middleware) == 5

    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once_with(update_info.content)
    assert m.call_count == 5


@pytest.mark.asyncio
async def test_resolve_wrap_handler_middlewares(
    router, handler_func, update_info
):
    m = mock.Mock()
    router.add_handler(
        handler_func,
        middleware=[middleware_factory(m) for _ in range(5)],
    )
    router._on_registration()
    assert await router._resolve(update_info)
    assert m.call_count == 5
    handler_func.assert_awaited_once_with(update_info.content)


@pytest.mark.asyncio
async def test_resolve_wrap_middlewares(router, update_info, handler_func):
    m = mock.Mock()
    router.add_handler(
        handler_func,
        middleware=[middleware_factory(m) for _ in range(5)],
    )
    for _ in range(5):
        router.add_middleware(
            Middleware(
                middleware_factory(m),
                is_handler=True,
            )
        )
    router._on_registration()
    assert await router._resolve(update_info)
    assert m.call_count == 10
    handler_func.assert_awaited_once_with(update_info.content)
