r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Wireless
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Optional
from twilio.base.version import Version
from twilio.base.domain import Domain
from twilio.rest.wireless.v1.command import CommandList
from twilio.rest.wireless.v1.rate_plan import RatePlanList
from twilio.rest.wireless.v1.sim import SimList
from twilio.rest.wireless.v1.usage_record import UsageRecordList


class V1(Version):
    def __init__(self, domain: Domain):
        """
        Initialize the V1 version of Wireless

        :param domain: The Twilio.wireless domain
        """
        super().__init__(domain, "v1")
        self._commands: Optional[CommandList] = None
        self._rate_plans: Optional[RatePlanList] = None
        self._sims: Optional[SimList] = None
        self._usage_records: Optional[UsageRecordList] = None

    @property
    def commands(self) -> CommandList:
        if self._commands is None:
            self._commands = CommandList(self)
        return self._commands

    @property
    def rate_plans(self) -> RatePlanList:
        if self._rate_plans is None:
            self._rate_plans = RatePlanList(self)
        return self._rate_plans

    @property
    def sims(self) -> SimList:
        if self._sims is None:
            self._sims = SimList(self)
        return self._sims

    @property
    def usage_records(self) -> UsageRecordList:
        if self._usage_records is None:
            self._usage_records = UsageRecordList(self)
        return self._usage_records

    def __repr__(self) -> str:
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        """
        return "<Twilio.Wireless.V1>"
