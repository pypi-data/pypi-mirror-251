r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Preview
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from typing import Any, Dict, Optional, Union
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version


class UsageInstance(InstanceResource):

    """
    :ivar sim_sid:
    :ivar sim_unique_name:
    :ivar account_sid:
    :ivar period:
    :ivar commands_usage:
    :ivar commands_costs:
    :ivar data_usage:
    :ivar data_costs:
    :ivar url:
    """

    def __init__(self, version: Version, payload: Dict[str, Any], sim_sid: str):
        super().__init__(version)

        self.sim_sid: Optional[str] = payload.get("sim_sid")
        self.sim_unique_name: Optional[str] = payload.get("sim_unique_name")
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.period: Optional[Dict[str, object]] = payload.get("period")
        self.commands_usage: Optional[Dict[str, object]] = payload.get("commands_usage")
        self.commands_costs: Optional[Dict[str, object]] = payload.get("commands_costs")
        self.data_usage: Optional[Dict[str, object]] = payload.get("data_usage")
        self.data_costs: Optional[Dict[str, object]] = payload.get("data_costs")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "sim_sid": sim_sid,
        }
        self._context: Optional[UsageContext] = None

    @property
    def _proxy(self) -> "UsageContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: UsageContext for this UsageInstance
        """
        if self._context is None:
            self._context = UsageContext(
                self._version,
                sim_sid=self._solution["sim_sid"],
            )
        return self._context

    def fetch(
        self,
        end: Union[str, object] = values.unset,
        start: Union[str, object] = values.unset,
    ) -> "UsageInstance":
        """
        Fetch the UsageInstance

        :param end:
        :param start:

        :returns: The fetched UsageInstance
        """
        return self._proxy.fetch(
            end=end,
            start=start,
        )

    async def fetch_async(
        self,
        end: Union[str, object] = values.unset,
        start: Union[str, object] = values.unset,
    ) -> "UsageInstance":
        """
        Asynchronous coroutine to fetch the UsageInstance

        :param end:
        :param start:

        :returns: The fetched UsageInstance
        """
        return await self._proxy.fetch_async(
            end=end,
            start=start,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Preview.Wireless.UsageInstance {}>".format(context)


class UsageContext(InstanceContext):
    def __init__(self, version: Version, sim_sid: str):
        """
        Initialize the UsageContext

        :param version: Version that contains the resource
        :param sim_sid:
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sim_sid": sim_sid,
        }
        self._uri = "/Sims/{sim_sid}/Usage".format(**self._solution)

    def fetch(
        self,
        end: Union[str, object] = values.unset,
        start: Union[str, object] = values.unset,
    ) -> UsageInstance:
        """
        Fetch the UsageInstance

        :param end:
        :param start:

        :returns: The fetched UsageInstance
        """

        data = values.of(
            {
                "End": end,
                "Start": start,
            }
        )

        payload = self._version.fetch(method="GET", uri=self._uri, params=data)

        return UsageInstance(
            self._version,
            payload,
            sim_sid=self._solution["sim_sid"],
        )

    async def fetch_async(
        self,
        end: Union[str, object] = values.unset,
        start: Union[str, object] = values.unset,
    ) -> UsageInstance:
        """
        Asynchronous coroutine to fetch the UsageInstance

        :param end:
        :param start:

        :returns: The fetched UsageInstance
        """

        data = values.of(
            {
                "End": end,
                "Start": start,
            }
        )

        payload = await self._version.fetch_async(
            method="GET", uri=self._uri, params=data
        )

        return UsageInstance(
            self._version,
            payload,
            sim_sid=self._solution["sim_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Preview.Wireless.UsageContext {}>".format(context)


class UsageList(ListResource):
    def __init__(self, version: Version, sim_sid: str):
        """
        Initialize the UsageList

        :param version: Version that contains the resource
        :param sim_sid:

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sim_sid": sim_sid,
        }

    def get(self) -> UsageContext:
        """
        Constructs a UsageContext

        """
        return UsageContext(self._version, sim_sid=self._solution["sim_sid"])

    def __call__(self) -> UsageContext:
        """
        Constructs a UsageContext

        """
        return UsageContext(self._version, sim_sid=self._solution["sim_sid"])

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Preview.Wireless.UsageList>"
