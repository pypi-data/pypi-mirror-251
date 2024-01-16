from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.steuerkennzeichen import Steuerkennzeichen
from ..enum.waehrungscode import Waehrungscode


class Steuerbetrag(BaseModel):
    """
    Abbildung eines Steuerbetrages.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Steuerbetrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Steuerbetrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Steuerbetrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    basiswert: Decimal | None = Field(default=None, title="Basiswert")
    steuerkennzeichen: Steuerkennzeichen | None = None
    steuerwert: Decimal | None = Field(default=None, title="Steuerwert")
    waehrung: Waehrungscode | None = None
    steuerwert_vorausgezahlt: Decimal | None = Field(
        default=None, alias="steuerwertVorausgezahlt", title="Steuerwertvorausgezahlt"
    )
