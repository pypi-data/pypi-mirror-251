from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.zeiteinheit import Zeiteinheit


class Zeitraum(BaseModel):
    """
    Diese Komponente wird zur Abbildung von Zeiträumen in Form von Dauern oder der Angabe von Start und Ende verwendet.
    Es muss daher eine der drei Möglichkeiten angegeben sein:
    - Einheit und Dauer oder
    - Zeitraum: Startdatum bis Enddatum oder
    - Zeitraum: Startzeitpunkt (Datum und Uhrzeit) bis Endzeitpunkt (Datum und Uhrzeit)

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitraum.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitraum JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zeitraum.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    dauer: Decimal | None = Field(default=None, title="Dauer")
    einheit: Zeiteinheit | None = None
    enddatum: datetime | None = Field(default=None, title="Enddatum")
    endzeitpunkt: datetime | None = Field(default=None, title="Endzeitpunkt")
    startdatum: datetime | None = Field(default=None, title="Startdatum")
    startzeitpunkt: datetime | None = Field(default=None, title="Startzeitpunkt")
