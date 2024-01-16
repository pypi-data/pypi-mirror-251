# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

import logging
from typing import List, Optional

from pyasic.API.bmminer import BMMinerAPI
from pyasic.config import MinerConfig
from pyasic.data import Fan, HashBoard
from pyasic.data.error_codes import MinerErrorData
from pyasic.errors import APIError
from pyasic.miners.base import (
    BaseMiner,
    DataFunction,
    DataLocations,
    DataOptions,
    RPCAPICommand,
)

BMMINER_DATA_LOC = DataLocations(
    **{
        str(DataOptions.MAC): DataFunction("_get_mac"),
        str(DataOptions.API_VERSION): DataFunction(
            "_get_api_ver", [RPCAPICommand("api_version", "version")]
        ),
        str(DataOptions.FW_VERSION): DataFunction(
            "_get_fw_ver", [RPCAPICommand("api_version", "version")]
        ),
        str(DataOptions.HOSTNAME): DataFunction("_get_hostname"),
        str(DataOptions.HASHRATE): DataFunction(
            "_get_hashrate", [RPCAPICommand("api_summary", "summary")]
        ),
        str(DataOptions.EXPECTED_HASHRATE): DataFunction(
            "_get_expected_hashrate", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.HASHBOARDS): DataFunction(
            "_get_hashboards", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.ENVIRONMENT_TEMP): DataFunction("_get_env_temp"),
        str(DataOptions.WATTAGE): DataFunction("_get_wattage"),
        str(DataOptions.WATTAGE_LIMIT): DataFunction("_get_wattage_limit"),
        str(DataOptions.FANS): DataFunction(
            "_get_fans", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.FAN_PSU): DataFunction("_get_fan_psu"),
        str(DataOptions.ERRORS): DataFunction("_get_errors"),
        str(DataOptions.FAULT_LIGHT): DataFunction("_get_fault_light"),
        str(DataOptions.IS_MINING): DataFunction("_is_mining"),
        str(DataOptions.UPTIME): DataFunction(
            "_get_uptime", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.CONFIG): DataFunction("get_config"),
    }
)


