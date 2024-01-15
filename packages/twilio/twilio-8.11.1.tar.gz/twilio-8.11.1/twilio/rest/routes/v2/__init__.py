r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Routes
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Optional
from twilio.base.version import Version
from twilio.base.domain import Domain
from twilio.rest.routes.v2.phone_number import PhoneNumberList
from twilio.rest.routes.v2.sip_domain import SipDomainList
from twilio.rest.routes.v2.trunk import TrunkList


class V2(Version):
    def __init__(self, domain: Domain):
        """
        Initialize the V2 version of Routes

        :param domain: The Twilio.routes domain
        """
        super().__init__(domain, "v2")
        self._phone_numbers: Optional[PhoneNumberList] = None
        self._sip_domains: Optional[SipDomainList] = None
        self._trunks: Optional[TrunkList] = None

    @property
    def phone_numbers(self) -> PhoneNumberList:
        if self._phone_numbers is None:
            self._phone_numbers = PhoneNumberList(self)
        return self._phone_numbers

    @property
    def sip_domains(self) -> SipDomainList:
        if self._sip_domains is None:
            self._sip_domains = SipDomainList(self)
        return self._sip_domains

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
        return "<Twilio.Routes.V2>"
