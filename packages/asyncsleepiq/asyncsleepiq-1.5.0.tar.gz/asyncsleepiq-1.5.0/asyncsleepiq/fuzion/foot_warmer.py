"""Foundation foor warmer for Fuzion SleepIQ API."""
from __future__ import annotations

from typing import Any

from ..consts import SIDES_FULL, FootWarmingTemps
from ..foot_warmer import SleepIQFootWarmer


class SleepIQFuzionFootWarmer(SleepIQFootWarmer):
    """Foot warmer representation for SleepIQ API."""

    max_foot_warming_time = 600

    async def set_foot_warming(self, temperature: FootWarmingTemps, time: int) -> None:
        """Set foot warmer state through API."""
        if time <= 0 or time > self.max_foot_warming_time:
            raise ValueError(f"Invalid Time, must be between 0 and {self.max_foot_warming_time}")

        args = [SIDES_FULL[self.side].lower(), temperature.name.lower(), str(time)]
        await self._api.bamkey(self.bed_id, "SetFootwarmingSettings", args)
        await self.update({})

    async def update(self, data: dict[str, Any]) -> None:
        """Update the foot warmer through the API."""
        args = [SIDES_FULL[self.side].lower()]
        self.preset = await self._api.bamkey(self.bed_id, "GetFootwarmingSettings", args)
