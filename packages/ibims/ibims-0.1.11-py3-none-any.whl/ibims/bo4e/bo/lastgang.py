from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.zeitreihenwert import Zeitreihenwert
from ..enum.bo_typ import BoTyp
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.sparte import Sparte


class Lastgang(BaseModel):
    """
    Modell zur Abbildung eines Lastganges;
    In diesem Modell werden die Messwerte mit einem vollständigen Zeitintervall angegeben und es bietet daher eine hohe
    Flexibilität in der Übertragung jeglicher zeitlich veränderlicher Messgrössen.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Lastgang.svg" type="image/svg+xml"></object>

    .. HINT::
        `Lastgang JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Lastgang.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.LASTGANG, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    lokations_id: str | None = Field(default=None, alias="lokationsId", title="Lokationsid")
    lokationstyp: str | None = Field(default=None, title="Lokationstyp")
    messgroesse: Mengeneinheit | None = None
    obis_kennzahl: str | None = Field(default=None, alias="obisKennzahl", title="Obiskennzahl")
    sparte: Sparte | None = None
    version: str | None = Field(default=None, title="Version")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    werte: list[Zeitreihenwert] | None = Field(default=None, title="Werte")
