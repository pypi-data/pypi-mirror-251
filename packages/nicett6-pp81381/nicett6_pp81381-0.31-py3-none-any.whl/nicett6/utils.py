""" Misc utilities. """

import argparse
import asyncio
import logging
import platform
import re
from collections.abc import Awaitable, Callable
from typing import Coroutine, Sequence, Set, Tuple

_LOGGER = logging.getLogger(__name__)

MIN_ASPECT_RATIO = 0.3
MAX_ASPECT_RATIO = 3.5
PCT_ABS_TOL = 0.0000001


def get_system_serial_port(system: str) -> str:
    """Work out the most likely serial port given the type of system. YMMV."""
    if system == "Windows":
        return "COM3"
    elif system == "Linux":
        return "/dev/ttyUSB0"
    else:
        raise ValueError("Invalid system - unable to determine serial_port")


def get_platform_serial_port() -> str:
    """Work out the most likely serial port given the platform"""
    return get_system_serial_port(platform.system())


async def async_get_platform_serial_port() -> str:
    """Work out the most likely serial port given the platform without blocking"""
    loop = asyncio.get_running_loop()
    system = await loop.run_in_executor(None, platform.system)
    return get_system_serial_port(system)


def hex_arg_to_int(arg: str, fixed_len: bool = True) -> int:
    """Parse and convert a 2 char hex string"""
    if fixed_len:
        pat = re.compile("[a-fA-F0-9]{2,2}$")
    else:
        pat = re.compile("[a-fA-F0-9]{1,2}$")
    m = pat.match(arg)
    if m is None:
        raise ValueError(f"Invalid hex string: {arg!r}")
    return int(m.group(0), 16)


def pct_arg_to_int(arg: str) -> int:
    """Parse a numeric string that represents a percentage in units of 0.1%.  1000 == 100%"""
    pat = re.compile("[0-9]{4,4}$")
    m = pat.match(arg)
    if m is None:
        raise ValueError(f"Invalid percent string: {arg!r}")
    pct = int(m.group(0))
    if pct < 0 or pct > 1000:
        raise ValueError(f"Invalid percent string: {arg!r}")
    return pct


class AsyncObserver:
    async def update(self, observable: "AsyncObservable") -> None:
        pass


class AsyncObservable:
    def __init__(self) -> None:
        self.observers: Set[AsyncObserver] = set()

    def attach(self, observer: AsyncObserver) -> None:
        self.observers.add(observer)

    def detach(self, observer: AsyncObserver) -> None:
        self.observers.remove(observer)

    async def notify_observers(self) -> None:
        for o in self.observers:
            await o.update(self)


def check_pos(name: str, pos: int) -> int:
    if pos < 0 or pos > 1000:
        raise ValueError(f"{name} position ({pos}) out of range")
    return pos


def check_aspect_ratio(aspect_ratio: float) -> None:
    if aspect_ratio < MIN_ASPECT_RATIO or aspect_ratio > MAX_ASPECT_RATIO:
        raise ValueError(f"Aspect ratio ({aspect_ratio}) is not sensible")


async def run_coro_after_delay(coro: Awaitable[None], delay: float = 2.0):
    _LOGGER.info("run_coro_after_delay started")
    await asyncio.sleep(delay)
    await coro
    _LOGGER.info("run_coro_after_delay completed")


def parse_example_args(
    examples: Sequence[Tuple[str, Callable[..., Coroutine[None, None, None]]]]
) -> Tuple[str, Callable[..., Coroutine[None, None, None]]]:
    default_example = examples[0][0]
    examples_dict = dict(examples)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--serial_port",
        type=str,
        default="socket://localhost:50200",
        help="serial port",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        choices=examples_dict,
        default=default_example,
        help="example name",
    )
    args = parser.parse_args()
    return args.serial_port, examples_dict[args.name]
