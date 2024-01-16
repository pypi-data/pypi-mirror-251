from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .menge import Menge


class Vertragsteil(BaseModel):
    """
    Abbildung für einen Vertragsteil. Der Vertragsteil wird dazu verwendet,
    eine vertragliche Leistung in Bezug zu einer Lokation (Markt- oder Messlokation) festzulegen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Vertragsteil.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertragsteil JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Vertragsteil.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    lokation: str | None = Field(default=None, title="Lokation")
    maximale_abnahmemenge: Menge | None = Field(default=None, alias="maximaleAbnahmemenge")
    minimale_abnahmemenge: Menge | None = Field(default=None, alias="minimaleAbnahmemenge")
    vertraglich_fixierte_menge: Menge | None = Field(default=None, alias="vertraglichFixierteMenge")
    vertragsteilbeginn: datetime | None = Field(default=None, title="Vertragsteilbeginn")
    vertragsteilende: datetime | None = Field(default=None, title="Vertragsteilende")
