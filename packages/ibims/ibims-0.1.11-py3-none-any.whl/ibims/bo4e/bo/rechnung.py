from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.betrag import Betrag
from ..com.externe_referenz import ExterneReferenz
from ..com.rechnungsposition import Rechnungsposition
from ..com.steuerbetrag import Steuerbetrag
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.rechnungsstatus import Rechnungsstatus
from ..enum.rechnungstyp import Rechnungstyp
from .geschaeftspartner import Geschaeftspartner


class Rechnung(BaseModel):
    """
    Modell für die Abbildung von Rechnungen im Kontext der Energiewirtschaft;
    Ausgehend von diesem Basismodell werden weitere spezifische Formen abgeleitet.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Rechnung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Rechnung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Rechnung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.RECHNUNG, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    faelligkeitsdatum: datetime | None = Field(default=None, title="Faelligkeitsdatum")
    gesamtbrutto: Betrag | None = None
    gesamtnetto: Betrag | None = None
    gesamtsteuer: Betrag | None = None
    original_rechnungsnummer: str | None = Field(
        default=None, alias="originalRechnungsnummer", title="Originalrechnungsnummer"
    )
    rabatt_brutto: Betrag | None = Field(default=None, alias="rabattBrutto")
    rechnungsdatum: datetime | None = Field(default=None, title="Rechnungsdatum")
    rechnungsempfaenger: Geschaeftspartner | None = None
    rechnungsersteller: Geschaeftspartner | None = None
    rechnungsnummer: str | None = Field(default=None, title="Rechnungsnummer")
    rechnungsperiode: Zeitraum | None = None
    rechnungspositionen: list[Rechnungsposition] | None = Field(default=None, title="Rechnungspositionen")
    rechnungsstatus: Rechnungsstatus | None = None
    rechnungstitel: str | None = Field(default=None, title="Rechnungstitel")
    rechnungstyp: Rechnungstyp | None = None
    steuerbetraege: list[Steuerbetrag] | None = Field(default=None, title="Steuerbetraege")
    storno: bool | None = Field(default=None, title="Storno")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    vorausgezahlt: Betrag | None = None
    zuzahlen: Betrag | None = None
    ist_selbstausgestellt: bool | None = Field(default=None, alias="istSelbstausgestellt", title="Istselbstausgestellt")
    ist_reverse_charge: bool | None = Field(default=None, alias="istReverseCharge", title="Istreversecharge")
