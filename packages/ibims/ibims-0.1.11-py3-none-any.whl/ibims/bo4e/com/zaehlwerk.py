from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.abgabeart import Abgabeart
from ..enum.energierichtung import Energierichtung
from ..enum.mengeneinheit import Mengeneinheit


class Zaehlwerk(BaseModel):
    """
    Mit dieser Komponente werden Zählwerke modelliert.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zaehlwerk.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zaehlwerk JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zaehlwerk.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    einheit: Mengeneinheit | None = None
    obis_kennzahl: str | None = Field(default=None, alias="obisKennzahl", title="Obiskennzahl")
    richtung: Energierichtung | None = None
    wandlerfaktor: Decimal | None = Field(default=None, title="Wandlerfaktor")
    zaehlwerk_id: str | None = Field(default=None, alias="zaehlwerkId", title="Zaehlwerkid")
    vorkommastellen: int = Field(..., title="Vorkommastellen")
    nachkommastellen: int = Field(..., title="Nachkommastellen")
    schwachlastfaehig: bool = Field(..., title="Schwachlastfaehig")
    konzessionsabgaben_typ: Abgabeart | None = Field(default=None, alias="konzessionsabgabenTyp")
    active_from: datetime = Field(..., alias="activeFrom", title="Activefrom")
    active_until: datetime | None = Field(default=None, alias="activeUntil", title="Activeuntil")
    description: str | None = Field(default=None, title="Description")
    verbrauchsart: str | None = Field(default=None, title="Verbrauchsart")
