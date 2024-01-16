from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.ausschreibungslos import Ausschreibungslos
from ..com.externe_referenz import ExterneReferenz
from ..com.zeitraum import Zeitraum
from ..enum.ausschreibungsportal import Ausschreibungsportal
from ..enum.ausschreibungsstatus import Ausschreibungsstatus
from ..enum.ausschreibungstyp import Ausschreibungstyp
from ..enum.bo_typ import BoTyp
from .geschaeftspartner import Geschaeftspartner


class Ausschreibung(BaseModel):
    """
    Das BO Ausschreibung dient zur detaillierten Darstellung von ausgeschriebenen Energiemengen in der Energiewirtschaft

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Ausschreibung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Ausschreibung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    abgabefrist: Zeitraum | None = None
    ausschreibender: Geschaeftspartner | None = None
    ausschreibungportal: Ausschreibungsportal | None = None
    ausschreibungsnummer: str | None = Field(default=None, title="Ausschreibungsnummer")
    ausschreibungsstatus: Ausschreibungsstatus | None = None
    ausschreibungstyp: Ausschreibungstyp | None = None
    bindefrist: Zeitraum | None = None
    bo_typ: BoTyp | None = Field(default=BoTyp.AUSSCHREIUNG, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    kostenpflichtig: bool | None = Field(default=None, title="Kostenpflichtig")
    lose: list[Ausschreibungslos] | None = Field(default=None, title="Lose")
    veroeffentlichungszeitpunkt: datetime | None = Field(default=None, title="Veroeffentlichungszeitpunkt")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    webseite: str | None = Field(default=None, title="Webseite")
