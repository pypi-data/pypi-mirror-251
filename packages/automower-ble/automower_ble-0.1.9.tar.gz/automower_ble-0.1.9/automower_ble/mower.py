"""
    The top level script to connect and communicate with the mower
    This sends requests and decodes responses. This is an example of
    how the request and response classes can be used.
"""

# Copyright: Alistair Francis <alistair@alistair23.me>

import argparse
import asyncio
import logging

import binascii

from .request import *
from .response import MowerResponse

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

logger = logging.getLogger(__name__)

MTU_SIZE = 20

class Mower:
    def __init__(self, channel_id: int, address):
        self.channel_id = channel_id
        self.address = address

        self.request = MowerRequest(channel_id)
        self.response = MowerResponse(channel_id)

        self.queue = asyncio.Queue()

    async def connect(self, device):
        """
            Connect to a device and setup the channel
        """
        logger.info("starting scan...")

        if device is None:
            logger.error(
                "could not find device with address '%s'", self.address)
            return

        logger.info("connecting to device...")
        self.client = BleakClient(
            device,
            services=["98bd0001-0b0e-421a-84e5-ddbf75dc6de4"],
            use_cached=True
        )
        await self.client.connect()
        logger.info("connected")

        logger.info("pairing device...")
        await self.client.pair()
        logger.info("paired")

        self.client._backend._mtu_size = MTU_SIZE

        for service in self.client.services:
            logger.info("[Service] %s", service)

            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await self.client.read_gatt_char(char.uuid)
                        logger.debug(
                            "  [Characteristic] %s (%s), Value: %r",
                            char,
                            ",".join(char.properties),
                            value,
                        )
                    except Exception as e:
                        logger.error(
                            "  [Characteristic] %s (%s), Error: %s",
                            char,
                            ",".join(char.properties),
                            e,
                        )

                else:
                    logger.debug(
                        "  [Characteristic] %s (%s)", char, ",".join(char.properties)
                    )
                if char.uuid == "98bd0002-0b0e-421a-84e5-ddbf75dc6de4":
                    self.write_char = char

                if char.uuid == "98bd0003-0b0e-421a-84e5-ddbf75dc6de4":
                    self.read_char = char

        async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
            logger.info("Received: " + str(binascii.hexlify(data)))
            await self.queue.put(data)

        await self.client.start_notify(self.read_char, notification_handler)

        data = self.request.generate_request_setup_channel_id()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        logger.debug("chunk_size: " + str(chunk_size))
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()

        data = self.request.generate_request_handshake()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()

    async def get_model(self):
        """
            Get the mower model
        """
        data = self.request.generate_request_device_type()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

        return self.response.decode_response_device_type(data)

    async def is_charging(self):
        data = self.request.generate_request_is_charging()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

    async def battery_level(self):
        """
            Query the mower battery level
        """
        data = self.request.generate_request_battery_level()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

        return self.response.decode_response_battery_level(data)

    async def mower_state(self):
        data = self.request.generate_request_mower_state()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

        return self.response.decode_response_mower_state(data)

    async def mower_activity(self):
        data = self.request.generate_request_mower_activity()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

        return self.response.decode_response_mower_activity(data)

    async def mower_override(self):
        """
            Force the mower to run 3 hours
        """

        data = self.request.generate_request_mode_of_operation("manual")
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

        data = self.request.generate_request_override_duration("3hours")
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

    async def mower_pause(self):
        data = self.request.generate_request_pause()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

    async def mower_resume(self):
        data = self.request.generate_request_resume()
        logger.info("Writing: " + str(binascii.hexlify(data)))

        chunk_size = MTU_SIZE - 3
        for chunk in (
            data[i: i + chunk_size] for i in range(0, len(data), chunk_size)
        ):
            logger.info(chunk)
            await self.client.write_gatt_char(self.write_char, chunk, response=False)

        data = await self.queue.get()
        if data[len(data) - 1] != 0x03:
            data = data + await self.queue.get()

    async def disconnect(self):
        """
            Disconnect from the mower, this should be called after every
            `connect()` before the Python script exits
        """

        await self.client.stop_notify(self.read_char)
        await self.queue.put(None)

        logger.info("disconnecting...")
        await self.client.disconnect()
        logger.info("disconnected")


async def main(mower):
    device = await BleakScanner.find_device_by_address(
            mower.address
        )

    await mower.connect(device)

    model = await mower.get_model()
    print("Connected to: " + model)

    charging = await mower.is_charging()
    if charging:
        print("Mower is charging")
    else:
        print("Mower is not charging")

    battery_level = await mower.battery_level()
    print("Battery is: " + str(battery_level) + "%")

    state = await mower.mower_state()
    print("Mower state: " + state)

    activity = await mower.mower_activity()
    print("Mower activity: " + activity)

    # print("Running for 3 hours")
    # await mower.mower_override()

    # print("Pause")
    # await mower.mower_pause()

    # print("Resume")
    # await mower.mower_resume()

    # state = await mower.mower_state()
    # print("Mower state: " + state)

    # activity = await mower.mower_activity()
    # print("Mower activity: " + activity)

    await mower.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    device_group = parser.add_mutually_exclusive_group(required=True)

    device_group.add_argument(
        "--address",
        metavar="<address>",
        help="the Bluetooth address of the Automower device to connect to",
    )

    args = parser.parse_args()

    mower = Mower(1197489078, args.address)

    log_level = logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main(mower))
