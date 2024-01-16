from pydantic import BaseModel, ConfigDict, Field

from ..enum.auf_abschlagstyp import AufAbschlagstyp
from ..enum.auf_abschlagsziel import AufAbschlagsziel
from ..enum.waehrungseinheit import Waehrungseinheit
from .energiemix import Energiemix
from .preisgarantie import Preisgarantie
from .regionale_preisstaffel import RegionalePreisstaffel
from .tarifeinschraenkung import Tarifeinschraenkung
from .vertragskonditionen import Vertragskonditionen
from .zeitraum import Zeitraum


class RegionalerAufAbschlag(BaseModel):
    """
    Mit dieser Komponente können Auf- und Abschläge verschiedener Typen im Zusammenhang mit regionalen Gültigkeiten
    abgebildet werden.
    Hier sind auch die Auswirkungen auf verschiedene Tarifparameter modelliert, die sich durch die Auswahl eines Auf-
    oder Abschlags ergeben.

    .. raw:: html

        <object data="../_static/images/bo4e/com/RegionalerAufAbschlag.svg" type="image/svg+xml"></object>

    .. HINT::
        `RegionalerAufAbschlag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/RegionalerAufAbschlag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    auf_abschlagstyp: AufAbschlagstyp | None = Field(default=None, alias="aufAbschlagstyp")
    auf_abschlagsziel: AufAbschlagsziel | None = Field(default=None, alias="aufAbschlagsziel")
    beschreibung: str | None = Field(default=None, title="Beschreibung")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    einheit: Waehrungseinheit | None = None
    einschraenkungsaenderung: Tarifeinschraenkung | None = None
    energiemixaenderung: Energiemix | None = None
    garantieaenderung: Preisgarantie | None = None
    gueltigkeitszeitraum: Zeitraum | None = None
    staffeln: list[RegionalePreisstaffel] | None = Field(default=None, title="Staffeln")
    tarifnamensaenderungen: str | None = Field(default=None, title="Tarifnamensaenderungen")
    vertagskonditionsaenderung: Vertragskonditionen | None = None
    voraussetzungen: list[str] | None = Field(default=None, title="Voraussetzungen")
    website: str | None = Field(default=None, title="Website")
    zusatzprodukte: list[str] | None = Field(default=None, title="Zusatzprodukte")
