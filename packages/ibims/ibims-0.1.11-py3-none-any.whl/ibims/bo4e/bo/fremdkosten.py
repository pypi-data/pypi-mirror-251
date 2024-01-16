from pydantic import BaseModel, ConfigDict, Field

from ..com.betrag import Betrag
from ..com.externe_referenz import ExterneReferenz
from ..com.fremdkostenblock import Fremdkostenblock
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp


class Fremdkosten(BaseModel):
    """
    Mit diesem BO werden die Fremdkosten, beispielsweise für eine Angebotserstellung oder eine Rechnungsprüfung,
    übertragen.
    Die Fremdkosten enthalten dabei alle Kostenblöcke, die von anderen Marktteilnehmern oder Instanzen erhoben werden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Fremdkosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Fremdkosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Fremdkosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.FREMDKOSTEN, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    gueltigkeit: Zeitraum | None = None
    kostenbloecke: list[Fremdkostenblock] | None = Field(default=None, title="Kostenbloecke")
    summe_kosten: Betrag | None = Field(default=None, alias="summeKosten")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
