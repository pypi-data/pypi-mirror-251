from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.messpreistyp import Messpreistyp
from ..enum.tarifkalkulationsmethode import Tarifkalkulationsmethode
from .preis import Preis
from .tarifpreis import Tarifpreis


class Tarifberechnungsparameter(BaseModel):
    """
    In dieser Komponente sind die Berechnungsparameter für die Ermittlung der Tarifkosten zusammengefasst.
    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifberechnungsparameter.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifberechnungsparameter JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifberechnungsparameter.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    berechnungsmethode: Tarifkalkulationsmethode | None = None
    hoechstpreis_ht: Preis | None = Field(default=None, alias="hoechstpreisHT")
    hoechstpreis_nt: Preis | None = Field(default=None, alias="hoechstpreisNT")
    kw_inklusive: Decimal | None = Field(default=None, alias="kwInklusive", title="Kwinklusive")
    kw_weitere_mengen: Decimal | None = Field(default=None, alias="kwWeitereMengen", title="Kwweiteremengen")
    messpreis_beruecksichtigen: bool | None = Field(
        default=None, alias="messpreisBeruecksichtigen", title="Messpreisberuecksichtigen"
    )
    messpreis_in_gp_enthalten: bool | None = Field(
        default=None, alias="messpreisInGpEnthalten", title="Messpreisingpenthalten"
    )
    messpreistyp: Messpreistyp | None = None
    mindestpreis: Preis | None = None
    zusatzpreise: list[Tarifpreis] | None = Field(default=None, title="Zusatzpreise")
