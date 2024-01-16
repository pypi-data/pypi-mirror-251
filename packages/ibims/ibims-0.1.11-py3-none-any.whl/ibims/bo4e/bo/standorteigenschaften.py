from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.standorteigenschaften_gas import StandorteigenschaftenGas
from ..com.standorteigenschaften_strom import StandorteigenschaftenStrom
from ..enum.bo_typ import BoTyp


class Standorteigenschaften(BaseModel):
    """
    Modelliert die regionalen und spartenspezifischen Eigenschaften einer gegebenen Adresse.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Standorteigenschaften.svg" type="image/svg+xml"></object>

    .. HINT::
        `Standorteigenschaften JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Standorteigenschaften.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.STANDORTEIGENSCHAFTEN, alias="boTyp")
    eigenschaften_gas: StandorteigenschaftenGas | None = Field(default=None, alias="eigenschaftenGas")
    eigenschaften_strom: list[StandorteigenschaftenStrom] | None = Field(
        default=None, alias="eigenschaftenStrom", title="Eigenschaftenstrom"
    )
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
