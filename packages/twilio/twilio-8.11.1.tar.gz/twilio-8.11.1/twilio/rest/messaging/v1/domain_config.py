r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Messaging
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import datetime
from typing import Any, Dict, Optional, Union
from twilio.base import deserialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version


class DomainConfigInstance(InstanceResource):

    """
    :ivar domain_sid: The unique string that we created to identify the Domain resource.
    :ivar config_sid: The unique string that we created to identify the Domain config (prefix ZK).
    :ivar fallback_url: Any requests we receive to this domain that do not match an existing shortened message will be redirected to the fallback url. These will likely be either expired messages, random misdirected traffic, or intentional scraping.
    :ivar callback_url: URL to receive click events to your webhook whenever the recipients click on the shortened links.
    :ivar continue_on_failure: Boolean field to set customer delivery preference when there is a failure in linkShortening service
    :ivar date_created: Date this Domain Config was created.
    :ivar date_updated: Date that this Domain Config was last updated.
    :ivar url:
    :ivar disable_https: Customer's choice to send links with/without \"https://\" attached to shortened url. If true, messages will not be sent with https:// at the beginning of the url. If false, messages will be sent with https:// at the beginning of the url. False is the default behavior if it is not specified.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        domain_sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.domain_sid: Optional[str] = payload.get("domain_sid")
        self.config_sid: Optional[str] = payload.get("config_sid")
        self.fallback_url: Optional[str] = payload.get("fallback_url")
        self.callback_url: Optional[str] = payload.get("callback_url")
        self.continue_on_failure: Optional[bool] = payload.get("continue_on_failure")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.url: Optional[str] = payload.get("url")
        self.disable_https: Optional[bool] = payload.get("disable_https")

        self._solution = {
            "domain_sid": domain_sid or self.domain_sid,
        }
        self._context: Optional[DomainConfigContext] = None

    @property
    def _proxy(self) -> "DomainConfigContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: DomainConfigContext for this DomainConfigInstance
        """
        if self._context is None:
            self._context = DomainConfigContext(
                self._version,
                domain_sid=self._solution["domain_sid"],
            )
        return self._context

    def fetch(self) -> "DomainConfigInstance":
        """
        Fetch the DomainConfigInstance


        :returns: The fetched DomainConfigInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "DomainConfigInstance":
        """
        Asynchronous coroutine to fetch the DomainConfigInstance


        :returns: The fetched DomainConfigInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self,
        fallback_url: Union[str, object] = values.unset,
        callback_url: Union[str, object] = values.unset,
        continue_on_failure: Union[bool, object] = values.unset,
        disable_https: Union[bool, object] = values.unset,
    ) -> "DomainConfigInstance":
        """
        Update the DomainConfigInstance

        :param fallback_url: Any requests we receive to this domain that do not match an existing shortened message will be redirected to the fallback url. These will likely be either expired messages, random misdirected traffic, or intentional scraping.
        :param callback_url: URL to receive click events to your webhook whenever the recipients click on the shortened links
        :param continue_on_failure: Boolean field to set customer delivery preference when there is a failure in linkShortening service
        :param disable_https: Customer's choice to send links with/without \\\"https://\\\" attached to shortened url. If true, messages will not be sent with https:// at the beginning of the url. If false, messages will be sent with https:// at the beginning of the url. False is the default behavior if it is not specified.

        :returns: The updated DomainConfigInstance
        """
        return self._proxy.update(
            fallback_url=fallback_url,
            callback_url=callback_url,
            continue_on_failure=continue_on_failure,
            disable_https=disable_https,
        )

    async def update_async(
        self,
        fallback_url: Union[str, object] = values.unset,
        callback_url: Union[str, object] = values.unset,
        continue_on_failure: Union[bool, object] = values.unset,
        disable_https: Union[bool, object] = values.unset,
    ) -> "DomainConfigInstance":
        """
        Asynchronous coroutine to update the DomainConfigInstance

        :param fallback_url: Any requests we receive to this domain that do not match an existing shortened message will be redirected to the fallback url. These will likely be either expired messages, random misdirected traffic, or intentional scraping.
        :param callback_url: URL to receive click events to your webhook whenever the recipients click on the shortened links
        :param continue_on_failure: Boolean field to set customer delivery preference when there is a failure in linkShortening service
        :param disable_https: Customer's choice to send links with/without \\\"https://\\\" attached to shortened url. If true, messages will not be sent with https:// at the beginning of the url. If false, messages will be sent with https:// at the beginning of the url. False is the default behavior if it is not specified.

        :returns: The updated DomainConfigInstance
        """
        return await self._proxy.update_async(
            fallback_url=fallback_url,
            callback_url=callback_url,
            continue_on_failure=continue_on_failure,
            disable_https=disable_https,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Messaging.V1.DomainConfigInstance {}>".format(context)


class DomainConfigContext(InstanceContext):
    def __init__(self, version: Version, domain_sid: str):
        """
        Initialize the DomainConfigContext

        :param version: Version that contains the resource
        :param domain_sid: Unique string used to identify the domain that this config should be associated with.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "domain_sid": domain_sid,
        }
        self._uri = "/LinkShortening/Domains/{domain_sid}/Config".format(
            **self._solution
        )

    def fetch(self) -> DomainConfigInstance:
        """
        Fetch the DomainConfigInstance


        :returns: The fetched DomainConfigInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return DomainConfigInstance(
            self._version,
            payload,
            domain_sid=self._solution["domain_sid"],
        )

    async def fetch_async(self) -> DomainConfigInstance:
        """
        Asynchronous coroutine to fetch the DomainConfigInstance


        :returns: The fetched DomainConfigInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return DomainConfigInstance(
            self._version,
            payload,
            domain_sid=self._solution["domain_sid"],
        )

    def update(
        self,
        fallback_url: Union[str, object] = values.unset,
        callback_url: Union[str, object] = values.unset,
        continue_on_failure: Union[bool, object] = values.unset,
        disable_https: Union[bool, object] = values.unset,
    ) -> DomainConfigInstance:
        """
        Update the DomainConfigInstance

        :param fallback_url: Any requests we receive to this domain that do not match an existing shortened message will be redirected to the fallback url. These will likely be either expired messages, random misdirected traffic, or intentional scraping.
        :param callback_url: URL to receive click events to your webhook whenever the recipients click on the shortened links
        :param continue_on_failure: Boolean field to set customer delivery preference when there is a failure in linkShortening service
        :param disable_https: Customer's choice to send links with/without \\\"https://\\\" attached to shortened url. If true, messages will not be sent with https:// at the beginning of the url. If false, messages will be sent with https:// at the beginning of the url. False is the default behavior if it is not specified.

        :returns: The updated DomainConfigInstance
        """
        data = values.of(
            {
                "FallbackUrl": fallback_url,
                "CallbackUrl": callback_url,
                "ContinueOnFailure": continue_on_failure,
                "DisableHttps": disable_https,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return DomainConfigInstance(
            self._version, payload, domain_sid=self._solution["domain_sid"]
        )

    async def update_async(
        self,
        fallback_url: Union[str, object] = values.unset,
        callback_url: Union[str, object] = values.unset,
        continue_on_failure: Union[bool, object] = values.unset,
        disable_https: Union[bool, object] = values.unset,
    ) -> DomainConfigInstance:
        """
        Asynchronous coroutine to update the DomainConfigInstance

        :param fallback_url: Any requests we receive to this domain that do not match an existing shortened message will be redirected to the fallback url. These will likely be either expired messages, random misdirected traffic, or intentional scraping.
        :param callback_url: URL to receive click events to your webhook whenever the recipients click on the shortened links
        :param continue_on_failure: Boolean field to set customer delivery preference when there is a failure in linkShortening service
        :param disable_https: Customer's choice to send links with/without \\\"https://\\\" attached to shortened url. If true, messages will not be sent with https:// at the beginning of the url. If false, messages will be sent with https:// at the beginning of the url. False is the default behavior if it is not specified.

        :returns: The updated DomainConfigInstance
        """
        data = values.of(
            {
                "FallbackUrl": fallback_url,
                "CallbackUrl": callback_url,
                "ContinueOnFailure": continue_on_failure,
                "DisableHttps": disable_https,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return DomainConfigInstance(
            self._version, payload, domain_sid=self._solution["domain_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Messaging.V1.DomainConfigContext {}>".format(context)


class DomainConfigList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the DomainConfigList

        :param version: Version that contains the resource

        """
        super().__init__(version)

    def get(self, domain_sid: str) -> DomainConfigContext:
        """
        Constructs a DomainConfigContext

        :param domain_sid: Unique string used to identify the domain that this config should be associated with.
        """
        return DomainConfigContext(self._version, domain_sid=domain_sid)

    def __call__(self, domain_sid: str) -> DomainConfigContext:
        """
        Constructs a DomainConfigContext

        :param domain_sid: Unique string used to identify the domain that this config should be associated with.
        """
        return DomainConfigContext(self._version, domain_sid=domain_sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Messaging.V1.DomainConfigList>"
