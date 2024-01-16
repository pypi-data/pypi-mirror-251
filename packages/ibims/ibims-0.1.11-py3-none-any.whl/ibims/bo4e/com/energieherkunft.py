from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.erzeugungsart import Erzeugungsart


class Energieherkunft(BaseModel):
    """
    Abbildung einer Energieherkunft

    .. raw:: html

        <object data="../_static/images/bo4e/com/Energieherkunft.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energieherkunft JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Energieherkunft.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    anteil_prozent: Decimal | None = Field(default=None, alias="anteilProzent", title="Anteilprozent")
    erzeugungsart: Erzeugungsart | None = None
