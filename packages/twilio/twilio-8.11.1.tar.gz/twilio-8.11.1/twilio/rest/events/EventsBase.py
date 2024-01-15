r"""
  This code was generated by
  ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
   |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
   |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

  NOTE: This class is auto generated by OpenAPI Generator.
  https://openapi-generator.tech
  Do not edit the class manually.
"""

from typing import Optional

from twilio.base.domain import Domain
from twilio.rest import Client
from twilio.rest.events.v1 import V1


class EventsBase(Domain):
    def __init__(self, twilio: Client):
        """
        Initialize the Events Domain

        :returns: Domain for Events
        """
        super().__init__(twilio, "https://events.twilio.com")
        self._v1: Optional[V1] = None

    @property
    def v1(self) -> V1:
        """
        :returns: Versions v1 of Events
        """
        if self._v1 is None:
            self._v1 = V1(self)
        return self._v1

    def __repr__(self) -> str:
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        """
        return "<Twilio.Events>"
