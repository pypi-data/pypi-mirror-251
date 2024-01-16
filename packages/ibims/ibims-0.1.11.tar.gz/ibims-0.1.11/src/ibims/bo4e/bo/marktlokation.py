from pydantic import BaseModel, ConfigDict, Field

from ..com.adresse import Adresse
from ..com.externe_referenz import ExterneReferenz
from ..com.geokoordinaten import Geokoordinaten
from ..com.katasteradresse import Katasteradresse
from ..com.messlokationszuordnung import Messlokationszuordnung
from ..enum.bilanzierungsmethode import Bilanzierungsmethode
from ..enum.bo_typ import BoTyp
from ..enum.energierichtung import Energierichtung
from ..enum.gasqualitaet import Gasqualitaet
from ..enum.gebiettyp import Gebiettyp
from ..enum.kundentyp import Kundentyp
from ..enum.marktgebiet import Marktgebiet
from ..enum.messtechnische_einordnung import MesstechnischeEinordnung
from ..enum.netzebene import Netzebene
from ..enum.profiltyp import Profiltyp
from ..enum.prognosegrundlage import Prognosegrundlage
from ..enum.regelzone import Regelzone
from ..enum.sparte import Sparte
from ..enum.variant import Variant
from ..enum.verbrauchsart import Verbrauchsart
from .geschaeftspartner import Geschaeftspartner


class Marktlokation(BaseModel):
    """
    Object containing information about a Marktlokation

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Marktlokation.svg" type="image/svg+xml"></object>

    .. HINT::
        `Marktlokation JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Marktlokation.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    bilanzierungsgebiet: str | None = Field(default=None, title="Bilanzierungsgebiet")
    bilanzierungsmethode: Bilanzierungsmethode | None = None
    bo_typ: BoTyp | None = Field(default=BoTyp.MARKTLOKATION, alias="boTyp")
    endkunde: Geschaeftspartner | None = None
    energierichtung: Energierichtung | None = None
    externe_referenzen: list[ExterneReferenz] | None = Field(
        default=None, alias="externeReferenzen", title="Externereferenzen"
    )
    gasqualitaet: Gasqualitaet | None = None
    gebietstyp: Gebiettyp | None = None
    geoadresse: Geokoordinaten | None = None
    grundversorgercodenr: str | None = Field(default=None, title="Grundversorgercodenr")
    katasterinformation: Katasteradresse | None = None
    kundengruppen: list[Kundentyp] | None = Field(default=None, title="Kundengruppen")
    lokationsadresse: Adresse | None = None
    marktlokations_id: str | None = Field(default=None, alias="marktlokationsId", title="Marktlokationsid")
    netzbetreibercodenr: str | None = Field(default=None, title="Netzbetreibercodenr")
    netzebene: Netzebene | None = None
    netzgebietsnr: str | None = Field(default=None, title="Netzgebietsnr")
    sparte: Sparte | None = None
    unterbrechbar: bool | None = Field(default=None, title="Unterbrechbar")
    verbrauchsart: Verbrauchsart | None = None
    versionstruktur: str | None = Field(default="2", title="Versionstruktur")
    zugehoerige_messlokation: Messlokationszuordnung | None = Field(default=None, alias="zugehoerigeMesslokation")
    messtechnische_einordnung: MesstechnischeEinordnung = Field(..., alias="messtechnischeEinordnung")
    uebertragungsnetzgebiet: Regelzone | None = None
    marktgebiet: Marktgebiet | None = None
    variant: Variant
    community_id: str = Field(..., alias="communityId", title="Communityid")
    prognose_grundlage: Prognosegrundlage | None = Field(default=None, alias="prognoseGrundlage")
    prognose_grundlage_detail: Profiltyp | None = Field(default=None, alias="prognoseGrundlageDetail")
