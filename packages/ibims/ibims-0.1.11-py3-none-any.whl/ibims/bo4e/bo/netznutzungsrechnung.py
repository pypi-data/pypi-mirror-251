from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.betrag import Betrag
from ..com.externe_referenz import ExterneReferenz
from ..com.rechnungsposition import Rechnungsposition
from ..com.steuerbetrag import Steuerbetrag
from ..com.zeitraum import Zeitraum
from ..enum.bo_typ import BoTyp
from ..enum.nn_rechnungsart import NNRechnungsart
from ..enum.nn_rechnungstyp import NNRechnungstyp
from ..enum.rechnungsstatus import Rechnungsstatus
from ..enum.rechnungstyp import Rechnungstyp
from ..enum.sparte import Sparte
from .geschaeftspartner import Geschaeftspartner


class Netznutzungsrechnung(BaseModel):
    """
    Modell für die Abbildung von Netznutzungsrechnungen

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Netznutzungsrechnung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Netznutzungsrechnung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Netznutzungsrechnung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    absendercodenummer: str | None = Field(default=None, title="Absendercodenummer")
    bo_typ: BoTyp | None = Field(default=BoTyp.NETZNUTZUNGSRECHNUNG, alias="boTyp")
    empfaengercodenummer: str | None = Field(default=None, title="Empfaengercodenummer")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    faelligkeitsdatum: datetime | None = Field(default=None, title="Faelligkeitsdatum")
    gesamtbrutto: Betrag | None = None
    gesamtnetto: Betrag | None = None
    gesamtsteuer: Betrag | None = None
    lokations_id: str | None = Field(default=None, alias="lokationsId", title="Lokationsid")
    nnrechnungsart: NNRechnungsart | None = None
    nnrechnungstyp: NNRechnungstyp | None = None
    original: bool | None = Field(default=None, title="Original")
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
    simuliert: bool | None = Field(default=None, title="Simuliert")
    sparte: Sparte | None = None
    steuerbetraege: list[Steuerbetrag] | None = Field(default=None, title="Steuerbetraege")
    storno: bool | None = Field(default=None, title="Storno")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    vorausgezahlt: Betrag | None = None
    zuzahlen: Betrag | None = None
