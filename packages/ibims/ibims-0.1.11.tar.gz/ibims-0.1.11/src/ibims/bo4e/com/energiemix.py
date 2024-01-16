from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.oekolabel import Oekolabel
from ..enum.oekozertifikat import Oekozertifikat
from ..enum.sparte import Sparte
from .energieherkunft import Energieherkunft


class Energiemix(BaseModel):
    """
    Zusammensetzung der gelieferten Energie aus den verschiedenen Primärenergieformen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Energiemix.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemix JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Energiemix.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    anteil: list[Energieherkunft] | None = Field(default=None, title="Anteil")
    atommuell: Decimal | None = Field(default=None, title="Atommuell")
    bemerkung: str | None = Field(default=None, title="Bemerkung")
    bezeichnung: str | None = Field(default=None, title="Bezeichnung")
    co2_emission: Decimal | None = Field(default=None, alias="co2Emission", title="Co2Emission")
    energieart: Sparte | None = None
    energiemixnummer: int | None = Field(default=None, title="Energiemixnummer")
    gueltigkeitsjahr: int | None = Field(default=None, title="Gueltigkeitsjahr")
    oeko_top_ten: bool | None = Field(default=None, alias="oekoTopTen", title="Oekotopten")
    oekolabel: list[Oekolabel] | None = Field(default=None, title="Oekolabel")
    oekozertifikate: list[Oekozertifikat] | None = Field(default=None, title="Oekozertifikate")
    website: str | None = Field(default=None, title="Website")
