from pydantic import BaseModel, ConfigDict, Field

from ..com.betrag import Betrag
from ..com.externe_referenz import ExterneReferenz
from ..com.kostenblock import Kostenblock
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kostenklasse import Kostenklasse


class Kosten(BaseModel):
    """
    Dieses BO wird zur Übertagung von hierarchischen Kostenstrukturen verwendet.
    Die Kosten werden dabei in Kostenblöcke und diese wiederum in Kostenpositionen strukturiert.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Kosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Kosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.KOSTEN, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    gueltigkeit: Zeitraum | None = None
    kostenbloecke: list[Kostenblock] | None = Field(default=None, title="Kostenbloecke")
    kostenklasse: Kostenklasse | None = None
    summe_kosten: list[Betrag] | None = Field(default=None, alias="summeKosten", title="Summekosten")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
