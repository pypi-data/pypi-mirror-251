from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..enum.bdew_artikelnummer import BDEWArtikelnummer
from ..enum.zeiteinheit import Zeiteinheit
from .betrag import Betrag
from .menge import Menge
from .preis import Preis
from .steuerbetrag import Steuerbetrag


class Rechnungsposition(BaseModel):
    """
    Über Rechnungspositionen werden Rechnungen strukturiert.
    In einem Rechnungsteil wird jeweils eine in sich geschlossene Leistung abgerechnet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Rechnungsposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Rechnungsposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Rechnungsposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    artikel_id: str | None = Field(default=None, alias="artikelId", title="Artikelid")
    artikelnummer: BDEWArtikelnummer | None = None
    einzelpreis: Preis | None = None
    lieferung_bis: datetime | None = Field(default=None, alias="lieferungBis", title="Lieferungbis")
    lieferung_von: datetime | None = Field(default=None, alias="lieferungVon", title="Lieferungvon")
    lokations_id: str | None = Field(default=None, alias="lokationsId", title="Lokationsid")
    positions_menge: Menge | None = Field(default=None, alias="positionsMenge")
    positionsnummer: int | None = Field(default=None, title="Positionsnummer")
    positionstext: str | None = Field(default=None, title="Positionstext")
    teilrabatt_netto: Betrag | None = Field(default=None, alias="teilrabattNetto")
    teilsumme_netto: Betrag | None = Field(default=None, alias="teilsummeNetto")
    teilsumme_steuer: Steuerbetrag | None = Field(default=None, alias="teilsummeSteuer")
    zeitbezogene_menge: Menge | None = Field(default=None, alias="zeitbezogeneMenge")
    zeiteinheit: Zeiteinheit | None = None
