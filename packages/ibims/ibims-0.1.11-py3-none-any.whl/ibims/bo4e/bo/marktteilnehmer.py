from pydantic import BaseModel, ConfigDict, Field

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..enum.anrede import Anrede
from ..enum.bo_typ import BoTyp
from ..enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from ..enum.kontaktart import Kontaktart
from ..enum.marktrolle import Marktrolle
from ..enum.rollencodetyp import Rollencodetyp
from ..enum.sparte import Sparte


class Marktteilnehmer(BaseModel):
    """
    Objekt zur Aufnahme der Information zu einem Marktteilnehmer

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Marktteilnehmer.svg" type="image/svg+xml"></object>

    .. HINT::
        `Marktteilnehmer JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Marktteilnehmer.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    amtsgericht: str | None = Field(default=None, title="Amtsgericht")
    anrede: Anrede | None = None
    bo_typ: BoTyp | None = Field(default=BoTyp.MARKTTEILNEHMER, alias="boTyp")
    e_mail_adresse: str | None = Field(default=None, alias="eMailAdresse", title="Emailadresse")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    geschaeftspartnerrolle: list[Geschaeftspartnerrolle] | None = Field(default=None, title="Geschaeftspartnerrolle")
    gewerbekennzeichnung: bool | None = Field(default=None, title="Gewerbekennzeichnung")
    glaeubiger_id: str | None = Field(default=None, alias="glaeubigerId", title="Glaeubigerid")
    hrnummer: str | None = Field(default=None, title="Hrnummer")
    kontaktweg: list[Kontaktart] | None = Field(default=None, title="Kontaktweg")
    makoadresse: str | None = Field(default=None, title="Makoadresse")
    marktrolle: Marktrolle | None = None
    name1: str | None = Field(default=None, title="Name1")
    name2: str | None = Field(default=None, title="Name2")
    name3: str | None = Field(default=None, title="Name3")
    partneradresse: Adresse | None = None
    rollencodenummer: str | None = Field(default=None, title="Rollencodenummer")
    rollencodetyp: Rollencodetyp | None = None
    sparte: Sparte | None = None
    umsatzsteuer_id: str | None = Field(default=None, alias="umsatzsteuerId", title="Umsatzsteuerid")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    website: str | None = Field(default=None, title="Website")
