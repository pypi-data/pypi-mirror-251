import logging
import math
import os
from threading import Event, Thread
from typing import Callable, Dict, List

import numpy as np
import requests
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger(__name__)

# Middleware Network Application ID (task ID, NETAPP_ID).
MIDDLEWARE_TASK_ID = str(
    os.getenv("MIDDLEWARE_TASK_ID", os.getenv("NETAPP_ID", "00000000-0000-0000-0000-000000000000"))
)
# NETAPP_ID used for compatibility.
NETAPP_ID = MIDDLEWARE_TASK_ID
NETAPP_ID_ROS = NETAPP_ID.replace("-", "_")
# Middleware robot ID (robot ID).
MIDDLEWARE_ROBOT_ID = str(os.getenv("MIDDLEWARE_ROBOT_ID", "00000000-0000-0000-0000-000000000000"))
# Middleware address.
MIDDLEWARE_ADDRESS = str(os.getenv("MIDDLEWARE_ADDRESS", "http://localhost"))
MIDDLEWARE_REPORT_INTERVAL = float(os.getenv("MIDDLEWARE_REPORT_INTERVAL", 1))
# Used for Network Application heart beat.
MAX_LATENCY = float(os.getenv("NETAPP_MAX_LATENCY", 100))

# Event name used for communication between clients and heartbeat module.
HEARTBEAT_CLIENT_EVENT = "heartbeat_client_event"


class LatencyMeasurements:
    """Class for holding data about processing times (latency)."""

    def __init__(self, num_latencies_to_keep: int = 10) -> None:
        self.num_latencies_to_keep = num_latencies_to_keep
        self.processing_latencies = np.zeros(num_latencies_to_keep)

    def store_latency(self, latency: float) -> None:
        """Store latency into "circular" list.

        Args:
            latency (float): Last latency.
        """

        # Remove the oldest entry and add the new one
        # Using strategy "Copy one before and substitute at the end" (fastest)
        self.processing_latencies[0:-1] = self.processing_latencies[1:]
        self.processing_latencies[-1] = latency

    def get_latencies(self) -> List[float]:
        """Get latencies.

        Returns:
            Latencies in list
        """
        latencies: list = self.processing_latencies.tolist()
        return latencies

    def get_avg_latency(self) -> float:
        """Get average latency.

        Returns:
            Average latency.
        """

        return float(np.mean(self.processing_latencies))


class RepeatedTimer(Thread):
    """Repeated interval timer of callback function in Thread."""

    def __init__(self, interval: float, callback: Callable):
        """Constructor.

        Args:
            interval (float): Interval in seconds.
            callback (Callable): Function to be called repeatedly.
        """

        super().__init__(daemon=True)
        self._stop_event = Event()
        self._callback = callback
        self._interval = interval

    def stop(self) -> None:
        """Set stop event to stop FCW worker."""

        self._stop_event.set()

    def run(self):
        """Periodically calls callback function."""

        self._stop_event = Event()
        while not self._stop_event.wait(self._interval):
            self._callback()


