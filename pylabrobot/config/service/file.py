from pathlib import Path
from typing import IO, Union

from pylabrobot.config.config import Config
from pylabrobot.config.service.reader import ConfigReader
from pylabrobot.config.service.writer import ConfigWriter


class FileReader(ConfigReader[str]):
  """A ConfigReader that reads from a file"""

  def __init__(self, format_reader: ConfigReader[IO]):
    self.format_reader = format_reader

  def read(self, r: str) -> Config:
    """Read a Config object from a file."""
    with open(r, self.format_reader.open_mode) as f:
      return self.format_reader.read(f)


class FileWriter(ConfigWriter[str]):
  """A ConfigWriter that writes to a file"""

  def __init__(self, format_writer: ConfigWriter[IO]):
    self.format_writer = format_writer

  def write(self, w: str, cfg: Config):
    """Write a Config object to a file."""
    with open(w, self.format_writer.open_mode) as f:
      return self.format_writer.write(f, cfg)


class MultiReader(ConfigReader[str]):
  """A ConfigReader that can read from multiple formats"""

  def __init__(self, reader_map: dict[str, ConfigReader[IO]]):
    self.reader_map = reader_map

  def read(self, r: Union[str, Path]) -> Config:
    """Read a Config object from a file."""
    if isinstance(r, str):
      r = Path(r)
    file_ext = r.suffix.lstrip(".")
    reader = self.reader_map.get(file_ext)
    if reader is None:
      raise ValueError(f"Unknown file extension: {file_ext}")
    with open(r, reader.open_mode) as f:
      return reader.read(f)
