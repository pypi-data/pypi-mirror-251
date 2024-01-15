r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Numbers
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Optional
from twilio.base.version import Version
from twilio.base.domain import Domain
from twilio.rest.numbers.v1.bulk_eligibility import BulkEligibilityList
from twilio.rest.numbers.v1.porting_bulk_portability import PortingBulkPortabilityList
from twilio.rest.numbers.v1.porting_port_in_fetch import PortingPortInFetchList
from twilio.rest.numbers.v1.porting_portability import PortingPortabilityList


class V1(Version):
    def __init__(self, domain: Domain):
        """
        Initialize the V1 version of Numbers

        :param domain: The Twilio.numbers domain
        """
        super().__init__(domain, "v1")
        self._bulk_eligibilities: Optional[BulkEligibilityList] = None
        self._porting_bulk_portabilities: Optional[PortingBulkPortabilityList] = None
        self._porting_port_ins: Optional[PortingPortInFetchList] = None
        self._porting_portabilities: Optional[PortingPortabilityList] = None

    @property
    def bulk_eligibilities(self) -> BulkEligibilityList:
        if self._bulk_eligibilities is None:
            self._bulk_eligibilities = BulkEligibilityList(self)
        return self._bulk_eligibilities

    @property
    def porting_bulk_portabilities(self) -> PortingBulkPortabilityList:
        if self._porting_bulk_portabilities is None:
            self._porting_bulk_portabilities = PortingBulkPortabilityList(self)
        return self._porting_bulk_portabilities

    @property
    def porting_port_ins(self) -> PortingPortInFetchList:
        if self._porting_port_ins is None:
            self._porting_port_ins = PortingPortInFetchList(self)
        return self._porting_port_ins

    @property
    def porting_portabilities(self) -> PortingPortabilityList:
        if self._porting_portabilities is None:
            self._porting_portabilities = PortingPortabilityList(self)
        return self._porting_portabilities

    def __repr__(self) -> str:
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        """
        return "<Twilio.Numbers.V1>"
