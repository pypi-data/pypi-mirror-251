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
from .marktteilnehmer import Marktteilnehmer


class Tarifinfo(BaseModel):
    """
    Das BO Tarifinfo liefert die Merkmale, die einen Endkundentarif identifizierbar machen.
    Dieses BO dient als Basis für weitere BOs mit erweiterten Anwendungsmöglichkeiten.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Tarifinfo.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifinfo JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Tarifinfo.json>`_
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
    bo_typ: BoTyp | None = Field(default=BoTyp.TARIFINFO, alias="boTyp")
    energiemix: Energiemix | None = None
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    kundentypen: list[Kundentyp] | None = Field(default=None, title="Kundentypen")
    sparte: Sparte | None = None
    tarifart: Tarifart | None = None
    tarifmerkmale: list[Tarifmerkmal] | None = Field(default=None, title="Tarifmerkmale")
    tariftyp: Tariftyp | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    vertragskonditionen: Vertragskonditionen | None = None
    website: str | None = Field(default=None, title="Website")
    zeitliche_gueltigkeit: Zeitraum | None = Field(default=None, alias="zeitlicheGueltigkeit")
