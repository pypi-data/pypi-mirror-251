from pydantic import BaseModel, ConfigDict, Field

from ..enum.preismodell import Preismodell
from ..enum.rechnungslegung import Rechnungslegung
from ..enum.sparte import Sparte
from ..enum.vertragsform import Vertragsform
from .ausschreibungsdetail import Ausschreibungsdetail
from .menge import Menge
from .zeitraum import Zeitraum


class Ausschreibungslos(BaseModel):
    """
    Eine Komponente zur Abbildung einzelner Lose einer Ausschreibung

    .. raw:: html

        <object data="../_static/images/bo4e/com/Ausschreibungslos.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ausschreibungslos JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Ausschreibungslos.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    anzahl_lieferstellen: int | None = Field(default=None, alias="anzahlLieferstellen", title="Anzahllieferstellen")
    bemerkung: str | None = Field(default=None, title="Bemerkung")
    betreut_durch: str | None = Field(default=None, alias="betreutDurch", title="Betreutdurch")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    energieart: Sparte | None = None
    gesamt_menge: Menge | None = Field(default=None, alias="gesamtMenge")
    lieferstellen: list[Ausschreibungsdetail] | None = Field(default=None, title="Lieferstellen")
    lieferzeitraum: Zeitraum | None = None
    losnummer: str | None = Field(default=None, title="Losnummer")
    preismodell: Preismodell | None = None
    wiederholungsintervall: Zeitraum | None = None
    wunsch_kuendingungsfrist: Zeitraum | None = Field(default=None, alias="wunschKuendingungsfrist")
    wunsch_maximalmenge: Menge | None = Field(default=None, alias="wunschMaximalmenge")
    wunsch_mindestmenge: Menge | None = Field(default=None, alias="wunschMindestmenge")
    wunsch_rechnungslegung: Rechnungslegung | None = Field(default=None, alias="wunschRechnungslegung")
    wunsch_vertragsform: Vertragsform | None = Field(default=None, alias="wunschVertragsform")
    wunsch_zahlungsziel: Zeitraum | None = Field(default=None, alias="wunschZahlungsziel")
