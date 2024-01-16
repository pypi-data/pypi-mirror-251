from pydantic import BaseModel, ConfigDict, Field

from ..enum.dienstleistungstyp import Dienstleistungstyp


class Dienstleistung(BaseModel):
    """
    Abbildung einer abrechenbaren Dienstleistung.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Dienstleistung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Dienstleistung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Dienstleistung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    dienstleistungstyp: Dienstleistungstyp | None = None
