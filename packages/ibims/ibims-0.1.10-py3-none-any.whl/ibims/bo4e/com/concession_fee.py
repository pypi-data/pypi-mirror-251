from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class ConcessionFee(BaseModel):
    """
    The Concession Fee object was created during a migration project.
    It contains attributes needed for metering mapping.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    market_location_id: Annotated[str, Field(alias="marketLocationId", title="Marketlocationid")]
    group: Annotated[str | None, Field(None, title="Group")]
    obis: Annotated[str, Field(title="Obis")]
    active_from: Annotated[datetime, Field(alias="activeFrom", title="Activefrom")]
    active_until: Annotated[datetime | None, Field(None, alias="activeUntil", title="Activeuntil")]
    ka: Annotated[str | None, Field(None, title="Ka")]
