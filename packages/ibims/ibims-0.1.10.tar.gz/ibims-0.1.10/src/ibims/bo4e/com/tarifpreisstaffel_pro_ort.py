from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class TarifpreisstaffelProOrt(BaseModel):
    """
    Gibt die Staffelgrenzen der jeweiligen Preise an

    .. raw:: html

        <object data="../_static/images/bo4e/com/TarifpreisstaffelProOrt.svg" type="image/svg+xml"></object>

    .. HINT::
        `TarifpreisstaffelProOrt JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/TarifpreisstaffelProOrt.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    arbeitspreis: Annotated[Decimal | None, Field(None, title="Arbeitspreis")]
    arbeitspreis_nt: Annotated[Decimal | None, Field(None, alias="arbeitspreisNT", title="Arbeitspreisnt")]
    grundpreis: Annotated[Decimal | None, Field(None, title="Grundpreis")]
    staffelgrenze_bis: Annotated[Decimal | None, Field(None, alias="staffelgrenzeBis", title="Staffelgrenzebis")]
    staffelgrenze_von: Annotated[Decimal | None, Field(None, alias="staffelgrenzeVon", title="Staffelgrenzevon")]
