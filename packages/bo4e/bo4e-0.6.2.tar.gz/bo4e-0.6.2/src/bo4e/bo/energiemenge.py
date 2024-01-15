"""
Contains Energiemenge class
and corresponding marshmallow schema for de-/serialization
"""
from typing import Optional

from bo4e.bo.geschaeftsobjekt import Geschaeftsobjekt
from bo4e.com.verbrauch import Verbrauch
from bo4e.enum.botyp import BoTyp
from bo4e.enum.lokationstyp import Lokationstyp

# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module


class Energiemenge(Geschaeftsobjekt):
    """
    Abbildung von Mengen, die Lokationen zugeordnet sind

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Energiemenge.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemenge JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Energiemenge.json>`_

    """

    # required attributes
    bo_typ: BoTyp = BoTyp.ENERGIEMENGE
    #: Eindeutige Nummer der Marktlokation bzw. der Messlokation, zu der die Energiemenge gehört
    lokations_id: Optional[str] = None
    # todo: add validator such that only mess- or marktlokations IDs are accepted + cross check with lokationstyp
    #: Gibt an, ob es sich um eine Markt- oder Messlokation handelt
    lokationstyp: Optional[Lokationstyp] = None

    #: Gibt den Verbrauch in einer Zeiteinheit an
    energieverbrauch: Optional[list[Verbrauch]] = None
    # there are no optional attributes
