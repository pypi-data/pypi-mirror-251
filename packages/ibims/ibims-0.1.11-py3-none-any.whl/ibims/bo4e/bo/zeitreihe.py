from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.zeitreihenwert import Zeitreihenwert
from ..enum.bo_typ import BoTyp
from ..enum.medium import Medium
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.messart import Messart
from ..enum.messgroesse import Messgroesse
from ..enum.wertermittlungsverfahren import Wertermittlungsverfahren


class Zeitreihe(BaseModel):
    """
    Abbildung einer allgemeinen Zeitreihe mit einem Wertvektor.
    Die Werte können mit wahlfreier zeitlicher Distanz im Vektor abgelegt sein.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Zeitreihe.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihe JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Zeitreihe.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    beschreibung: str | None = Field(default=None, title="Beschreibung")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    bo_typ: BoTyp | None = Field(default=BoTyp.ZEITREIHE, alias="boTyp")
    einheit: Mengeneinheit | None = None
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    medium: Medium | None = None
    messart: Messart | None = None
    messgroesse: Messgroesse | None = None
    version: str | None = Field(default=None, title="Version")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    werte: list[Zeitreihenwert] | None = Field(default=None, title="Werte")
    wertherkunft: Wertermittlungsverfahren | None = None
