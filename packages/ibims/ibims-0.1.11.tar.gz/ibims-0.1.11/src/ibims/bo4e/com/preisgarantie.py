from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..enum.preisgarantietyp import Preisgarantietyp
from .zeitraum import Zeitraum


class Preisgarantie(BaseModel):
    """
    Definition für eine Preisgarantie mit der Möglichkeit verschiedener Ausprägungen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisgarantie.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisgarantie JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Preisgarantie.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    beschreibung: str | None = Field(default=None, title="Beschreibung")
    preisgarantietyp: Preisgarantietyp | None = None
    zeitliche_gueltigkeit: Zeitraum | None = Field(default=None, alias="zeitlicheGueltigkeit")
    creation_date: datetime | None = Field(default=None, alias="creationDate", title="Creationdate")
