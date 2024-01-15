r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Intelligence
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Optional
from twilio.base.version import Version
from twilio.base.domain import Domain
from twilio.rest.intelligence.v2.service import ServiceList
from twilio.rest.intelligence.v2.transcript import TranscriptList


class V2(Version):
    def __init__(self, domain: Domain):
        """
        Initialize the V2 version of Intelligence

        :param domain: The Twilio.intelligence domain
        """
        super().__init__(domain, "v2")
        self._services: Optional[ServiceList] = None
        self._transcripts: Optional[TranscriptList] = None

    @property
    def services(self) -> ServiceList:
        if self._services is None:
            self._services = ServiceList(self)
        return self._services

    @property
    def transcripts(self) -> TranscriptList:
        if self._transcripts is None:
            self._transcripts = TranscriptList(self)
        return self._transcripts

    def __repr__(self) -> str:
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        """
        return "<Twilio.Intelligence.V2>"
