from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .betrag import Betrag
from .menge import Menge
from .preis import Preis


class Fremdkostenposition(BaseModel):
    """
    Eine Kostenposition im Bereich der Fremdkosten

    .. raw:: html

        <object data="../_static/images/bo4e/com/Fremdkostenposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Fremdkostenposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Fremdkostenposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    artikelbezeichnung: str | None = Field(default=None, title="Artikelbezeichnung")
    artikeldetail: str | None = Field(default=None, title="Artikeldetail")
    betrag_kostenposition: Betrag | None = Field(default=None, alias="betragKostenposition")
    bis: datetime | None = Field(default=None, title="Bis")
    einzelpreis: Preis | None = None
    gebietcode_eic: str | None = Field(default=None, alias="gebietcodeEic", title="Gebietcodeeic")
    link_preisblatt: str | None = Field(default=None, alias="linkPreisblatt", title="Linkpreisblatt")
    marktpartnercode: str | None = Field(default=None, title="Marktpartnercode")
    marktpartnername: str | None = Field(default=None, title="Marktpartnername")
    menge: Menge | None = None
    positionstitel: str | None = Field(default=None, title="Positionstitel")
    von: datetime | None = Field(default=None, title="Von")
    zeitmenge: Menge | None = None
