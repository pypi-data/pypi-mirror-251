from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.bdew_artikelnummer import BDEWArtikelnummer
from ..enum.bemessungsgroesse import Bemessungsgroesse
from ..enum.kalkulationsmethode import Kalkulationsmethode
from ..enum.leistungstyp import Leistungstyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.steuerkennzeichen import Steuerkennzeichen
from ..enum.tarifzeit import Tarifzeit
from ..enum.waehrungseinheit import Waehrungseinheit
from ..enum.zeiteinheit import Zeiteinheit
from .preisstaffel import Preisstaffel


class Preisposition(BaseModel):
    """
    Preis für eine definierte Lieferung oder Leistung innerhalb eines Preisblattes

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Preisposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bdew_artikelnummer: BDEWArtikelnummer | None = Field(default=None, alias="bdewArtikelnummer")
    berechnungsmethode: Kalkulationsmethode | None = None
    bezugsgroesse: Mengeneinheit | None = None
    freimenge_blindarbeit: Decimal | None = Field(
        default=None, alias="freimengeBlindarbeit", title="Freimengeblindarbeit"
    )
    freimenge_leistungsfaktor: Decimal | None = Field(
        default=None, alias="freimengeLeistungsfaktor", title="Freimengeleistungsfaktor"
    )
    gruppenartikel_id: str | None = Field(default=None, alias="gruppenartikelId", title="Gruppenartikelid")
    leistungsbezeichnung: str | None = Field(default=None, title="Leistungsbezeichnung")
    leistungstyp: Leistungstyp | None = None
    preiseinheit: Waehrungseinheit | None = None
    preisstaffeln: list[Preisstaffel] | None = Field(default=None, title="Preisstaffeln")
    tarifzeit: Tarifzeit | None = None
    zeitbasis: Zeiteinheit | None = None
    zonungsgroesse: Bemessungsgroesse | None = None
    steuersatz: Steuerkennzeichen
