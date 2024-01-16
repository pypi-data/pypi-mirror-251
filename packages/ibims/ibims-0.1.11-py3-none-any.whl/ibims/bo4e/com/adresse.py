from pydantic import BaseModel, ConfigDict, Field

from ..enum.landescode import Landescode


class Adresse(BaseModel):
    """
    Contains an address that can be used for most purposes.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Adresse.svg" type="image/svg+xml"></object>

    .. HINT::
        `Adresse JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Adresse.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    adresszusatz: str | None = Field(default=None, title="Adresszusatz")
    co_ergaenzung: str | None = Field(default=None, alias="coErgaenzung", title="Coergaenzung")
    hausnummer: str | None = Field(default=None, title="Hausnummer")
    landescode: Landescode | None = Landescode.DE
    ort: str | None = Field(default=None, title="Ort")
    ortsteil: str | None = Field(default=None, title="Ortsteil")
    postfach: str | None = Field(default=None, title="Postfach")
    postleitzahl: str | None = Field(default=None, title="Postleitzahl")
    strasse: str | None = Field(default=None, title="Strasse")
