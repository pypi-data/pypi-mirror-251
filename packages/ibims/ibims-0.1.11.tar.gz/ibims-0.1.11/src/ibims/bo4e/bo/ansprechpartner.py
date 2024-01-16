from pydantic import BaseModel, ConfigDict, Field

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..com.rufnummer import Rufnummer
from ..com.zustaendigkeit import Zustaendigkeit
from ..enum.anrede import Anrede
from ..enum.bo_typ import BoTyp
from ..enum.titel import Titel
from .geschaeftspartner import Geschaeftspartner


class Ansprechpartner(BaseModel):
    """
    Object containing information about a Ansprechpartner

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Ansprechpartner.svg" type="image/svg+xml"></object>

    .. HINT::
        `Ansprechpartner JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Ansprechpartner.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    adresse: Adresse | None = None
    anrede: Anrede | None = None
    bo_typ: BoTyp | None = Field(default=BoTyp.ANSPRECHPARTNER, alias="boTyp")
    e_mail_adresse: str | None = Field(default=None, alias="eMailAdresse", title="Emailadresse")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    geschaeftspartner: Geschaeftspartner | None = None
    individuelle_anrede: str | None = Field(default=None, alias="individuelleAnrede", title="Individuelleanrede")
    kommentar: str | None = Field(default=None, title="Kommentar")
    nachname: str | None = Field(default=None, title="Nachname")
    rufnummer: Rufnummer | None = None
    titel: Titel | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    vorname: str | None = Field(default=None, title="Vorname")
    zustaendigkeit: Zustaendigkeit | None = None
