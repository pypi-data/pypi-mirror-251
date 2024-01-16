from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.tagesvektor import Tagesvektor
from ..com.zeitintervall import Zeitintervall
from ..enum.bo_typ import BoTyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.sparte import Sparte


class LastgangKompakt(BaseModel):
    """
    Modell zur Abbildung eines kompakten Lastganges.
    In diesem Modell werden die Messwerte in Form von Tagesvektoren mit fester Anzahl von Werten übertragen.
    Daher ist dieses BO nur zur Übertragung von äquidistanten Messwertverläufen geeignet.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.LASTGANG_KOMPAKT, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    lokations_id: str | None = Field(default=None, alias="lokationsId", title="Lokationsid")
    lokationstyp: str | None = Field(default=None, title="Lokationstyp")
    messgroesse: Mengeneinheit | None = None
    obis_kennzahl: str | None = Field(default=None, alias="obisKennzahl", title="Obiskennzahl")
    sparte: Sparte | None = None
    tagesvektoren: list[Tagesvektor] | None = Field(default=None, title="Tagesvektoren")
    version: str | None = Field(default=None, title="Version")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    zeitintervall: Zeitintervall | None = None
