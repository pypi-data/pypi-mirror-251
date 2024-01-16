from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .zeitreihenwertkompakt import Zeitreihenwertkompakt


class Tagesvektor(BaseModel):
    """
    Abbildung eines Tagesvektors eines beliebigen äquidistanten Zeitrasters

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tagesvektor.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tagesvektor JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tagesvektor.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    tag: datetime | None = Field(default=None, title="Tag")
    werte: list[Zeitreihenwertkompakt] | None = Field(default=None, title="Werte")
