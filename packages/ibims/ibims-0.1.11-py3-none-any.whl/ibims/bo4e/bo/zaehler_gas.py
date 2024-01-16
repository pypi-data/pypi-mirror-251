from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.zaehlwerk import Zaehlwerk
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.geraetemerkmal import Geraetemerkmal
from ..enum.messwerterfassung import Messwerterfassung
from ..enum.netzebene import Netzebene
from ..enum.sparte import Sparte
from ..enum.tarifart import Tarifart
from ..enum.zaehlerauspraegung import Zaehlerauspraegung
from ..enum.zaehlertyp import Zaehlertyp
from .geschaeftspartner import Geschaeftspartner


class ZaehlerGas(BaseModel):
    """
    Resolve some ambiguity of `Strom` and `Gas`
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    bo_typ: BoTyp | None = Field(default=BoTyp.ZAEHLER, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    zaehlernummer: str | None = Field(default=None, title="Zaehlernummer")
    sparte: Sparte | None = None
    zaehlerauspraegung: Zaehlerauspraegung | None = None
    zaehlertyp: Zaehlertyp
    zaehlwerke: list[Zaehlwerk] | None = Field(default=None, title="Zaehlwerke")
    tarifart: Tarifart | None = None
    zaehlerkonstante: Decimal | None = Field(default=None, title="Zaehlerkonstante")
    eichung_bis: datetime | None = Field(default=None, alias="eichungBis", title="Eichungbis")
    letzte_eichung: datetime | None = Field(default=None, alias="letzteEichung", title="Letzteeichung")
    zaehlerhersteller: Geschaeftspartner | None = None
    messwerterfassung: Messwerterfassung
    nachstes_ablesedatum: datetime | None = Field(
        default=None, alias="nachstesAblesedatum", title="Nachstesablesedatum"
    )
    aktiver_zeitraum: Zeitraum | None = Field(default=None, alias="aktiverZeitraum")
    zaehlergroesse: Geraetemerkmal
    druckniveau: Netzebene
