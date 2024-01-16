from pydantic import BaseModel, ConfigDict, Field

from .tarifpreisstaffel_pro_ort import TarifpreisstaffelProOrt


class TarifpreispositionProOrt(BaseModel):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen abgebildet werden

    .. raw:: html

        <object data="../_static/images/bo4e/com/TarifpreispositionProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `TarifpreispositionProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/TarifpreispositionProOrt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    netznr: str | None = Field(default=None, title="Netznr")
    ort: str | None = Field(default=None, title="Ort")
    postleitzahl: str | None = Field(default=None, title="Postleitzahl")
    preisstaffeln: list[TarifpreisstaffelProOrt] | None = Field(default=None, title="Preisstaffeln")
