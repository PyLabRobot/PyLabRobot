import asyncio
from typing import Optional, Union

from pylabrobot.machine import MachineFrontend
from .backend import PumpBackend
from .calibration import PumpCalibration


class Pump(MachineFrontend):
  """ Frontend for a (peristaltic) pump.

  Attributes:
    backend: The backend that the pump is controlled through.
    calibration: The calibration of the pump.
  """

  def __init__(self, backend: PumpBackend, calibration: Optional[PumpCalibration] = None):
    self.backend: PumpBackend = backend
    self._setup_finished = False
    if calibration is not None:
      self.calibration = calibration[0]

  async def run_revolutions(self, num_revolutions: float):
    """ Run for a given number of revolutions.

    Args:
      num_revolutions: number of revolutions to run.
    """

    self.backend.run_revolutions(num_revolutions=num_revolutions)

  async def run_continuously(self, speed: float):
    """ Run continuously at a given speed.

    If speed is 0, the pump will be halted.

    Args:
      speed: speed in rpm/pump-specific units.
    """

    self.backend.run_continuously(speed=speed)

  async def run_for_duration(self, speed: Union[float, int], duration: Union[float, int]):
    """ Run the pump at specified speed for the specified duration.

    Args:
      speed: speed in rpm/pump-specific units.
      duration: duration to run pump.
    """

    if duration < 0:
      raise ValueError("Duration must be positive.")
    await self.run_continuously(speed=speed)
    await asyncio.sleep(duration)
    await self.run_continuously(speed=0)

  async def pump_volume(self, speed: Union[float, int],
                        volume: Union[float, int]):
    """ Run the pump at specified speed for the specified volume. Note that this function requires
    the pump to be calibrated at the input speed.

    Args:
      speed: speed in rpm/pump-specific units.
      volume: volume to pump.
    """

    if self.calibration is None:
      raise TypeError(
        "Pump is not calibrated. Volume based pumping and related functions unavailable.")
    duration = volume / self.calibration
    await self.run_for_duration(speed=speed, duration=duration)

  async def halt(self):
    """ Halt the pump."""
    self.backend.halt()
