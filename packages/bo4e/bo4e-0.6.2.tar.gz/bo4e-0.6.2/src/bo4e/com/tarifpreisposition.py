"""
Contains Tarifpreisposition class
and corresponding marshmallow schema for de-/serialization
"""

# pylint: disable=too-few-public-methods
# pylint: disable=no-name-in-module
from typing import Optional

from bo4e.com.com import COM
from bo4e.com.preisstaffel import Preisstaffel
from bo4e.enum.mengeneinheit import Mengeneinheit
from bo4e.enum.preistyp import Preistyp
from bo4e.enum.waehrungseinheit import Waehrungseinheit


class Tarifpreisposition(COM):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen abgebildet werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifpreisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifpreisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifpreisposition.json>`_

    """

    # required attributes
    #: Angabe des Preistypes (z.B. Grundpreis)
    preistyp: Optional[Preistyp] = None
    #: Einheit des Preises (z.B. EURO)
    einheit: Optional[Waehrungseinheit] = None
    #: Größe, auf die sich die Einheit bezieht, beispielsweise kWh, Jahr
    bezugseinheit: Optional[Mengeneinheit] = None
    #: Hier sind die Staffeln mit ihren Preisenangaben definiert
    preisstaffeln: Optional[list[Preisstaffel]] = None

    # optional attributes
    #: Gibt an, nach welcher Menge die vorgenannte Einschränkung erfolgt (z.B. Jahresstromverbrauch in kWh)
    mengeneinheitstaffel: Optional[Mengeneinheit] = None
