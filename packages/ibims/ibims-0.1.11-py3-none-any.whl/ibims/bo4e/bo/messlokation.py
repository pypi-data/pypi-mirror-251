from pydantic import BaseModel, ConfigDict, Field

from ..com.adresse import Adresse
from ..com.dienstleistung import Dienstleistung
from ..com.externe_referenz import ExterneReferenz
from ..com.geokoordinaten import Geokoordinaten
from ..com.hardware import Hardware
from ..com.katasteradresse import Katasteradresse
from ..enum.bo_typ import BoTyp
from ..enum.netzebene import Netzebene
from ..enum.sparte import Sparte
from .zaehler import Zaehler


class Messlokation(BaseModel):
    """
    Object containing information about a Messlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Messlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Messlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Messlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bo_typ: BoTyp | None = Field(default=BoTyp.MESSLOKATION, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    geoadresse: Geokoordinaten | None = None
    geraete: list[Hardware] | None = Field(default=None, title="Geraete")
    grundzustaendiger_msb_codenr: str | None = Field(
        default=None, alias="grundzustaendigerMsbCodenr", title="Grundzustaendigermsbcodenr"
    )
    grundzustaendiger_msbim_codenr: str | None = Field(
        default=None, alias="grundzustaendigerMsbimCodenr", title="Grundzustaendigermsbimcodenr"
    )
    katasterinformation: Katasteradresse | None = None
    messadresse: Adresse | None = None
    messdienstleistung: list[Dienstleistung] | None = Field(default=None, title="Messdienstleistung")
    messgebietnr: str | None = Field(default=None, title="Messgebietnr")
    messlokations_id: str | None = Field(default=None, alias="messlokationsId", title="Messlokationsid")
    messlokationszaehler: list[Zaehler] | None = Field(default=None, title="Messlokationszaehler")
    netzebene_messung: Netzebene | None = Field(default=None, alias="netzebeneMessung")
    sparte: Sparte | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
