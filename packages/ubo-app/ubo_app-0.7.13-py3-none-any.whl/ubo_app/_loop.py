# ruff: noqa: D100, D101, D102, D103, D104, D107, N999
from asyncio import Handle
from typing import Awaitable


def create_task(task: Awaitable) -> Handle:
    msg = f"Current thread is not an ubo service thread, can't run task {task}"
    raise NotImplementedError(msg)
