# Clase para comprarar rangos de fechas 
from typing import NamedTuple
from datetime import datetime

class Range(NamedTuple):
    start: datetime
    end: datetime