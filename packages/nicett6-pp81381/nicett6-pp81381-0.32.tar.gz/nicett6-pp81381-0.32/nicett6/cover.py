import logging
from asyncio import CancelledError, Event, Lock, Task, create_task
from asyncio import sleep as asyncio_sleep
from asyncio import sleep as notifier_asyncio_sleep
from time import perf_counter
from typing import Iterable

from nicett6.utils import AsyncObservable, check_pos

_LOGGER = logging.getLogger(__name__)

POLLING_INTERVAL = 0.2


class Cover(AsyncObservable):
    """A sensor class that can be used to monitor the position of a cover"""

    MOVEMENT_THRESHOLD_INTERVAL: float = 2.7
    IS_FULLY_UP_POS: int = 950
    IS_FULLY_DOWN_POS: int = 5

    def __init__(self, name: str, max_drop: float) -> None:
        super().__init__()
        self.name = name
        self.max_drop = max_drop
        self._pos: int = 1000
        self._prev_movement = perf_counter() - self.MOVEMENT_THRESHOLD_INTERVAL
        self._prev_pos: int = self._pos
        self._notifier = PostMovementNotifier(self)
        self.idle_event = Event()
        self.idle_event.set()

    def __repr__(self):
        return (
            f"Cover: {self.name}, {self.max_drop}, "
            f"{self._pos}, {self._prev_pos}, "
            f"{self._prev_movement}"
        )

    def log(self, msg: str, loglevel: int = logging.DEBUG) -> None:
        _LOGGER.log(
            loglevel,
            f"{msg}; "
            f"name: {self.name}; "
            f"max_drop: {self.max_drop}; "
            f"pos: {self.pos}; "
            f"_prev_pos: {self._prev_pos}; "
            f"is_moving: {self.is_moving}; "
            f"is_going_down: {self.is_going_down}; "
            f"is_going_up: {self.is_going_up}; "
            f"is_fully_down: {self.is_fully_down}; "
            f"is_fully_up: {self.is_fully_up}; ",
        )

    @property
    def pos(self) -> int:
        """Native position: from 0 (fully down) to 1000 (fully up)"""
        return self._pos

    async def set_pos(self, value: int) -> None:
        """Position (0 fully down to 1000 fully up)"""
        prev_pos = self._pos  # Preserve state in case of exception
        self._pos = check_pos(f"{self.name} pos", value)
        self._prev_pos = prev_pos
        await self.moved()

    @property
    def drop(self) -> float:
        """Drop in length units from 0.0 when fully up to max_drop when fully down"""
        return (1000 - self._pos) * self.max_drop / 1000.0

    async def moved(self) -> None:
        """Called to indicate movement"""
        self._prev_movement = perf_counter()
        self.idle_event.clear()
        await self._notifier.moved()
        await self.notify_observers()

    async def set_idle(self) -> None:
        """Called to indicate that movement has finished"""
        self._prev_pos = self._pos
        self._prev_movement = perf_counter() - self.MOVEMENT_THRESHOLD_INTERVAL
        self.idle_event.set()
        await self.notify_observers()

    async def wait_idle(self) -> None:
        _LOGGER.debug(f"State of idle_event is {self.idle_event.is_set()}")
        await self.idle_event.wait()

    @property
    def is_moving(self) -> bool:
        """
        Returns True if the cover has moved recently

        When initiating movement, call self.moved() so that self.is_moving
        will be meaningful before the first POS message comes back from the cover
        """
        return perf_counter() - self._prev_movement < self.MOVEMENT_THRESHOLD_INTERVAL

    @property
    def is_fully_up(self) -> bool:
        """Returns True if the cover is fully up"""
        return not self.is_moving and self._pos > self.IS_FULLY_UP_POS

    @property
    def is_fully_down(self) -> bool:
        """Returns True if the cover is fully down"""
        return not self.is_moving and self._pos < self.IS_FULLY_DOWN_POS

    @property
    def is_going_up(self) -> bool:
        """
        Returns True if the cover is going up

        Will only be meaningful after _pos has been set by the first
        POS message coming back from the cover for a movement
        """
        return self.is_moving and self._pos > self._prev_pos

    @property
    def is_going_down(self) -> bool:
        """
        Returns True if the cover is going down

        Will only be meaningful after _pos has been set by the first
        POS message coming back from the cover for a movement
        """
        return self.is_moving and self._pos < self._prev_pos

    async def set_going_up(self) -> None:
        """Force the state to is_going_up"""
        self._prev_pos = self._pos - 1
        await self.moved()

    async def set_going_down(self) -> None:
        """Force the state to is_going_down"""
        self._prev_pos = self._pos + 1
        await self.moved()

    async def set_target_pos_hint(self, target_pos: int) -> None:
        """ "Force the state to is_going_up/down based on target_pos"""
        if target_pos < self._pos:
            await self.set_going_down()
        elif target_pos > self._pos:
            await self.set_going_up()

    async def stop_notifier(self) -> None:
        await self._notifier.cancel_task()


async def wait_for_motion_to_complete(covers: Iterable[Cover]) -> None:
    """
    Poll for motion to complete

    Make sure that Cover.moving() is called when movement
    is initiated for this method to work reliably
    (see TT6Cover.handle_response_message)
    Has the side effect of notifying observers of the idle state
    """
    while True:
        await asyncio_sleep(POLLING_INTERVAL)
        if all([not cover.is_moving for cover in covers]):
            return


class PostMovementNotifier:
    """
    Invokes set_idle (and hence notify_observers) one last time after movement stops

    The cover is considered idle if it hasn't moved for
    Cover.MOVEMENT_THRESHOLD_INTERVAL + PostMovementNotifier.POST_MOVEMENT_ALLOWANCE seconds
    """

    POST_MOVEMENT_ALLOWANCE = 0.05

    def __init__(self, cover: Cover) -> None:
        self.cover = cover
        self._task_lock: Lock = Lock()
        self._task: Task | None = None

    async def moved(self) -> None:
        """
        Manage a task that will call set_idle on the cover after a short delay

        Reset the task if movement happens again while a task is running
        """
        async with self._task_lock:
            await self._cancel_task()
            self._task = create_task(self._set_idle_after_delay())
            self.cover.log("PostMovementNotifier task started", logging.DEBUG)

    async def _set_idle_after_delay(self) -> None:
        await notifier_asyncio_sleep(
            Cover.MOVEMENT_THRESHOLD_INTERVAL + self.POST_MOVEMENT_ALLOWANCE
        )
        await self.cover.set_idle()
        self.cover.log("PostMovementNotifier set to idle", logging.DEBUG)

    async def cancel_task(self) -> None:
        async with self._task_lock:
            await self._cancel_task()

    async def _cancel_task(self) -> None:
        """Cancel task - make sure you have acquired the lock first"""
        if self._task is not None:
            if not self._task.done():
                self._task.cancel()
            try:
                await self._task
            except CancelledError:
                pass
