from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..enum.anrede import Anrede
from ..enum.bo_typ import BoTyp
from ..enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from ..enum.kontaktart import Kontaktart


class Geschaeftspartner(BaseModel):
    """
    Mit diesem Objekt können Geschäftspartner übertragen werden.
    Sowohl Unternehmen, als auch Privatpersonen können Geschäftspartner sein.
    Hinweis: Marktteilnehmer haben ein eigenes BO, welches sich von diesem BO ableitet.
    Hier sollte daher keine Zuordnung zu Marktrollen erfolgen.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Geschaeftspartner.svg" type="image/svg+xml"></object>

    .. HINT::
        `Geschaeftspartner JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Geschaeftspartner.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    amtsgericht: str | None = Field(default=None, title="Amtsgericht")
    anrede: Anrede | None = None
    bo_typ: BoTyp | None = Field(default=BoTyp.GESCHAEFTSPARTNER, alias="boTyp")
    e_mail_adresse: str | None = Field(default=None, alias="eMailAdresse", title="Emailadresse")
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    geschaeftspartnerrolle: list[Geschaeftspartnerrolle] | None = Field(default=None, title="Geschaeftspartnerrolle")
    gewerbekennzeichnung: bool | None = Field(default=None, title="Gewerbekennzeichnung")
    glaeubiger_id: str | None = Field(default=None, alias="glaeubigerId", title="Glaeubigerid")
    hrnummer: str | None = Field(default=None, title="Hrnummer")
    kontaktweg: list[Kontaktart] | None = Field(default=None, title="Kontaktweg")
    name1: str | None = Field(default=None, title="Name1")
    name2: str | None = Field(default=None, title="Name2")
    name3: str | None = Field(default=None, title="Name3")
    partneradresse: Adresse | None = None
    umsatzsteuer_id: str | None = Field(default=None, alias="umsatzsteuerId", title="Umsatzsteuerid")
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    website: str | None = Field(default=None, title="Website")
    erstellungsdatum: datetime | None = Field(default=None, title="Erstellungsdatum")
    geburtstag: datetime | None = Field(default=None, title="Geburtstag")
    telefonnummer_mobil: str | None = Field(default=None, alias="telefonnummerMobil", title="Telefonnummermobil")
    telefonnummer_privat: str | None = Field(default=None, alias="telefonnummerPrivat", title="Telefonnummerprivat")
    telefonnummer_geschaeft: str | None = Field(
        default=None, alias="telefonnummerGeschaeft", title="Telefonnummergeschaeft"
    )
    firmenname: str | None = Field(default=None, title="Firmenname")
    hausbesitzer: bool | None = Field(default=None, title="Hausbesitzer")