class BMMiner(BaseMiner):
    """Base handler for BMMiner based miners."""

    def __init__(self, ip: str, api_ver: str = "0.0.0") -> None:
        super().__init__(ip)
        # interfaces
        self.api = BMMinerAPI(ip, api_ver)

        # static data
        self.api_type = "BMMiner"
        # data gathering locations
        self.data_locations = BMMINER_DATA_LOC

        # data storage
        self.api_ver = api_ver

    async def send_ssh_command(self, cmd: str) -> Optional[str]:
        result = None

        try:
            conn = await self._get_ssh_connection()
        except ConnectionError:
            return None

        # open an ssh connection
        async with conn:
            # 3 retries
            for i in range(3):
                try:
                    # run the command and get the result
                    result = await conn.run(cmd)
                    result = result.stdout

                except Exception as e:
                    # if the command fails, log it
                    logging.warning(f"{self} command {cmd} error: {e}")

                    # on the 3rd retry, return None
                    if i == 3:
                        return
                    continue
        # return the result, either command output or None
        return result

    async def get_config(self) -> MinerConfig:
        # get pool data
        try:
            pools = await self.api.pools()
        except APIError:
            return self.config

        self.config = MinerConfig.from_api(pools)
        return self.config

    async def reboot(self) -> bool:
        logging.debug(f"{self}: Sending reboot command.")
        ret = await self.send_ssh_command("reboot")
        logging.debug(f"{self}: Reboot command completed.")
        if ret is None:
            return False
        return True

    async def send_config(self, config: MinerConfig, user_suffix: str = None) -> None:
        return None

    async def fault_light_off(self) -> bool:
        return False

    async def fault_light_on(self) -> bool:
        return False

    async def restart_backend(self) -> bool:
        return False

    async def stop_mining(self) -> bool:
        return False

    async def resume_mining(self) -> bool:
        return False

    async def set_power_limit(self, wattage: int) -> bool:
        return False

    ##################################################
    ### DATA GATHERING FUNCTIONS (get_{some_data}) ###
    ##################################################

    async def _get_mac(self) -> Optional[str]:
        return None

    async def _get_api_ver(self, api_version: dict = None) -> Optional[str]:
        if not api_version:
            try:
                api_version = await self.api.version()
            except APIError:
                pass

        if api_version:
            try:
                self.api_ver = api_version["VERSION"][0]["API"]
            except LookupError:
                pass

        return self.api_ver

    async def _get_fw_ver(self, api_version: dict = None) -> Optional[str]:
        if not api_version:
            try:
                api_version = await self.api.version()
            except APIError:
                pass

        if api_version:
            try:
                self.fw_ver = api_version["VERSION"][0]["CompileTime"]
            except LookupError:
                pass

        return self.fw_ver

    async def _get_fan_psu(self):
        return None

    async def _get_hostname(self) -> Optional[str]:
        hn = await self.send_ssh_command("cat /proc/sys/kernel/hostname")
        return hn

    async def _get_hashrate(self, api_summary: dict = None) -> Optional[float]:
        # get hr from API
        if not api_summary:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary:
            try:
                return round(float(api_summary["SUMMARY"][0]["GHS 5s"] / 1000), 2)
            except (LookupError, ValueError, TypeError):
                pass

    async def _get_hashboards(self, api_stats: dict = None) -> List[HashBoard]:
        hashboards = []

        if not api_stats:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        if api_stats:
            try:
                board_offset = -1
                boards = api_stats["STATS"]
                if len(boards) > 1:
                    for board_num in range(1, 16, 5):
                        for _b_num in range(5):
                            b = boards[1].get(f"chain_acn{board_num + _b_num}")

                            if b and not b == 0 and board_offset == -1:
                                board_offset = board_num
                    if board_offset == -1:
                        board_offset = 1

                    real_slots = []

                    for i in range(board_offset, board_offset + 4):
                        try:
                            key = f"chain_acs{i}"
                            if boards[1].get(key, "") != "":
                                real_slots.append(i)
                        except LookupError:
                            pass

                    if len(real_slots) < 3:
                        real_slots = list(
                            range(board_offset, board_offset + self.expected_hashboards)
                        )

                    for i in real_slots:
                        hashboard = HashBoard(
                            slot=i - board_offset, expected_chips=self.expected_chips
                        )

                        chip_temp = boards[1].get(f"temp{i}")
                        if chip_temp:
                            hashboard.chip_temp = round(chip_temp)

                        temp = boards[1].get(f"temp2_{i}")
                        if temp:
                            hashboard.temp = round(temp)

                        hashrate = boards[1].get(f"chain_rate{i}")
                        if hashrate:
                            hashboard.hashrate = round(float(hashrate) / 1000, 2)

                        chips = boards[1].get(f"chain_acn{i}")
                        if chips:
                            hashboard.chips = chips
                            hashboard.missing = False
                        if (not chips) or (not chips > 0):
                            hashboard.missing = True
                        hashboards.append(hashboard)
            except (LookupError, ValueError, TypeError):
                pass

        return hashboards

    async def _get_env_temp(self) -> Optional[float]:
        return None

    async def _get_wattage(self) -> Optional[int]:
        return None

    async def _get_wattage_limit(self) -> Optional[int]:
        return None

    async def _get_fans(self, api_stats: dict = None) -> List[Fan]:
        if not api_stats:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        fans = [Fan() for _ in range(self.expected_fans)]
        if api_stats:
            try:
                fan_offset = -1

                for fan_num in range(1, 8, 4):
                    for _f_num in range(4):
                        f = api_stats["STATS"][1].get(f"fan{fan_num + _f_num}", 0)
                        if f and not f == 0 and fan_offset == -1:
                            fan_offset = fan_num
                if fan_offset == -1:
                    fan_offset = 1

                for fan in range(self.expected_fans):
                    fans[fan].speed = api_stats["STATS"][1].get(
                        f"fan{fan_offset+fan}", 0
                    )
            except LookupError:
                pass

        return fans

    async def _get_errors(self) -> List[MinerErrorData]:
        return []

    async def _get_fault_light(self) -> bool:
        return False

    async def _get_expected_hashrate(self, api_stats: dict = None) -> Optional[float]:
        # X19 method, not sure compatibility
        if not api_stats:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        if api_stats:
            try:
                expected_rate = api_stats["STATS"][1]["total_rateideal"]
                try:
                    rate_unit = api_stats["STATS"][1]["rate_unit"]
                except KeyError:
                    rate_unit = "GH"
                if rate_unit == "GH":
                    return round(expected_rate / 1000, 2)
                if rate_unit == "MH":
                    return round(expected_rate / 1000000, 2)
                else:
                    return round(expected_rate, 2)
            except LookupError:
                pass

    async def _is_mining(self, *args, **kwargs) -> Optional[bool]:
        return None

    async def _get_uptime(self, api_stats: dict = None) -> Optional[int]:
        if not api_stats:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        if api_stats:
            try:
                return int(api_stats["STATS"][1]["Elapsed"])
            except LookupError:
                pass
