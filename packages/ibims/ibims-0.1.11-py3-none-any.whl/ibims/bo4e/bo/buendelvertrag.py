from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.unterschrift import Unterschrift
from ..com.vertragskonditionen import Vertragskonditionen
from ..enum.bo_typ import BoTyp
from ..enum.sparte import Sparte
from ..enum.vertragsart import Vertragsart
from ..enum.vertragsstatus import Vertragsstatus
from .geschaeftspartner import Geschaeftspartner
from .vertrag import Vertrag


class Buendelvertrag(BaseModel):
    """
    Abbildung eines Bündelvertrags.
    Es handelt sich hierbei um eine Liste von Einzelverträgen, die in einem Vertragsobjekt gebündelt sind.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Buendelvertrag.svg" type="image/svg+xml"></object>

    .. HINT::
        `Buendelvertrag JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Buendelvertrag.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    beschreibung: str | None = Field(default=None, title="Beschreibung")
    bo_typ: BoTyp | None = Field(default=BoTyp.BUENDELVERTRAG, alias="boTyp")
    einzelvertraege: list[Vertrag] | None = Field(default=None, title="Einzelvertraege")
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
    vertragskonditionen: list[Vertragskonditionen] | None = Field(default=None, title="Vertragskonditionen")
    vertragsnummer: str | None = Field(default=None, title="Vertragsnummer")
    vertragspartner1: Geschaeftspartner | None = None
    vertragspartner2: Geschaeftspartner | None = None
    vertragsstatus: Vertragsstatus | None = None
