from pydantic import BaseModel, ConfigDict, Field

from .marktgebiet_info import MarktgebietInfo


class StandorteigenschaftenGas(BaseModel):
    """
    Standorteigenschaften der Sparte Gas

    .. raw:: html

        <object data="../_static/images/bo4e/com/StandorteigenschaftenGas.svg" type="image/svg+xml"></object>

    .. HINT::
        `StandorteigenschaftenGas JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/StandorteigenschaftenGas.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    marktgebiete: list[MarktgebietInfo] | None = Field(default=None, title="Marktgebiete")
    netzkontonummern: list[str] | None = Field(default=None, title="Netzkontonummern")
