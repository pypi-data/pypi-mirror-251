from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.messwertstatus import Messwertstatus
from ..enum.messwertstatuszusatz import Messwertstatuszusatz


class Zeitreihenwert(BaseModel):
    """
    Abbildung eines Zeitreihenwertes bestehend aus Zeitraum, Wert und Statusinformationen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitreihenwert.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihenwert JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zeitreihenwert.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    datum_uhrzeit_bis: datetime | None = Field(default=None, alias="datumUhrzeitBis", title="Datumuhrzeitbis")
    datum_uhrzeit_von: datetime | None = Field(default=None, alias="datumUhrzeitVon", title="Datumuhrzeitvon")
    status: Messwertstatus | None = None
    statuszusatz: Messwertstatuszusatz | None = None
    wert: Decimal | None = Field(default=None, title="Wert")
