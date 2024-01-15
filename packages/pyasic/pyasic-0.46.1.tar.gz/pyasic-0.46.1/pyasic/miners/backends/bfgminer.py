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

from collections import namedtuple
from typing import List, Optional, Tuple

from pyasic.API.bfgminer import BFGMinerAPI
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

BFGMINER_DATA_LOC = DataLocations(
    **{
        str(DataOptions.MAC): DataFunction("get_mac"),
        str(DataOptions.MODEL): DataFunction("get_model"),
        str(DataOptions.API_VERSION): DataFunction(
            "get_api_ver", [RPCAPICommand("api_version", "version")]
        ),
        str(DataOptions.FW_VERSION): DataFunction(
            "get_fw_ver", [RPCAPICommand("api_version", "version")]
        ),
        str(DataOptions.HOSTNAME): DataFunction("get_hostname"),
        str(DataOptions.HASHRATE): DataFunction(
            "get_hashrate", [RPCAPICommand("api_summary", "summary")]
        ),
        str(DataOptions.EXPECTED_HASHRATE): DataFunction(
            "get_expected_hashrate", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.HASHBOARDS): DataFunction(
            "get_hashboards", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.ENVIRONMENT_TEMP): DataFunction("get_env_temp"),
        str(DataOptions.WATTAGE): DataFunction("get_wattage"),
        str(DataOptions.WATTAGE_LIMIT): DataFunction("get_wattage_limit"),
        str(DataOptions.FANS): DataFunction(
            "get_fans", [RPCAPICommand("api_stats", "stats")]
        ),
        str(DataOptions.FAN_PSU): DataFunction("get_fan_psu"),
        str(DataOptions.ERRORS): DataFunction("get_errors"),
        str(DataOptions.FAULT_LIGHT): DataFunction("get_fault_light"),
        str(DataOptions.IS_MINING): DataFunction("is_mining"),
        str(DataOptions.UPTIME): DataFunction("get_uptime"),
        str(DataOptions.CONFIG): DataFunction("get_config"),
    }
)


class BFGMiner(BaseMiner):
    """Base handler for BFGMiner based miners."""

    def __init__(self, ip: str, api_ver: str = "0.0.0") -> None:
        super().__init__(ip)
        # interfaces
        self.api = BFGMinerAPI(ip, api_ver)

        # static data
        self.api_type = "BFGMiner"
        # data gathering locations
        self.data_locations = BFGMINER_DATA_LOC

        # data storage
        self.api_ver = api_ver

    async def get_config(self) -> MinerConfig:
        # get pool data
        try:
            pools = await self.api.pools()
        except APIError:
            return self.config

        self.config = MinerConfig.from_api(pools)
        return self.config

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

    async def get_mac(self) -> str:
        return "00:00:00:00:00:00"

    async def get_api_ver(self, api_version: dict = None) -> Optional[str]:
        # Check to see if the version info is already cached
        if self.api_ver:
            return self.api_ver

        if not api_version:
            try:
                api_version = await self.api.version()
            except APIError:
                pass

        if api_version:
            try:
                self.api_ver = api_version["VERSION"][0]["API"]
            except (KeyError, IndexError):
                pass

        return self.api_ver

    async def get_fw_ver(self, api_version: dict = None) -> Optional[str]:
        # Check to see if the version info is already cached
        if self.fw_ver:
            return self.fw_ver

        if not api_version:
            try:
                api_version = await self.api.version()
            except APIError:
                pass

        if api_version:
            try:
                self.fw_ver = api_version["VERSION"][0]["CompileTime"]
            except (KeyError, IndexError):
                pass

        return self.fw_ver

    async def get_version(
        self, api_version: dict = None
    ) -> Tuple[Optional[str], Optional[str]]:
        # check if version is cached
        miner_version = namedtuple("MinerVersion", "api_ver fw_ver")
        return miner_version(
            api_ver=await self.get_api_ver(api_version),
            fw_ver=await self.get_fw_ver(api_version=api_version),
        )

    async def reboot(self) -> bool:
        return False

    async def get_fan_psu(self):
        return None

    async def get_hostname(self) -> Optional[str]:
        return None

    async def get_hashrate(self, api_summary: dict = None) -> Optional[float]:
        # get hr from API
        if not api_summary:
            try:
                api_summary = await self.api.summary()
            except APIError:
                pass

        if api_summary:
            try:
                return round(float(api_summary["SUMMARY"][0]["MHS 20s"] / 1000000), 2)
            except (IndexError, KeyError, ValueError, TypeError):
                pass

    async def get_hashboards(self, api_stats: dict = None) -> List[HashBoard]:
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

                    for i in range(
                        board_offset, board_offset + self.expected_hashboards
                    ):
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
            except (IndexError, KeyError, ValueError, TypeError):
                pass

        return hashboards

    async def get_env_temp(self) -> Optional[float]:
        return None

    async def get_wattage(self) -> Optional[int]:
        return None

    async def get_wattage_limit(self) -> Optional[int]:
        return None

    async def get_fans(self, api_stats: dict = None) -> List[Fan]:
        if not api_stats:
            try:
                api_stats = await self.api.stats()
            except APIError:
                pass

        fans_data = [None, None, None, None]
        if api_stats:
            try:
                fan_offset = -1

                for fan_num in range(0, 8, 4):
                    for _f_num in range(4):
                        f = api_stats["STATS"][1].get(f"fan{fan_num + _f_num}", 0)
                        if not f == 0 and fan_offset == -1:
                            fan_offset = fan_num
                if fan_offset == -1:
                    fan_offset = 1

                for fan in range(self.fan_count):
                    fans_data[fan] = api_stats["STATS"][1].get(
                        f"fan{fan_offset+fan}", 0
                    )
            except (KeyError, IndexError):
                pass
        fans = [Fan(speed=d) if d else Fan() for d in fans_data]

        return fans

    async def get_errors(self) -> List[MinerErrorData]:
        return []

    async def get_fault_light(self) -> bool:
        return False

    async def get_expected_hashrate(self, api_stats: dict = None) -> Optional[float]:
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
            except (KeyError, IndexError):
                pass

    async def is_mining(self, *args, **kwargs) -> Optional[bool]:
        return None

    async def get_uptime(self, *args, **kwargs) -> Optional[int]:
        return None
