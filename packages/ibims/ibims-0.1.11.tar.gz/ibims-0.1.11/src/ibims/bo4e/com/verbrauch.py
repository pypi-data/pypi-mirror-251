from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..enum.ablesende_rolle import AblesendeRolle
from ..enum.ablesungsstatus import Ablesungsstatus
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.messwertstatus import Messwertstatus
from ..enum.wertermittlungsverfahren import Wertermittlungsverfahren


class Verbrauch(BaseModel):
    """
    Abbildung eines zeitlich abgegrenzten Verbrauchs

    .. raw:: html

        <object data="../_static/images/bo4e/com/Verbrauch.svg" type="image/svg+xml"></object>

    .. HINT::
        `Verbrauch JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Verbrauch.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: str | None = Field(default=None, alias="_id", title=" Id")
    einheit: Mengeneinheit | None = None
    enddatum: datetime | None = Field(default=None, title="Enddatum")
    obis_kennzahl: str | None = Field(default=None, alias="obisKennzahl", title="Obiskennzahl")
    startdatum: datetime | None = Field(default=None, title="Startdatum")
    wert: Decimal | None = Field(default=None, title="Wert")
    wertermittlungsverfahren: Wertermittlungsverfahren | None = None
    ablesegrund: str | None = Field(default=None, title="Ablesegrund")
    ablesebeschreibung: str | None = Field(default=None, title="Ablesebeschreibung")
    periodenverbrauch: Decimal | None = Field(default=None, title="Periodenverbrauch")
    periodenverbrauch_ursprung: str | None = Field(
        default=None, alias="periodenverbrauchUrsprung", title="Periodenverbrauchursprung"
    )
    ableser: AblesendeRolle | None = None
    status: Ablesungsstatus | None = None
    energiegehalt_gas: Decimal | None = Field(default=None, alias="energiegehaltGas", title="Energiegehaltgas")
    energiegehalt_gas_gueltig_von: datetime | None = Field(
        default=None, alias="energiegehaltGasGueltigVon", title="Energiegehaltgasgueltigvon"
    )
    energiegehalt_gas_gueltig_bis: datetime | None = Field(
        default=None, alias="energiegehaltGasGueltigBis", title="Energiegehaltgasgueltigbis"
    )
    umwandlungsfaktor_gas: Decimal | None = Field(
        default=None, alias="umwandlungsfaktorGas", title="Umwandlungsfaktorgas"
    )
    umwandlungsfaktor_gas_gueltig_von: datetime | None = Field(
        default=None, alias="umwandlungsfaktorGasGueltigVon", title="Umwandlungsfaktorgasgueltigvon"
    )
    umwandlungsfaktor_gas_gueltig_bis: datetime | None = Field(
        default=None, alias="umwandlungsfaktorGasGueltigBis", title="Umwandlungsfaktorgasgueltigbis"
    )
    messwertstatus: Messwertstatus | None = None
