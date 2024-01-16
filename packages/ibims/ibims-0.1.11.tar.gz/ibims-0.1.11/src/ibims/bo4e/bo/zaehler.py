from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.zaehlwerk import Zaehlwerk
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.messwerterfassung import Messwerterfassung
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.zaehlerauspraegung import Zaehlerauspraegung
from ..enum.zaehlertyp import Zaehlertyp
from .geschaeftspartner import Geschaeftspartner


class Zaehler(BaseModel):
    """
    Object containing information about a meter/"Zaehler".

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Zaehler.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zaehler JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Zaehler.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.ZAEHLER, alias="boTyp")
    eichung_bis: datetime | None = Field(default=None, alias="eichungBis", title="Eichungbis")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    letzte_eichung: datetime | None = Field(default=None, alias="letzteEichung", title="Letzteeichung")
    sparte: Sparte | None = None
    tarifart: Tarifart | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    zaehlerauspraegung: Zaehlerauspraegung | None = None
    zaehlerhersteller: Geschaeftspartner | None = None
    zaehlerkonstante: Decimal | None = Field(default=None, title="Zaehlerkonstante")
    zaehlernummer: str | None = Field(default=None, title="Zaehlernummer")
    zaehlertyp: Zaehlertyp | None = None
    zaehlwerke: list[Zaehlwerk] | None = Field(default=None, title="Zaehlwerke")
    messwerterfassung: Messwerterfassung
    nachstes_ablesedatum: datetime | None = Field(
        default=None, alias="nachstesAblesedatum", title="Nachstesablesedatum"
    )
    aktiver_zeitraum: Zeitraum | None = Field(default=None, alias="aktiverZeitraum")
