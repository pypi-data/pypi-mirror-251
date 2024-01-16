from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.angebotsvariante import Angebotsvariante
from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp
from ..enum.sparte import Sparte
from .ansprechpartner import Ansprechpartner
from .geschaeftspartner import Geschaeftspartner


class Angebot(BaseModel):
    """
    Mit diesem BO kann ein Versorgungsangebot zur Strom- oder Gasversorgung oder die Teilnahme an einer Ausschreibung
    übertragen werden. Es können verschiedene Varianten enthalten sein (z.B. ein- und mehrjährige Laufzeit).
    Innerhalb jeder Variante können Teile enthalten sein, die jeweils für eine oder mehrere Marktlokationen erstellt
    werden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Angebot.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebot JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Angebot.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    anfragereferenz: str | None = Field(default=None, title="Anfragereferenz")
    angebotsdatum: datetime | None = Field(default=None, title="Angebotsdatum")
    angebotsgeber: Geschaeftspartner | None = None
    angebotsnehmer: Geschaeftspartner | None = None
    angebotsnummer: str | None = Field(default=None, title="Angebotsnummer")
    bindefrist: datetime | None = Field(default=None, title="Bindefrist")
    bo_typ: BoTyp | None = Field(default=BoTyp.ANGEBOT, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    sparte: Sparte | None = None
    unterzeichner_angebotsgeber: Ansprechpartner | None = Field(default=None, alias="unterzeichnerAngebotsgeber")
    unterzeichner_angebotsnehmer: Ansprechpartner | None = Field(default=None, alias="unterzeichnerAngebotsnehmer")
    varianten: list[Angebotsvariante] | None = Field(default=None, title="Varianten")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
