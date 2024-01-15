from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.abgabeart import Abgabeart
from ..enum.energierichtung import Energierichtung
from ..enum.mengeneinheit import Mengeneinheit


class Zaehlwerk(BaseModel):
    """
    Mit dieser Komponente werden Zählwerke modelliert.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zaehlwerk.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zaehlwerk JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zaehlwerk.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    einheit: Mengeneinheit | None = None
    obis_kennzahl: Annotated[str | None, Field(None, alias="obisKennzahl", title="Obiskennzahl")]
    richtung: Energierichtung | None = None
    wandlerfaktor: Annotated[Decimal | None, Field(None, title="Wandlerfaktor")]
    zaehlwerk_id: Annotated[str | None, Field(None, alias="zaehlwerkId", title="Zaehlwerkid")]
    vorkommastellen: Annotated[int, Field(title="Vorkommastellen")]
    nachkommastellen: Annotated[int, Field(title="Nachkommastellen")]
    schwachlastfaehig: Annotated[bool, Field(title="Schwachlastfaehig")]
    konzessionsabgaben_typ: Annotated[Abgabeart | None, Field(None, alias="konzessionsabgabenTyp")]
    active_from: Annotated[datetime, Field(alias="activeFrom", title="Activefrom")]
    active_until: Annotated[datetime | None, Field(None, alias="activeUntil", title="Activeuntil")]
    description: Annotated[str | None, Field(None, title="Description")]
    verbrauchsart: Annotated[str | None, Field(None, title="Verbrauchsart")]
