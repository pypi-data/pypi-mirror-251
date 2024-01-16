from pydantic import BaseModel, ConfigDict, Field


class StandorteigenschaftenStrom(BaseModel):
    """
    Standorteigenschaften der Sparte Strom

    .. raw:: html

        <object data="../_static/images/bo4e/com/StandorteigenschaftenStrom.svg" type="image/svg+xml"></object>

    .. HINT::
        `StandorteigenschaftenStrom JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/StandorteigenschaftenStrom.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bilanzierungsgebiet_eic: str | None = Field(
        default=None, alias="bilanzierungsgebietEic", title="Bilanzierungsgebieteic"
    )
    regelzone: str | None = Field(default=None, title="Regelzone")
    regelzone_eic: str | None = Field(default=None, alias="regelzoneEic", title="Regelzoneeic")
