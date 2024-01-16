from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.regionskriterium import Regionskriterium
from ..enum.bo_typ import BoTyp


class Region(BaseModel):
    """
    Modellierung einer Region als Menge von Kriterien, die eine Region beschreiben

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Region.svg" type="image/svg+xml"></object>

    .. HINT::
        `Region JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Region.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    bo_typ: BoTyp | None = Field(default=BoTyp.REGION, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    negativ_liste: list[Regionskriterium] | None = Field(default=None, alias="negativListe", title="Negativliste")
    positiv_liste: list[Regionskriterium] | None = Field(default=None, alias="positivListe", title="Positivliste")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
