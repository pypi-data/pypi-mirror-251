"""Main UTE API Wrapper module."""
"""
UTE (Administración Nacional de Usinas y Trasmisiones Eléctricas) API Wrapper.
Copyright (C) 2023 Roger Gonzalez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime, timedelta
from time import sleep
from typing import List, Optional

import requests

from .exceptions import (
    InvalidPlanException,
    InvalidPowerFactorException,
    MultipleDevicesException,
    ReadingRequestFailedException,
    ReadingResponseInvalidException,
    TariffException,
    UnsupportedMethodException,
)

API_VERSION_1 = "https://rocme.ute.com.uy/api/v1"
API_VERSION_2 = "https://rocme.ute.com.uy/api/v2"


class UTEClient:
    """
    UTE (Administración Nacional de Usinas y Trasmisiones Eléctricas) API Wrapper.

    Args:
        email (str): User email for authentication
        phone_number (str): User phone number for authentication
        device_id (str): UTE Device id
        average_cost_per_kwh (float): Average cost per kwh
        power_factor (float): Power factor

    Raises:
        InvalidPowerFactorException: If the power factor is not between 0 and 1
        MultipleDevicesException: If there are multiple devices associated with the account
        UnsupportedMethodException: If an unsupported method is used
        InvalidPlanException: If the plan is not valid
        ReadingRequestException: If the reading request is not valid
        TariffException: If the tariff is not valid
    """

    def __init__(
        self,
        email: str,
        phone_number: str,
        device_id: str = None,
        average_cost_per_kwh: float = None,
        power_factor: float = None,
    ):
        """
        Initialize the UTE client.

        Args:
            email (str): User email for authentication
            phone_number (str): User phone number for authentication
            device_id (str): UTE Device id
            average_cost_per_kwh (float): Average cost per kwh
            power_factor (float): Power factor

        Raises:
            InvalidPowerFactorException: If the power factor is not between 0 and 1
            MultipleDevicesException: If there are multiple devices associated with the account
            UnsupportedMethodException: If an unsupported method is used
            InvalidPlanException: If the plan is not valid
            ReadingRequestException: If the reading request is not valid
            TariffException: If the tariff is not valid
        """
        self.email = email
        self.phone_number = phone_number
        self.device_id = device_id
        self.average_cost_per_kwh = average_cost_per_kwh
        self.authorization = self._login()
        self.power_factor = power_factor
        self._validate_power_factor()
        self._initialize_device_id()
        self._initialize_average_cost_per_kwh()

    def _validate_power_factor(self):
        if self.power_factor and not 0 <= self.power_factor <= 1:
            raise InvalidPowerFactorException("Power factor must be between 0 and 1")

    def _initialize_device_id(self):
        if not self.device_id:
            self.device_id = self._select_device_id()

    def _initialize_average_cost_per_kwh(self):
        if not self.average_cost_per_kwh:
            self.average_cost_per_kwh = self._determine_average_cost()

    def _select_device_id(self) -> str:
        devices = self.get_devices_list()
        if len(devices) > 1:
            devices_dict = {device["name"]: device["accountServicePointId"] for device in devices}
            raise MultipleDevicesException(f"Multiple device IDs found. Valid options: {devices_dict}")
        return devices[0]["accountServicePointId"]

    def _determine_average_cost(self) -> float:
        try:
            tariff_type = self.get_account()["meterInfo"]["tariffType"].lower()
            return self.get_average_price(tariff_type)
        except KeyError:
            raise TariffException("Tariff type not standard. Explicit definition required.")

    def _make_request(self, method: str, url: str, data: Optional[dict] = None) -> requests.Response:
        """
        Make a HTTP request.

        Args:
            method (str): The HTTP method to use. Accepted methods are ``GET``, ``POST``.
            url (str): The URL to use for the request.
            authorization (str): Authorization token
            data (dict): The data to send in the body of the request.

        Returns:
            requests.Response: The response object.

        Raises:
            Exception: If the method is not supported.
        """
        headers = {
            "X-Client-Type": "Android",
            "User-Agent": "okhttp/3.8.1",
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "Keep-Alive",
        }

        try:
            if self.authorization:
                headers["Authorization"] = f"Bearer {self.authorization}"
        except AttributeError:
            pass

        return getattr(requests, method.lower(), self._method_not_supported)(url, headers=headers, json=data)

    def _method_not_supported(self, *args, **kwargs):
        raise UnsupportedMethodException("HTTP method not supported")

    def _login(self) -> str:
        """
        Login to UTE.

        Args:
            email (str): User email for authentication
            phone_number (str): User phone number for authentication

        Returns:
            str: Authorization token
        """
        url = f"{API_VERSION_1}/token"
        data = {
            "Email": self.email,
            "PhoneNumber": self.phone_number,
        }

        return self._make_request("POST", url, data=data).text

    def get_devices_list(self) -> List[dict]:
        """
        Get UTE devices list.

        Returns:
            List[dict]: List of devices
        """
        accounts_url = f"{API_VERSION_1}/accounts"
        return self._make_request("GET", accounts_url).json()["data"]

    def get_account(self) -> dict:
        """
        Get UTE account info from device id.

        Returns:
            dict: UTE account information
        """
        accounts_by_id_url = f"{API_VERSION_1}/accounts/{self.device_id}"
        return self._make_request("GET", accounts_by_id_url).json()["data"]

    def get_peak(self) -> dict:
        """
        Get UTE peak info from device id.

        Returns:
            dict: UTE peak info
        """
        peak_by_id_url = f"{API_VERSION_1}/accounts/{self.device_id}/peak"
        return self._make_request("GET", peak_by_id_url).json()["data"]

    def get_network_status(self) -> List[dict]:
        """
        Get UTE network status from device id.

        Returns:
            dict: UTE network status
        """
        network_status_url = f"{API_VERSION_1}/info/network/status"
        return self._make_request("GET", network_status_url).json()["data"]["summary"]

    def get_renewable_sources(self) -> str:
        """
        Get UTE renewable sources.

        Returns:
            str: UTE renewable sources percentage
        """
        global_demand_url = f"{API_VERSION_1}/info/demand/global"
        return self._make_request("GET", global_demand_url).json()["data"]["renewableSources"]

    def get_historic_consumption(
        self,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None,
    ) -> dict:
        """
        Generate UTE historic consumption from device id and date range.

        Args:
            date_start (str): Start date to check in format YYYY-MM-DD
            date_end (str): End date to check in format YYYY-MM-DD

        Returns:
            dict: UTE info
        """
        if date_start is None or date_end is None:
            yesterday = datetime.now() - timedelta(days=1)
            yesterday_formatted = yesterday.strftime("%Y-%m-%d")
            date_start = date_start or yesterday_formatted
            date_end = date_end or yesterday_formatted

        historic_url = f"{API_VERSION_2}/device/{self.device_id}/curvefromtodate/D/{date_start}/{date_end}"
        response = self._make_request("GET", historic_url).json()

        active_energy = {"total": {"sum_in_kwh": 0, "aproximated_cost_in_uyu": 0}}
        num_days = 0

        for item in response["data"]:
            if item["magnitudeVO"] == "IMPORT_ACTIVE_ENERGY":
                date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S%z")
                formatted_date = date.strftime("%d/%m/%Y")
                day_in_week = date.strftime("%A")

                if formatted_date not in active_energy:
                    active_energy[formatted_date] = {"kwh": 0, "aproximated_cost_in_uyu": 0}
                    num_days += 1

                value = round(float(item["value"]), 3)
                active_energy[formatted_date]["kwh"] += value
                active_energy[formatted_date]["aproximated_cost_in_uyu"] += round(value * self.average_cost_per_kwh, 3)
                active_energy[formatted_date]["day_in_week"] = day_in_week
                active_energy["total"]["sum_in_kwh"] += value

        total_kwh = active_energy["total"]["sum_in_kwh"]
        active_energy["total"]["aproximated_cost_in_uyu"] = round(total_kwh * self.average_cost_per_kwh, 3)
        active_energy["total"]["daily_average_cost"] = (
            round(active_energy["total"]["aproximated_cost_in_uyu"] / num_days, 3) if num_days > 0 else 0
        )

        return active_energy

    def _convert_powers_to_power_in_watts(self, readings: List[dict]) -> float:
        """
        Convert powers to power in watts and determine the system type (monophasic, biphasic, triphasic) automatically.

        Args:
            readings (List[dict]): List of readings

        Returns:
            float: Power in watts
        """
        SQUARE_ROOT_OF_THREE = 1.732
        reading_sums = {"I1": 0, "I2": 0, "I3": 0, "V1": 0, "V2": 0, "V3": 0}
        num_voltages = num_currents = 0

        for reading in readings:
            reading_type = reading.get("tipoLecturaMGMI")
            if reading_type in reading_sums and "valor" in reading:
                reading_sums[reading_type] += float(reading["valor"])
                num_voltages += "V" in reading_type
                num_currents += "I" in reading_type

        if num_voltages == 0 or num_currents == 0:
            return 0.0

        averaged_voltage = sum(reading_sums[v] for v in ["V1", "V2", "V3"]) / num_voltages
        averaged_current = sum(reading_sums[i] for i in ["I1", "I2", "I3"]) / num_currents

        if num_voltages == 3 and num_currents == 3:
            return round(averaged_voltage * averaged_current * self.power_factor * SQUARE_ROOT_OF_THREE, 3)

        return round(averaged_voltage * averaged_current * self.power_factor, 3)

    def get_current_usage_info(self) -> dict:
        """
        Get current usage info from device id.

        Returns:
            dict: UTE info

        Raises:
            ReadingRequestFailedException: If the reading request fails.
            ReadingResponseInvalidException: If the reading response is invalid.
        """
        reading_request_url = f"{API_VERSION_1}/device/readingRequest"
        reading_url = f"{API_VERSION_1}/device/{self.device_id}/lastReading/30"

        data = {"AccountServicePointId": self.device_id}

        reading_request = self._make_request("POST", reading_request_url, data=data)

        if reading_request.status_code != 200:
            raise ReadingRequestFailedException("Error getting reading request")

        response = self._make_request("GET", reading_url).json()

        while not response["success"]:
            sleep(5)
            response = self._make_request("GET", reading_url).json()

        readings = response.get("data", {}).get("readings")
        if readings is None:
            raise ReadingResponseInvalidException("Response data is missing 'readings'")

        power_in_watts = self._convert_powers_to_power_in_watts(readings)

        return {
            **response,
            "data": {
                **response.get("data", {}),
                "power_in_watts": power_in_watts,
                "using_power_factor": bool(self.power_factor),
            },
        }

    def get_average_price(self, plan: str) -> float:
        """
        Get the average price for a plan.

        Args:
            plan (str): Plan name. Can be "triple" or "doble"

        Returns:
            float: Average price

        Raises:
            Exception: If the plan is invalid
        """
        TRIPLE_HOUR_RATES = (11.032, 5.036, 2.298)
        DOUBLE_HOUR_RATES = (11.032, 4.422)
        if plan == "triple":
            # 11.032 UYU/kwh * 16.67% of the day (4 hours)
            # 5.036 UYU/kwh * 54.16% of the day (13 hours)
            # 2.298 UYU/kwh * 29.17% of the day (7 hours)
            return sum(rate * portion for rate, portion in zip(TRIPLE_HOUR_RATES, (0.1667, 0.2917, 0.5416)))

        if plan == "doble":
            # 11.032 UYU/kwh * 16.67% of the day (4 hours)
            # 4.422 UYU/kwh * 83.33% of the day (20 hours)
            return sum(rate * portion for rate, portion in zip(DOUBLE_HOUR_RATES, (0.1667, 0.8333)))

        raise InvalidPlanException("Invalid plan name.")
