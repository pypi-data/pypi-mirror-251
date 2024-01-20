from ._grib2io import *
from ._grib2io import __doc__
from ._grib2io import _Grib2Message

try:
    from . import __config__
    __version__ = __config__.grib2io_version
except(ImportError):
    pass

__all__ = ['open','Grib2Message','_Grib2Message','show_config','interpolate',
           'interpolate_to_stations','tables','templates','utils','Grib2GridDef']

from .g2clib import __version__ as __g2clib_version__
from .g2clib import _has_jpeg
from .g2clib import _has_png
from .g2clib import _has_aec

has_jpeg_support = bool(_has_jpeg)
has_png_support  = bool(_has_png)
has_aec_support = bool(_has_aec)

def show_config():
    """Print grib2io build configuration information."""
    print(f'grib2io version {__version__} Configuration:\n')
    print(f'\tg2c library version: {__g2clib_version__}')
    print(f'\tJPEG compression support: {has_jpeg_support}')
    print(f'\tPNG compression support: {has_png_support}')
    print(f'\tAEC compression support: {has_aec_support}')
