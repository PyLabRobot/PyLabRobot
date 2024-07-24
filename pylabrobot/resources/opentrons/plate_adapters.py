""" Opentrons Plate Adapters """

from pylabrobot.resources.plate_adapter import PlateAdapter


def Opentrons_96_adapter_Vb(name: str) -> PlateAdapter:
  """ Opentrons cat. no.: 999-00028
  - Material: aluminium
  - Part of "Aluminium block set
  - Adapter for 96 well PCR plate (skirted, semi-, and non-skirted).
  - ANSI/SLAS footprint.
  """
  return PlateAdapter(
    name=name,
    size_x=127.76,
    size_y=85.48,
    size_z=18.55,
    dx=11.65,
    dy=8.51,
    dz=3.8, # TODO: correct dz once Plate definition has been completely fixed
    adapter_hole_size_x=5.46,
    adapter_hole_size_y=5.46,
    site_pedestal_z=15.5,
    model="Opentrons_96_adapter_Vb",
  )
