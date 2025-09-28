from enum import StrEnum


# Brazilian electric energy market submercados
class Submarket(StrEnum):
    SOUTH = "S"
    SOUTHEAST = "SE"
    NORTHEAST = "NE"
    NORTH = "N"


class MigrationStatus(StrEnum):
    CREATED = "CRIADA"
    COMPLETED = "CONCLUIDA"
    REJECTED = "REPROVADA"
    CLOSED = "ENCERRADA"
    CANCELLED = "CANCELADA"
    EXPIRED = "EXPIRADA"
