from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.unterschrift import Unterschrift
from ..com.vertragskonditionen import Vertragskonditionen
from ..com.vertragsteil import Vertragsteil
from ..enum.bo_typ import BoTyp
from ..enum.sparte import Sparte
from ..enum.vertragsart import Vertragsart
from ..enum.vertragsstatus import Vertragsstatus
from .geschaeftspartner import Geschaeftspartner


class Vertrag(BaseModel):
    """
    Modell für die Abbildung von Vertragsbeziehungen;
    Das Objekt dient dazu, alle Arten von Verträgen, die in der Energiewirtschaft Verwendung finden, abzubilden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Vertrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Vertrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Vertrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    beschreibung: str | None = Field(default=None, title="Beschreibung")
    bo_typ: BoTyp | None = Field(default=BoTyp.VERTRAG, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    sparte: Sparte | None = None
    unterzeichnervp1: list[Unterschrift] | None = Field(default=None, title="Unterzeichnervp1")
    unterzeichnervp2: list[Unterschrift] | None = Field(default=None, title="Unterzeichnervp2")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    vertragsart: Vertragsart | None = None
    vertragsbeginn: datetime | None = Field(default=None, title="Vertragsbeginn")
    vertragsende: datetime | None = Field(default=None, title="Vertragsende")
    vertragskonditionen: Vertragskonditionen | None = None
    vertragsnummer: str | None = Field(default=None, title="Vertragsnummer")
    vertragspartner1: Geschaeftspartner | None = None
    vertragspartner2: Geschaeftspartner | None = None
    vertragsstatus: Vertragsstatus | None = None
    vertragsteile: list[Vertragsteil] | None = Field(default=None, title="Vertragsteile")
