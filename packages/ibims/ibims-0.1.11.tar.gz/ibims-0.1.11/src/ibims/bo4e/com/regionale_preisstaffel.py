from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from .regionale_gueltigkeit import RegionaleGueltigkeit
from .sigmoidparameter import Sigmoidparameter


class RegionalePreisstaffel(BaseModel):
    """
    Abbildung einer Preisstaffel mit regionaler Abgrenzung

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionalePreisstaffel.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionalePreisstaffel JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/RegionalePreisstaffel.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    einheitspreis: Decimal | None = Field(default=None, title="Einheitspreis")
    regionale_gueltigkeit: RegionaleGueltigkeit | None = Field(default=None, alias="regionaleGueltigkeit")
    sigmoidparameter: Sigmoidparameter | None = None
    staffelgrenze_bis: Decimal | None = Field(default=None, alias="staffelgrenzeBis", title="Staffelgrenzebis")
    staffelgrenze_von: Decimal | None = Field(default=None, alias="staffelgrenzeVon", title="Staffelgrenzevon")
