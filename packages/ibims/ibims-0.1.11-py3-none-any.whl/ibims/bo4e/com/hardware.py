from pydantic import BaseModel, ConfigDict, Field

from ..enum.geraetetyp import Geraetetyp


class Hardware(BaseModel):
    """
    Abbildung einer abrechenbaren Hardware

    .. raw:: html

        <object data="../_static/images/bo4e/com/Hardware.svg" type="image/svg+xml"></object>

    .. HINT::
        `Hardware JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Hardware.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    geraetetyp: Geraetetyp | None = None
