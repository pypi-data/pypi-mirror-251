from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Unterschrift(BaseModel):
    """
    Modellierung einer Unterschrift, z.B. für Verträge, Angebote etc.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Unterschrift.svg" type="image/svg+xml"></object>

    .. HINT::
        `Unterschrift JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Unterschrift.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    datum: datetime | None = Field(default=None, title="Datum")
    name: str | None = Field(default=None, title="Name")
    ort: str | None = Field(default=None, title="Ort")
