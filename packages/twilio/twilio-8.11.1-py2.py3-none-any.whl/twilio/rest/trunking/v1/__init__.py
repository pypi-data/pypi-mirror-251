r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Trunking
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Optional
from twilio.base.version import Version
from twilio.base.domain import Domain
from twilio.rest.trunking.v1.trunk import TrunkList


class V1(Version):
    def __init__(self, domain: Domain):
        """
        Initialize the V1 version of Trunking

        :param domain: The Twilio.trunking domain
        """
        super().__init__(domain, "v1")
        self._trunks: Optional[TrunkList] = None

    @property
    def trunks(self) -> TrunkList:
        if self._trunks is None:
            self._trunks = TrunkList(self)
        return self._trunks

    def __repr__(self) -> str:
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        """
        return "<Twilio.Trunking.V1>"
