import argparse
import asyncio
import logging

from nicett6.cover import Cover, wait_for_motion_to_complete
from nicett6.cover_manager import CoverManager
from nicett6.ttbus_device import TTBusDeviceAddress

_LOGGER = logging.getLogger(__name__)


async def log_cover_state(cover):
    try:
        while cover.is_moving:
            _LOGGER.info(
                f"drop: {cover.drop}; "
                f"set_going_up: {cover.set_going_up}; "
                f"is_going_down: {cover.is_going_down}; "
            )
            await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        pass


async def example1(serial_port):
    tt_addr = TTBusDeviceAddress(0x02, 0x04)
    max_drop = 2.0
    async with CoverManager(serial_port) as mgr:
        tt6_cover = await mgr.add_cover(tt_addr, Cover("Cover", max_drop))

        message_tracker_task = asyncio.create_task(mgr.message_tracker())
        logger_task = asyncio.create_task(log_cover_state(tt6_cover.cover))

        await tt6_cover.send_pos_command(900)
        await wait_for_motion_to_complete([tt6_cover.cover])

        await tt6_cover.send_simple_command("MOVE_UP")
        await wait_for_motion_to_complete([tt6_cover.cover])

        logger_task.cancel()
        await logger_task

    await message_tracker_task


async def example2(serial_port):
    tt_addr = TTBusDeviceAddress(0x03, 0x04)
    # max_drop = 1.825
    max_drop = 0.62
    async with CoverManager(serial_port) as mgr:
        tt6_cover = await mgr.add_cover(tt_addr, Cover("Cover", max_drop))

        message_tracker_task = asyncio.create_task(mgr.message_tracker())
        logger_task = asyncio.create_task(log_cover_state(tt6_cover.cover))

        await asyncio.sleep(1.0)

        # await tt6_cover.send_pos_command(60)
        await tt6_cover.send_hex_move_command(254)
        await wait_for_motion_to_complete([tt6_cover.cover])

        logger_task.cancel()
        await logger_task

    await message_tracker_task


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--serial_port",
        type=str,
        default="socket://localhost:50200",
        help="serial port",
    )
    args = parser.parse_args()
    asyncio.run(example2(args.serial_port))
