from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp
from ..enum.hinweis_thema import HinweisThema


class Hinweis(BaseModel):
    """
    Contains specific hints for the handling of contracts and customers.
    Hints are meant to be read and written by agents or customer service employees.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    bo_typ: BoTyp | None = Field(default=BoTyp.GESCHAEFTSOBJEKT, alias="boTyp")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    erstellungsdatum: datetime = Field(..., title="Erstellungsdatum")
    thema: HinweisThema | str = Field(..., title="Thema")
    nachricht: str = Field(..., title="Nachricht")
