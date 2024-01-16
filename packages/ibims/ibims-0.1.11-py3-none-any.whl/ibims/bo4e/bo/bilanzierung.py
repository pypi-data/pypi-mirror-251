from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..com.lastprofil import Lastprofil
from ..enum.aggregationsverantwortung import Aggregationsverantwortung
from ..enum.bo_typ import BoTyp
from ..enum.profiltyp import Profiltyp
from ..enum.prognosegrundlage import Prognosegrundlage


class Bilanzierung(BaseModel):
    """
    Bilanzierung is a business object used for balancing. This object is no BO4E standard and a complete go
    implementation can be found at
    https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/bo/bilanzierung.go
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    bo_typ: BoTyp | None = Field(default="BILANZIERUNG", alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bilanzierungsbeginn: datetime = Field(..., title="Bilanzierungsbeginn")
    bilanzierungsende: datetime = Field(..., title="Bilanzierungsende")
    bilanzkreis: str | None = Field(default=None, title="Bilanzkreis")
    aggregationsverantwortung: Aggregationsverantwortung | None = None
    lastprofile: list[Lastprofil] | None = Field(default=None, title="Lastprofile")
    prognosegrundlage: Prognosegrundlage | None = None
    details_prognosegrundlage: Profiltyp | None = Field(default=None, alias="detailsPrognosegrundlage")
