from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.energiemix import Energiemix
from ..com.externe_referenz import ExterneReferenz
from ..com.vertragskonditionen import Vertragskonditionen
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.kundentyp import Kundentyp
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.tarifmerkmal import Tarifmerkmal
from ..enum.tariftyp import Tariftyp
from .kosten import Kosten
from .marktteilnehmer import Marktteilnehmer


class Tarifkosten(BaseModel):
    """
    Objekt zur Kommunikation von Kosten, die im Rahmen der Tarifanwendung entstehen

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Tarifkosten.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifkosten JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Tarifkosten.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    anbieter: Marktteilnehmer | None = None
    anbietername: str | None = Field(default=None, title="Anbietername")
    anwendung_von: datetime | None = Field(default=None, alias="anwendungVon", title="Anwendungvon")
    bemerkung: str | None = Field(default=None, title="Bemerkung")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    bo_typ: BoTyp | None = Field(default=BoTyp.TARIFKOSTEN, alias="boTyp")
    energiemix: Energiemix | None = None
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    kosten: Kosten | None = None
    kundentypen: list[Kundentyp] | None = Field(default=None, title="Kundentypen")
    sparte: Sparte | None = None
    tarifart: Tarifart | None = None
    tarifmerkmale: list[Tarifmerkmal] | None = Field(default=None, title="Tarifmerkmale")
    tariftyp: Tariftyp | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    vertragskonditionen: Vertragskonditionen | None = None
    website: str | None = Field(default=None, title="Website")
    zeitliche_gueltigkeit: Zeitraum | None = Field(default=None, alias="zeitlicheGueltigkeit")
