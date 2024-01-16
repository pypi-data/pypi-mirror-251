from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.geraeteeigenschaften import Geraeteeigenschaften
from ..com.preisposition import Preisposition
from ..com.zeitraum import Zeitraum
from ..enum.bilanzierungsmethode import Bilanzierungsmethode
from ..enum.bo_typ import BoTyp
from ..enum.dienstleistungstyp import Dienstleistungstyp
from ..enum.netzebene import Netzebene
from ..enum.preisstatus import Preisstatus
from ..enum.sparte import Sparte
from .marktteilnehmer import Marktteilnehmer


class PreisblattMessung(BaseModel):
    """
    Variante des Preisblattmodells zur Abbildung der Preise des Messstellenbetriebs und damit verbundener Leistungen

    .. raw:: html

        <object data="../_static/images/bo4e/bo/PreisblattMessung.svg" type="image/svg+xml"></object>

    .. HINT::
        `PreisblattMessung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/PreisblattMessung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    bilanzierungsmethode: Bilanzierungsmethode | None = None
    bo_typ: BoTyp | None = Field(default=BoTyp.PREISBLATTMESSUNG, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    gueltigkeit: Zeitraum | None = None
    herausgeber: Marktteilnehmer | None = None
    inklusive_dienstleistungen: list[Dienstleistungstyp] | None = Field(
        default=None, alias="inklusiveDienstleistungen", title="Inklusivedienstleistungen"
    )
    inklusive_geraete: list[Geraeteeigenschaften] | None = Field(
        default=None, alias="inklusiveGeraete", title="Inklusivegeraete"
    )
    messebene: Netzebene | None = None
    preispositionen: list[Preisposition] | None = Field(default=None, title="Preispositionen")
    preisstatus: Preisstatus | None = None
    sparte: Sparte | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    zaehler: Geraeteeigenschaften | None = None
