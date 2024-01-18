"""
Initialization of the IDUN Guardian Client
"""
import os
import asyncio
from typing import Union
import logging
from datetime import datetime
from .igeb_bluetooth import GuardianBLE
from .igeb_api import GuardianAPI
from .igeb_utils import check_platform, check_valid_mac, check_valid_uuid
import uuid
import gc
from typing import Union
from bleak import exc
from idun_data_models import RecordingIn, DataStreams, RecordingConfig
from .debug_logs import *


class GuardianClient:
    """
    Class object for the communication between Guardian Earbuds and Cloud API
    """

    def __init__(
        self,
        address: Union[str, None] = None,
        debug=True,
        debug_console=True,
    ) -> None:
        """Initialize the Guardian Client

        Args:
            address (str, optional): The MAC address of the Guardian Earbuds. Defaults to "00000000-0000-0000-0000-000000000000".
            debug (bool, optional): Enable debug logging. Defaults to True.
            debug_console (bool, optional): Enable debug logging to console. Defaults to True.

        Raises:
            ValueError: If the MAC address is not valid
        """
        self.is_connected = False
        self.debug = debug
        self.debug_to_console = debug_console
        self.connection_status = 0
        if self.debug:
            self.configure_logger()

        if address is not None:
            if self.check_ble_address(address):
                self.guardian_ble = GuardianBLE(address, debug=self.debug)
                self.address = address
        else:
            logging.info("No BLE address provided, will search for device...")
            print("No BLE address provided, will search for device..")
            self.guardian_ble = GuardianBLE(debug=self.debug)

        self.guardian_api = GuardianAPI(debug=self.debug)

    def configure_logger(self):
        """Configure the logger for the Guardian Client"""
        if not os.path.exists("./logs"):
            os.makedirs("logs")

        datestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"./logs/ble_info-{datestr}.log"

        if not os.path.exists(os.path.dirname(log_filename)):
            os.makedirs(os.path.dirname(log_filename))
        log_handlers = [logging.FileHandler(log_filename)]

        if self.debug_to_console:
            log_handlers.append(logging.StreamHandler())

        logging.basicConfig(
            level=logging.INFO,
            datefmt="%d-%b-%y %H:%M:%S",
            format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
            handlers=log_handlers,
        )

    def check_ble_address(self, address: str) -> bool:
        """Check if the BLE address is valid

        Args:
            address (str): The MAC address of the Guardian Earbuds

        Returns:
            bool: True if the address is valid, False otherwise
        """
        if (
            check_platform() == "Windows"
            or check_platform() == "Linux"
            and check_valid_mac(address)
        ):
            return True
        elif check_platform() == "Darwin" and check_valid_uuid(address):
            logging.info("Platform detected: Darwin")
            # print(f"UUID is valid for system Darwin: {address}")
            return True
        else:
            logging.error("Invalid BLE address")
            raise ValueError("Invalid BLE address")

    async def search_device(self):
        """Connect to the Guardian Earbuds

        Returns:
            is_connected: bool
        """

        self.address = await self.guardian_ble.search_device()

        return self.address

    async def get_device_address(self) -> str:
        """Get the MAC address of the Guardian Earbuds.
        It searches the MAC address of the device automatically. This
        address is used as the deviceID for cloud communication
        """
        device_address = await self.guardian_ble.get_device_mac(
            self.guardian_ble.client
        )
        return device_address

    async def start_recording(
        self,
        recording_timer: int = 36000,
        led_sleep: bool = False,
        experiment: str = "None provided",
        impedance_measurement: bool = False,
        mains_freq_60hz: bool = False,
        sending_timout: float = 2,
        bi_directional_receiving_timeout: float = 5,
        filter_data: bool = True,
    ):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.

        Args:
            recording_timer (int, optional): The duration of the recording in seconds. Defaults to 36000.
            led_sleep (bool, optional): Enable LED sleep mode. Defaults to False.
            experiment (str, optional): The name of the experiment. Defaults to "None provided". This will
                                        go to the log file.
            impedance_measurement (bool, optional): Enable impedance measurement. Defaults to False.
            mains_freq_60hz (bool, optional): Set to True if the mains frequency is 60Hz. Defaults to False.
            sending_timout (float): The timeout in seconds for sending data to the cloud. Defaults to 1.
                                    If no data is sent for a second the sending is interupted and the data
                                    is buffered. If you have a fast internet and you do not want to lose any data,
                                    then make 0.5 seconds. If you have slow internet and are fine with losing some data,
                                    then make 5 seconds. The seconds will be the amount lost before noticing internet loss.
            bi_directional_receiving_timeout (float): The timeout in seconds for receiving data from the cloud. Defaults to 4.
                                                      If no data is received for 5 seconds the receiving is interupted and the data
                                                      the connection will be re-established. If you have a fast internet and you do not want to lose
                                                      bi-directional data, then make 5 seconds. If you have slow internet and are fine with losing some data,
                                                      then make 10 seconds. The seconds will be the amount lost before noticing internet loss.


        Raises:
            ValueError: If the recording timer is not valid
        """
        # set the timers
        self.guardian_api.runtime_receipt_timeout = sending_timout
        self.guardian_api.runtime_bi_directional_timeout = (
            bi_directional_receiving_timeout
        )
        try:
            if self.debug:
                logging.info(
                    "[CLIENT]: Recording timer set to: %s seconds", recording_timer
                )
                logging.info("[CLIENT]: Start recording")

            print(f"[CLIENT]: Recording timer set to: {recording_timer} seconds")
            print("-----Recording starting------")

            data_queue: asyncio.Queue = asyncio.Queue(maxsize=86400)

            recording_id = "py-" + str(
                uuid.uuid4()
            )  # the recordingID is a unique ID for each recording
            logging.info("[CLIENT] Recording ID: %s", recording_id)
            # log the experiment name in bold using the logging module
            logging.info("[CLIENT] Experiment description: %s", experiment)

            while self.connection_status == 0:  # TRUE FALSE
                self.connection_status = await self.guardian_ble.connect_to_device()
                log_device_status(self.debug, self.connection_status)

            if filter_data:
                return_filtered_data = True
                return_raw_data = False
            else:
                return_filtered_data = False
                return_raw_data = True

            data_stream = RecordingConfig(
                data_stream_subscription=DataStreams(
                    # NOTE: enable the data streams you want to record
                    bp_filter_eeg=return_filtered_data,
                    raw_eeg=return_raw_data,
                )
            )

            self.guardian_api.deviceID = self.guardian_ble.mac_id
            self.guardian_api.guardian_rec = RecordingIn(
                recordingID=recording_id,
                displayName="Your Recording",
                config=data_stream,
            )
            task_list = []
            task_list.append(
                asyncio.create_task(
                    self.guardian_ble.run_ble_record(
                        data_queue,
                        recording_timer,
                        self.guardian_ble.mac_id,
                        led_sleep,
                        impedance_measurement,
                        mains_freq_60hz,
                    )
                )
            )
            task_list.append(
                asyncio.create_task(
                    self.guardian_api.connect_ws_api(
                        data_queue,
                        self.guardian_ble.mac_id,
                        recording_id,
                        impedance_measurement,
                    )
                )
            )

            await asyncio.wait(task_list)

        except exc.BleakError as err:
            logging.error("[CLIENT]: BLE error: %s", err)

        if self.debug:
            logging.info("[CLIENT]: -----------  All tasks are COMPLETED -----------")
        print(f"-----Recording ID {recording_id}------")
        try:
            print(f"-----Device ID {self.guardian_ble.mac_id}------")
        except Exception:
            print("An exception occurred, check if your device is switched on")

        print("-----Recording stopped------")

    def stop_recording(self):
        """Stop recording data from the Guardian Earbuds"""

    async def start_battery(self):
        """
        Start recording data from the Guardian Earbuds.
        Unidirectional websocket connection to the Guardian Cloud API.
        """
        print("-----Battery readout started------")
        if self.debug:
            logging.info("[CLIENT]: Start recording")

        ble_client_task = asyncio.create_task(self.guardian_ble.read_battery_level())
        await asyncio.wait([ble_client_task])

        if self.debug:
            logging.info("[CLIENT]: Disconnect BLE and close websocket connection")
        print("-----Battery check stopped------")
