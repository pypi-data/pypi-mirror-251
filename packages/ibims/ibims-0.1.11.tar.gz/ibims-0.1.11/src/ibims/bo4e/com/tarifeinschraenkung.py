from pydantic import BaseModel, ConfigDict, Field

from ..enum.voraussetzungen import Voraussetzungen
from .geraet import Geraet
from .menge import Menge


class Tarifeinschraenkung(BaseModel):
    """
    Mit dieser Komponente werden Einschränkungen für die Anwendung von Tarifen modelliert.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifeinschraenkung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifeinschraenkung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifeinschraenkung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    einschraenkungleistung: list[Menge] | None = Field(default=None, title="Einschraenkungleistung")
    einschraenkungzaehler: list[Geraet] | None = Field(default=None, title="Einschraenkungzaehler")
    voraussetzungen: list[Voraussetzungen] | None = Field(default=None, title="Voraussetzungen")
    zusatzprodukte: list[str] | None = Field(default=None, title="Zusatzprodukte")
