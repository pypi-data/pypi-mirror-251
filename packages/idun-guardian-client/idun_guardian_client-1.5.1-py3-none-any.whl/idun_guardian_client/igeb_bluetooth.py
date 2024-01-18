"""
Guardian Bluetooth utils.
"""
import sys
import asyncio
import os
from codecs import utf_8_encode
import logging
import time
import base64
import datetime
import gc
from bleak import BleakClient, BleakScanner, exc
import typing
import platform
from .config import settings
from .debug_logs import *

SEARCH_BREAK = 3


class GuardianBLE:
    """Main Guardian BLE client."""

    def __init__(self, address: str = "", debug: bool = True) -> None:
        """Initialize the Guardian BLE client.

        Args:
            address (str, optional): BLE device address. Defaults to "".
            debug (bool, optional): Debug mode. Defaults to True.
        """
        self.client: typing.Optional[BleakClient] = None

        # Debugging mode
        self.address = address
        self.debug = debug
        self.write_to_file: bool = debug

        # Initial connection flags
        self.initialise_connection: bool = True
        self.connection_established = False
        self.time_left = True
        self.initial_time = True

        # Bluetooth reconnect delay
        self.original_time = time.time()
        self.reconnect_try_amount = 50
        self.try_to_connect_timeout = self.reconnect_try_amount

        # Bluetooth timings
        self.ble_delay = 1
        self.ble_stop_delay = 1
        self.device_lost = False

        # API timeings
        self.sent_final_package_time = 1

        # The timing constants
        self.sample_rate = 250
        self.amount_samples_packet = 20
        self.max_index = 256
        self.prev_index = 0
        self.prev_timestamp = 0

        self.remaining_time = 1

        self.get_ble_characteristic()
        self.device = None
        self.mac_id = ""
        self.platform = platform.system()
        self.teminating_ble_process = False
        loggig_ble_init(self.debug)

    def get_ble_characteristic(self) -> None:
        """Get the environment variables."""
        # General information
        self.battery_id = settings.UUID_BATT_GDK
        self.device_service = settings.UUID_DEVICE_SERVICE
        self.mac_uuid = settings.UUID_MAC_ID
        self.firmware_uuid = settings.UUID_FIRMWARE_VERSION

        # EEG/IMU measurement
        self.meas_eeg_id = settings.UUID_MEAS_EEGIMU
        self.command_id = settings.UUID_CMD
        self.start_cmd = settings.START_CMD
        self.stop_cmd = settings.STOP_CMD

        # Impedance measurement
        self.meas_imp_id = settings.UUID_MEAS_IMP
        self.start_imp_cmd = settings.START_IMP_CMD
        self.stop_imp_cmd = settings.STOP_IMP_CMD
        self.notch_freq_50_cfg = settings.NOTCH_FREQ_50_CFG
        self.notch_freq_60_cfg = settings.NOTCH_FREQ_60_CFG

        # LED control
        self.cfg_id = settings.UUID_CFG
        self.led_on_cfg = settings.LED_ON_CFG
        self.led_off_cfg = settings.LED_OFF_CFG

    async def get_ble_devices(self) -> list:
        """
        Scan for devices and return a list of devices.
        """
        devices_dict: dict = {}
        ble_device_list: list = []
        devices = await BleakScanner.discover()
        igeb_name = "IGEB"
        device_id = 0
        print("\n----- Available devices -----\n")
        print("Index | Name | Address")
        print("----------------------------")
        for _, device in enumerate(devices):
            # print device discovered
            if device.name == igeb_name:
                print(f"{device_id}     | {device.name} | {device.address}")
                devices_dict[device.address] = []
                devices_dict[device.address].append(device.name)
                ble_device_list.append(device.address)
                device_id += 1
        print("----------------------------\n")
        return ble_device_list

    async def get_device_mac(self, client) -> str:
        """Get the device MAC address.
        This is different from BLE device address
        (UUID on Mac or MAC address on Windows)

        Args:
            device_name (str): Device name

        Returns:
            str: MAC address
        """
        # async with BleakClient(self.address) as client:
        logging_searching(self.debug)
        value = bytes(await client.read_gatt_char(self.mac_uuid))
        await asyncio.sleep(self.ble_delay)
        firmware_version = bytes(await client.read_gatt_char(self.firmware_uuid))
        mac_address = value.decode("utf-8")
        firmware_decoded = firmware_version.decode("utf-8")
        mac_address = mac_address.replace(":", "-")

        logging_device_info(self.debug, mac_address, firmware_decoded)
        return mac_address

    async def search_device(self) -> str:
        """This function searches for the device and returns the address of the device.
        If the device is not found, it exits the program. If multiple devices are found,
        it asks the user to select the device. If one device is found, it returns the
        address of the device.

        Returns:
            _type_: _description_
        """

        while True:
            ble_device_list = await self.get_ble_devices()
            if len(ble_device_list) == 0:
                logging_device_not_found(self.debug, SEARCH_BREAK)
                await asyncio.sleep(SEARCH_BREAK)

            elif len(ble_device_list) == 1:
                logging_device_found(self.debug, ble_device_list)
                self.address = ble_device_list[0]
                break
            else:
                index_str = input(
                    "Enter the index of the GDK device you want to connect to \
                    \nIf cannot find the device, please restart the program and try again: "
                )
                index = int(index_str)
                self.address = ble_device_list[index]
                break

        logging_device_address(self.debug, self.address)

        return self.address

    async def connect_to_device(self):
        """
        This function initialises the connection to the device.
        It finds the device using the address, sets up callback,
        and connects to the device.
        """
        logging_trying_to_connect(self.debug, self.address)

        if not self.device:
            self.device = await BleakScanner.find_device_by_address(
                self.address, timeout=20.0
            )
        if not self.device:
            raise exc.BleakError(
                f"A device with address {self.address} could not be found."
            )

        if self.platform == "Windows":
            if not self.client:
                self.client = BleakClient(
                    self.device, disconnected_callback=self.disconnected_callback
                )
        else:
            self.client = None
            self.client = BleakClient(
                self.device, disconnected_callback=self.disconnected_callback
            )
        if self.client is not None:
            try:
                await asyncio.wait_for(self.client.connect(), timeout=4)
            except asyncio.TimeoutError:
                log_timeout_while_trying_connection(self.debug)
                pass
            except Exception as err:
                log_exception_while_trying_connection(self.debug, err)
                pass
            if self.client.is_connected:
                if self.mac_id == "":
                    try:
                        self.mac_id = await self.get_device_mac(self.client)

                    except Exception as err:
                        log_exception_unable_to_find_MACaddress(self.debug, err)
                        self.initialise_connection = True
                        self.connection_established = False
                        return 0
                if self.mac_id:
                    self.connection_established = True
                    self.initialise_connection = False
                    logging_connected(self.debug, self.address)
                    return 1

            else:
                log_no_connection_established(self.debug)
                try:
                    await self.client.disconnect()
                    await asyncio.sleep(4)
                except Exception:
                    log_exception_in_disconnecting(self.debug)
                gc.collect()
                self.initialise_connection = True
                self.connection_established = False
                return 0
        else:
            log_not_client_found(self.debug)

    def disconnected_callback(self, client):  # pylint: disable=unused-argument
        """
        Callback function when device is disconnected.

        Args:
            client (BleakClient): BleakClient object
        """
        logging_disconnected_recognised(self.debug)
        self.connection_established = False
        self.initialise_connection = True

    async def run_ble_record(
        self,
        data_queue: asyncio.Queue,
        record_time=60,
        mac_id="MAC_ID",
        led_sleep: bool = False,
        impedance_measurement: bool = False,
        mains_freq_60hz: bool = False,
    ) -> None:
        """
        This function runs the recording of the data. It sets up the bluetooth
        connection, starts the recording, and then reads the data and adds it to
        the queue. The API class then reads the data from the queue and sends it
        to the cloud.

        Args:
            data_queue (asyncio.Queue): Queue to store the data
            record_time (_type_): The time to record for
            mac_id (_type_): The MAC address of the device
            led_sleep (_type_): Whether to turn off the LED

        Raises:
            BleakError: _description_
        """

        def time_stamp_creator(new_index):
            """
            This function creates a timestamp for the cloud based on the
            time the recording started. Each time stamp is based on the index
            of that is sent from the device. The index is the number of iterates
            between 0 and 256. The time stamp is the 1/250s multiplied by the
            index.

            Args:
                new_index (int): Index of the data point from the ble packet

            Returns:
                str: Timestamp in the format of YYYY-MM-DDTHH:MM:SS
            """
            index_diff = new_index - self.prev_index

            if self.prev_timestamp == 0:
                time_data = datetime.datetime.now().astimezone().isoformat()
                # convert time_data to a float in seconds
                time_data = time.mktime(
                    datetime.datetime.strptime(
                        time_data, "%Y-%m-%dT%H:%M:%S.%f%z"
                    ).timetuple()
                )
                new_time_stamp = time_data
            else:
                multiplier = (index_diff + self.max_index) % self.max_index
                new_time_stamp = (
                    self.amount_samples_packet * (1 / self.sample_rate) * multiplier
                ) + self.prev_timestamp

            self.prev_index = new_index
            self.prev_timestamp = new_time_stamp

            time_stamp_isoformat = (
                datetime.datetime.fromtimestamp(new_time_stamp).astimezone().isoformat()
            )

            return time_stamp_isoformat

        async def data_handler(_, data):
            """Data handler for the BLE client.
                Data is put in a queue and forwarded to the API.

            Args:
                callback (handler Object): Handler object
                data (bytes): Binary data package
            """
            data_base_64 = base64.b64encode(data).decode("ascii")
            new_time_stamp = time_stamp_creator(data[1])

            if self.write_to_file:
                self.data_recording_logfile.write(f"{data_base_64},\n")

            package = {
                "timestamp": new_time_stamp,
                "deviceID": mac_id,
                "data": data_base_64,
                "stop": False,
            }
            if not data_queue.full():
                await asyncio.shield(data_queue.put(package))
            else:
                await asyncio.shield(data_queue.get())

        async def battery_handler(_, data):
            """Battery handler for the BLE client.
            Args:
                callback (handler Object): Handler object
                data (bytes): Battery Level as uint8_t
            """
            logging_batterylevel(self.debug, data)

        async def impedance_handler(_, data):
            """Impedance handler for the BLE client.
                Data is put in a queue and forwarded to the API.

            Args:
                callback (handler Object): Handler object
                data (bytes): Binary data package with impedance values
            """
            data_int = int.from_bytes(data, byteorder="little")
            print(f"[BLE]: Impedance value : {round(data_int/1000,2)} kOhms")
            if self.write_to_file:
                self.data_recording_logfile.write(f"{data_int}\n")

            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "deviceID": mac_id,
                "stop": False,
                "impedance": data_int,
            }
            # add the received impedance data to the queue
            if not data_queue.full():
                await data_queue.put(package)
            else:
                await data_queue.get()

        async def send_start_commands_recording():
            """Send start commands to the device."""
            logging_sending_start(self.debug)

            # ------------------ Configuration ------------------
            if led_sleep:
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.led_off_cfg)[0]
                )
            # ------------------ Subscribe to notifications ------------------
            # Notify the client that these two services are required
            logging_subscribing_eeg_notification(self.debug)
            await asyncio.sleep(self.ble_delay)
            await self.client.start_notify(self.meas_eeg_id, data_handler)

            logging_subscribing_battery_notification(self.debug)
            await asyncio.sleep(self.ble_delay)
            await self.client.start_notify(self.battery_id, battery_handler)

            # ------------------ Start commands ------------------
            # sleep so that cleint can respond
            await asyncio.sleep(self.ble_delay)
            # send start command for recording data
            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.start_cmd)[0]
            )

        async def send_start_commands_impedance():
            # ----------------- Configuration -----------------
            if mains_freq_60hz:
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.notch_freq_60_cfg)[0]
                )
            else:
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.notch_freq_50_cfg)[0]
                )

            # ----------------- Subscribe -----------------
            logging_subscribing_impedance_notification(self.debug)
            await asyncio.sleep(self.ble_delay)
            await self.client.start_notify(self.meas_imp_id, impedance_handler)

            # ----------------- Send start command -----------------
            logging_starting_impedance_measurement_commands(self.debug)
            await asyncio.sleep(self.ble_delay)
            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.start_imp_cmd)[0]
            )

        async def stop_impedance_timeout():
            """Stop recording gracefully."""
            # make sure the last data is now a stop command
            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "deviceID": mac_id,
                "stop": True,
            }
            # ------------------ Load final stop package ------------------
            if not data_queue.full():
                await data_queue.put(package)
            else:
                await data_queue.get()
                await data_queue.put(package)
            logging_sending_stop(self.debug)
            # ------------------ API should send already loaded package  ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # This gives time for the api to send already loaded data
            logging_sending_stop_device(self.debug)
            await asyncio.sleep(self.ble_delay)

            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.stop_imp_cmd)[0]
            )

            # ------------------ Disconnect command to device ------------------
            logging_sending_disconnect(self.debug)
            await asyncio.sleep(self.ble_stop_delay)
            await self.client.disconnect()
            await asyncio.sleep(self.ble_stop_delay)

            if self.write_to_file:
                self.data_recording_logfile.close()
            logging_recording_successfully_stopped(self.debug)

        async def stop_recording_timeout():
            """Stop recording gracefully."""

            # make sure the last data is now a stop command
            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "deviceID": mac_id,
                "data": "STOP_TIMEOUT",
                "stop": True,
            }
            # ------------------ Load final stop package ------------------
            if not data_queue.full():
                await data_queue.put(package)
            else:
                await data_queue.get()
                await data_queue.put(package)
            logging_sending_stop(self.debug)
            # ------------------ API should send already loaded package  ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # This gives time for the api to send already loaded data
            logging_sending_stop_device(self.debug)
            await asyncio.sleep(self.ble_delay)

            await self.client.write_gatt_char(
                self.command_id, utf_8_encode(self.stop_cmd)[0]
            )

            if led_sleep:
                logging_turn_ble_on(self.debug)
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.led_on_cfg)[0]
                )
            # ------------------ Disconnect command to device ------------------
            logging_sending_disconnect(self.debug)
            await asyncio.sleep(self.ble_stop_delay)
            await self.client.disconnect()
            await asyncio.sleep(self.ble_stop_delay)

            if self.write_to_file:
                self.data_recording_logfile.close()
            logging_recording_successfully_stopped(self.debug)

        async def stop_impedance_cancelled_script():
            """Stop recording abruptly."""
            logging_keyboard_interrupt(self.debug)

            # ------------------ Sending final API packages ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # Give API time to send last package
            # With its own interupt handling
            # ------------------ Send stop EEG recording command ------------------
            logging_sending_stop_device(self.debug)
            await asyncio.sleep(self.ble_delay)
            try:
                await self.client.write_gatt_char(
                    self.command_id, utf_8_encode(self.stop_imp_cmd)[0]
                )
            except Exception:
                log_device_not_connected_cannot_stop(self.debug)

            # ------------------ Disconnecting commands ------------------
            logging_sending_disconnect(self.debug)
            await asyncio.sleep(self.ble_stop_delay)

            await self.client.disconnect()

            log_exception_in_disconnecting(self.debug)
            await asyncio.sleep(self.ble_stop_delay)
            # ------------------ Closing file  ------------------
            if self.write_to_file:
                self.data_recording_logfile.close()
            logging_recording_successfully_stopped(self.debug)
            # ------------------ Sending final API packages ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # Give API time to send last package
            # With its own interupt handling

        async def stop_recording_cancelled_script():
            """Stop recording abruptly."""
            logging_keyboard_interrupt(self.debug)

            # ------------------ Sending final API packages ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # Give API time to send last package
            # With its own interupt handling
            # ------------------ Send stop EEG recording command ------------------
            logging_sending_stop_device(self.debug)
            await asyncio.sleep(self.ble_delay)
            try:
                await self.client.write_gatt_char(
                    self.command_id, utf_8_encode(self.stop_cmd)[0]
                )
            except Exception:
                log_device_not_connected_cannot_stop(self.debug)

            # ------------------ Configuring LED back on ------------------
            if led_sleep:
                logging_turn_led_on(self.debug)
                await asyncio.sleep(self.ble_delay)
                await self.client.write_gatt_char(
                    self.cfg_id, utf_8_encode(self.led_on_cfg)[0]
                )
            # ------------------ Disconnecting commands ------------------
            logging_sending_disconnect(self.debug)
            await asyncio.sleep(self.ble_stop_delay)

            await self.client.disconnect()

            await asyncio.sleep(self.ble_stop_delay)
            # ------------------ Closing file  ------------------
            if self.write_to_file:
                self.data_recording_logfile.close()
            logging_recording_successfully_stopped(self.debug)
            # ------------------ Sending final API packages ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # Give API time to send last package
            # With its own interupt handling

        async def stop_recording_device_lost():
            """Stop recording device lost."""
            logging_device_lost_give_up(self.debug)
            # ------------------ Sending final API packages ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(self.ble_delay)  # Give API time to send last package
            # ------------------ Loading last package ------------------
            logging_sending_stop(self.debug)
            package = {
                "timestamp": datetime.datetime.now().astimezone().isoformat(),
                "deviceID": mac_id,
                "data": "STOP_DEVICE_LOST",
                "stop": True,
            }
            # pack the stop command
            if not data_queue.full():
                await data_queue.put(package)
            else:
                await data_queue.get()
                await data_queue.put(package)
            # ------------------ Sending final API packages ------------------
            logging_giving_time_api(self.debug)
            await asyncio.sleep(
                self.sent_final_package_time
            )  # Give API time to send last package
            # ------------------ Closing file ------------------
            if self.write_to_file:
                self.data_recording_logfile.close()

            return True

        async def bluetooth_reconnect():
            """Set flags to reconnect to bluetooth device."""
            self.try_to_connect_timeout = self.try_to_connect_timeout - 1
            if self.try_to_connect_timeout <= 0:
                self.device_lost = await stop_recording_device_lost()
            logging_trying_to_connect_again(self.debug, self.try_to_connect_timeout)
            self.connection_established = False
            self.initialise_connection = True

        def initialise_file():
            """Initialise file for recording."""
            if self.write_to_file:
                if not os.path.exists("./logs"):
                    os.makedirs("logs")

                if not impedance_measurement:
                    measurement_type = "rec"
                else:
                    measurement_type = "imp"

                datestr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                recording_filename = f"./logs/IGEB-{measurement_type}-{datestr}.txt"
                self.data_recording_logfile = open(
                    recording_filename, "w", encoding="utf-8"
                )

        def initialise_timestamps():
            if self.initial_time:
                self.initial_time = False  # record that this is the initial time
                self.original_time = time.time()

        async def main_loop():
            while True:
                if self.connection_established:
                    await asyncio.shield(
                        asyncio.sleep(self.ble_delay)
                    )  # sleep so that everything can happen
                    self.remaining_time = record_time - (
                        time.time() - self.original_time
                    )
                    print(f"Time left: {round(self.remaining_time)}s")

                    if self.remaining_time <= 0:
                        logging_time_reached(self.debug, self.original_time)
                        if not impedance_measurement:
                            await stop_recording_timeout()
                        else:
                            await stop_impedance_timeout()
                        break

                else:
                    break

        # >>>>>>>>>>>>>>>>>>>>> Start of recording process <<<<<<<<<<<<<<<<<<<<<<<<
        # ------------------ Initialise values for timestamps ------------------
        self.prev_timestamp = 0
        self.prev_index = -1
        # ------------------ Initialise time values for recording timeout ------------------
        # This has been decoupled from the device timing for robustness
        self.original_time = time.time()
        self.initial_time = True
        self.time_left = True
        self.initial_time = True
        # ------------------ Initialise connection values for trying to connect again ------------------
        # self.connection_established = False
        self.try_to_connect_timeout = self.reconnect_try_amount
        # ------------------ Initialise log file ------------------
        initialise_file()

        while not self.teminating_ble_process:
            log_connection_flag(self.debug, self.connection_established)
            log_connection_initialize_flag(self.debug, self.initialise_connection)

            try:
                if self.initialise_connection:
                    while self.initialise_connection == True:
                        await self.connect_to_device()
                if self.client is not None:
                    if self.client.is_connected:
                        logging_device_connected_general(self.debug)
                        # for windows reconnection
                        self.initialise_connection = True

                    if not impedance_measurement:
                        await send_start_commands_recording()
                    else:
                        await send_start_commands_impedance()

                    logging_recording_started(self.debug)
                    self.try_to_connect_timeout = (
                        self.reconnect_try_amount
                    )  # reset counter
                    # >>>>>>>>>>>>>>>>>>>>> Main loop <<<<<<<<<<<<<<<<<<<<<<<<
                    initialise_timestamps()
                    await asyncio.shield(main_loop())
                    # >>>>>>>>>>>>>>>>>>>>> Main loop <<<<<<<<<<<<<<<<<<<<<<<<

                if self.remaining_time <= 0:
                    self.teminating_ble_process = True
                    break

                if not self.connection_established:
                    logging_disconnected_recognised(self.debug)
                    await bluetooth_reconnect()
                    if self.device_lost:
                        break

            except asyncio.CancelledError:
                if not impedance_measurement:
                    await stop_recording_cancelled_script()
                else:
                    await stop_impedance_cancelled_script()
                self.teminating_ble_process = True
                self.connection_established = False
                self.initialise_connection = False
                break

            except Exception as error:
                logging_ble_client_lost(self.debug, error)

            finally:
                logging_ensuring_ble_disconnected(self.debug)
                await asyncio.sleep(self.ble_stop_delay)
                if self.client is not None:
                    if self.client.is_connected:
                        try:
                            print("Stop notification")
                            await self.client.stop_notify(self.meas_eeg_id)
                            await asyncio.sleep(self.ble_delay)
                            await self.client.stop_notify(self.battery_id)
                            await asyncio.sleep(self.ble_delay)
                            await self.client.disconnect()
                            gc.collect()
                        except Exception:
                            log_exception_in_disconnecting(self.debug)

                await asyncio.sleep(self.ble_stop_delay)
                self.connection_established = False

        logging_ble_complete(self.debug)

    async def get_service_and_char(self) -> None:
        """Get the services and characteristics of the device."""
        try:
            async with BleakClient(self.address) as client:
                logging_device_connected_general(self.debug)

                for service in client.services:
                    logging_device_info_uuid(self.debug, service)

                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                            except exc.BleakError as err:
                                value = str(err).encode()
                        else:
                            value = None
                        logging_device_info_characteristic(self.debug, char, value)

                await asyncio.sleep(self.ble_stop_delay)
                await client.disconnect()
                await asyncio.sleep(self.ble_stop_delay)
                logging_sending_disconnect(self.debug)

        except exc.BleakError as err:
            logging_device_connection_failed(self.debug, err)

    async def read_battery_level(self) -> None:
        """Read the battery level of the device given pre-defined interval."""
        logging_reading_battery_level(self.debug)
        while True:
            try:
                async with BleakClient(self.address) as client:
                    logging_device_connected_general(self.debug)

                    await asyncio.sleep(self.ble_delay)
                    value = int.from_bytes(
                        (await client.read_gatt_char(self.battery_id)),
                        byteorder="little",
                    )
                    print("-----------------------------")
                    print(f"\nBattery level: {value}%\n")
                    print("-----------------------------")
                    logging_batterylevel_int(self.debug, value)

                    await asyncio.sleep(self.ble_stop_delay)
                    await client.disconnect()
                    await asyncio.sleep(self.ble_stop_delay)
                    logging_sending_disconnect(self.debug)
                    break

            except exc.BleakError as err:
                # log the error
                logging_device_connection_failed(self.debug, err)
                await asyncio.sleep(3)
                continue

    async def get_device_information(self) -> dict:
        """Read the device information of the device."""

        device_info = {}

        async with BleakClient(self.address) as client:
            logging_device_connected_general(self.debug)

            for service in client.services:
                if service.uuid == self.device_service:
                    for char in service.characteristics:
                        if "read" in char.properties:
                            try:
                                value = bytes(await client.read_gatt_char(char.uuid))
                            except exc.BleakError as err:
                                value = str(err).encode()
                        else:
                            value = None

                        print(f"{ char.description}:{str(value)}")
                        device_info[char.description] = str(value)
                        logging_device_description_list(self.debug, char, value)

        return device_info
