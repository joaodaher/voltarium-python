from enum import StrEnum


# Brazilian electric energy market submercados
class Submarket(StrEnum):
    SOUTH = "S"
    SOUTHEAST = "SE"
    NORTHEAST = "NE"
    NORTH = "N"


API_BASE_URL = "https://api-abm.ccee.org.br"
API_BASE_URL_STAGING = "https://sandbox-api-abm.ccee.org.br"
