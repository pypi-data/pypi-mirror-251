from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.verbrauch import Verbrauch
from ..enum.bo_typ import BoTyp
from ..enum.lokationstyp import Lokationstyp


class Energiemenge(BaseModel):
    """
    Abbildung von Mengen, die Lokationen zugeordnet sind

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Energiemenge.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemenge JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Energiemenge.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.ENERGIEMENGE, alias="boTyp")
    energieverbrauch: list[Verbrauch] | None = Field(default=None, title="Energieverbrauch")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    lokations_id: str | None = Field(default=None, alias="lokationsId", title="Lokationsid")
    lokationstyp: Lokationstyp | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