class HeartBeatSender:
    """HeartBeat to Middleware sender."""

    # TODO: Move to era_5g_server?
    def __init__(self) -> None:
        """Constructor.

        Try to connect to MIDDLEWARE_ADDRESS.
        """

        self.retries = Retry(total=0, read=0, connect=0, backoff_factor=0, status_forcelist=[429, 500, 502, 503, 504])
        self.session: requests.Session = requests.Session()
        self.adapter: HTTPAdapter = HTTPAdapter(max_retries=self.retries)
        self.session.mount(MIDDLEWARE_ADDRESS, self.adapter)
        self.connection_error = False

    def _send_heart_beat_request(self, headers: Dict, json: Dict, repeat_on_error: bool = False) -> None:
        """Send heart beat request to Middleware.

        Args:
            headers (Dict): Request headers.
            json (Dict): Request JSON.
            repeat_on_error (bool): If set, repeat requests further. Defaults to False.
        """

        if not self.connection_error or repeat_on_error:
            logger.debug(f"Sending heart beat to middleware: {json}")
            try:
                response = self.session.post(MIDDLEWARE_ADDRESS, headers=headers, json=json, timeout=(0.2, 0.2))
                if response.ok:
                    logger.debug(f"Middleware heart beat response: {response.text}")
                else:
                    logger.warning(
                        f"Middleware heart beat response: {response}, middleware address: {MIDDLEWARE_ADDRESS}"
                    )
                    self.connection_error = True
            except requests.RequestException as ex:
                logger.warning(f"Failed to connect to the middleware address: {MIDDLEWARE_ADDRESS}, {repr(ex)}")
                self.connection_error = True

    def send_robot_heart_beat(
        self,
        battery_level: float,
        cpu_utilization: List[float],
        ram_utilization: float,
        quality_map_status=None,
        repeat_on_error: bool = False,
    ) -> None:
        """Send robot heart beat to Middleware.

        Args:
            battery_level (float): Robot battery level.
            cpu_utilization (float): Robot CPU utilization.
            ram_utilization (float):  Robot RAM utilization.
            quality_map_status (None): Unused, will be updated.
            repeat_on_error (bool): If set, repeat requests further. Defaults to False.
        """

        data = {
            "RobotId": MIDDLEWARE_ROBOT_ID,
            "BatteryLevel": battery_level,
            "CPUUtilization": cpu_utilization,
            "RAMUtilization": ram_utilization,
            "QualityMapStatus": quality_map_status,
        }
        headers = {"Content-type": "application/json"}
        self._send_heart_beat_request(headers=headers, json=data, repeat_on_error=repeat_on_error)

    def send_middleware_heart_beat(
        self, avg_latency: float, queue_size: int, queue_occupancy: float, current_robot_count: int
    ) -> None:
        """Obsolete function, use send_application_heart_beat instead.

        Args:
            avg_latency (float): Average latency.
            queue_size (int): Queue size.
            queue_occupancy (float): Queue occupancy.
            current_robot_count (int): Current robot count.
        """
        self.send_application_heart_beat(avg_latency, queue_size, queue_occupancy, current_robot_count)

    def send_application_heart_beat(
        self,
        avg_latency: float,
        queue_size: int,
        queue_occupancy: float,
        current_robot_count: int,
        repeat_on_error: bool = False,
    ) -> None:
        """Send application heart beat to Middleware.

        Args:
            avg_latency (float): Average latency.
            queue_size (int): Queue size.
            queue_occupancy (float): Queue occupancy.
            current_robot_count (int): Current robot count.
            repeat_on_error (bool): If set, repeat requests further. Defaults to False.
        """

        # Latency can change over time, so reporting just the simple que occupancy can be misleading.
        # Instead, it is better to report occupancy in terms of:
        #  'total time estimated to be needed to process everything in the queue' / 'required max latency'
        processing_time_occupancy = queue_size * avg_latency / MAX_LATENCY

        if queue_size == 0:
            # If the queue is empty then no estimate can be made about robot count limit,
            # but most likely at least one more robot can be added.
            hard_robot_count_limit = current_robot_count + 1
            optimal_robot_count_limit = current_robot_count + 1
        elif avg_latency == 0:
            # If there are no latency measurements, the maximum number of robots cannot be estimated
            # using processing_time_occupancy, but we can still try to use queue_occupancy.
            hard_robot_count_limit = math.floor(current_robot_count / queue_occupancy)
            optimal_robot_count_limit = math.floor(hard_robot_count_limit * 0.8)
        else:
            hard_robot_count_limit = math.floor(current_robot_count / processing_time_occupancy)
            optimal_robot_count_limit = math.floor(hard_robot_count_limit * 0.8)

        data = {
            "Id": MIDDLEWARE_TASK_ID,
            "CurrentRobotsCount": current_robot_count,
            "OptimalLimit": optimal_robot_count_limit,
            "HardLimit": hard_robot_count_limit,
        }
        headers = {"Content-type": "application/json"}
        self._send_heart_beat_request(headers=headers, json=data, repeat_on_error=repeat_on_error)
