from pydantic import BaseModel, ConfigDict, Field

from ..enum.tarifregionskriterium import Tarifregionskriterium


class KriteriumWert(BaseModel):
    """
    Mit dieser Komponente können Kriterien und deren Werte definiert werden

    .. raw:: html

        <object data="../_static/images/bo4e/com/KriteriumWert.svg" type="image/svg+xml"></object>

    .. HINT::
        `KriteriumWert JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/KriteriumWert.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    kriterium: Tarifregionskriterium | None = None
    wert: str | None = Field(default=None, title="Wert")
