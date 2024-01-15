r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Ip_messaging
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import deserialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class CredentialInstance(InstanceResource):
    class PushService(object):
        GCM = "gcm"
        APN = "apn"
        FCM = "fcm"

    """
    :ivar sid: 
    :ivar account_sid: 
    :ivar friendly_name: 
    :ivar type: 
    :ivar sandbox: 
    :ivar date_created: 
    :ivar date_updated: 
    :ivar url: 
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.type: Optional["CredentialInstance.PushService"] = payload.get("type")
        self.sandbox: Optional[str] = payload.get("sandbox")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "sid": sid or self.sid,
        }
        self._context: Optional[CredentialContext] = None

    @property
    def _proxy(self) -> "CredentialContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: CredentialContext for this CredentialInstance
        """
        if self._context is None:
            self._context = CredentialContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the CredentialInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the CredentialInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "CredentialInstance":
        """
        Fetch the CredentialInstance


        :returns: The fetched CredentialInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "CredentialInstance":
        """
        Asynchronous coroutine to fetch the CredentialInstance


        :returns: The fetched CredentialInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self,
        friendly_name: Union[str, object] = values.unset,
        certificate: Union[str, object] = values.unset,
        private_key: Union[str, object] = values.unset,
        sandbox: Union[bool, object] = values.unset,
        api_key: Union[str, object] = values.unset,
        secret: Union[str, object] = values.unset,
    ) -> "CredentialInstance":
        """
        Update the CredentialInstance

        :param friendly_name:
        :param certificate:
        :param private_key:
        :param sandbox:
        :param api_key:
        :param secret:

        :returns: The updated CredentialInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            certificate=certificate,
            private_key=private_key,
            sandbox=sandbox,
            api_key=api_key,
            secret=secret,
        )

    async def update_async(
        self,
        friendly_name: Union[str, object] = values.unset,
        certificate: Union[str, object] = values.unset,
        private_key: Union[str, object] = values.unset,
        sandbox: Union[bool, object] = values.unset,
        api_key: Union[str, object] = values.unset,
        secret: Union[str, object] = values.unset,
    ) -> "CredentialInstance":
        """
        Asynchronous coroutine to update the CredentialInstance

        :param friendly_name:
        :param certificate:
        :param private_key:
        :param sandbox:
        :param api_key:
        :param secret:

        :returns: The updated CredentialInstance
        """
        return await self._proxy.update_async(
            friendly_name=friendly_name,
            certificate=certificate,
            private_key=private_key,
            sandbox=sandbox,
            api_key=api_key,
            secret=secret,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.IpMessaging.V2.CredentialInstance {}>".format(context)


class CredentialContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the CredentialContext

        :param version: Version that contains the resource
        :param sid:
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/Credentials/{sid}".format(**self._solution)

    def delete(self) -> bool:
        """
        Deletes the CredentialInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the CredentialInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> CredentialInstance:
        """
        Fetch the CredentialInstance


        :returns: The fetched CredentialInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return CredentialInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> CredentialInstance:
        """
        Asynchronous coroutine to fetch the CredentialInstance


        :returns: The fetched CredentialInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return CredentialInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    def update(
        self,
        friendly_name: Union[str, object] = values.unset,
        certificate: Union[str, object] = values.unset,
        private_key: Union[str, object] = values.unset,
        sandbox: Union[bool, object] = values.unset,
        api_key: Union[str, object] = values.unset,
        secret: Union[str, object] = values.unset,
    ) -> CredentialInstance:
        """
        Update the CredentialInstance

        :param friendly_name:
        :param certificate:
        :param private_key:
        :param sandbox:
        :param api_key:
        :param secret:

        :returns: The updated CredentialInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
                "Certificate": certificate,
                "PrivateKey": private_key,
                "Sandbox": sandbox,
                "ApiKey": api_key,
                "Secret": secret,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return CredentialInstance(self._version, payload, sid=self._solution["sid"])

    async def update_async(
        self,
        friendly_name: Union[str, object] = values.unset,
        certificate: Union[str, object] = values.unset,
        private_key: Union[str, object] = values.unset,
        sandbox: Union[bool, object] = values.unset,
        api_key: Union[str, object] = values.unset,
        secret: Union[str, object] = values.unset,
    ) -> CredentialInstance:
        """
        Asynchronous coroutine to update the CredentialInstance

        :param friendly_name:
        :param certificate:
        :param private_key:
        :param sandbox:
        :param api_key:
        :param secret:

        :returns: The updated CredentialInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
                "Certificate": certificate,
                "PrivateKey": private_key,
                "Sandbox": sandbox,
                "ApiKey": api_key,
                "Secret": secret,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return CredentialInstance(self._version, payload, sid=self._solution["sid"])

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.IpMessaging.V2.CredentialContext {}>".format(context)


class CredentialPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> CredentialInstance:
        """
        Build an instance of CredentialInstance

        :param payload: Payload response from the API
        """
        return CredentialInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.IpMessaging.V2.CredentialPage>"


class CredentialList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the CredentialList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/Credentials"

    def create(
        self,
        type: "CredentialInstance.PushService",
        friendly_name: Union[str, object] = values.unset,
        certificate: Union[str, object] = values.unset,
        private_key: Union[str, object] = values.unset,
        sandbox: Union[bool, object] = values.unset,
        api_key: Union[str, object] = values.unset,
        secret: Union[str, object] = values.unset,
    ) -> CredentialInstance:
        """
        Create the CredentialInstance

        :param type:
        :param friendly_name:
        :param certificate:
        :param private_key:
        :param sandbox:
        :param api_key:
        :param secret:

        :returns: The created CredentialInstance
        """

        data = values.of(
            {
                "Type": type,
                "FriendlyName": friendly_name,
                "Certificate": certificate,
                "PrivateKey": private_key,
                "Sandbox": sandbox,
                "ApiKey": api_key,
                "Secret": secret,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return CredentialInstance(self._version, payload)

    async def create_async(
        self,
        type: "CredentialInstance.PushService",
        friendly_name: Union[str, object] = values.unset,
        certificate: Union[str, object] = values.unset,
        private_key: Union[str, object] = values.unset,
        sandbox: Union[bool, object] = values.unset,
        api_key: Union[str, object] = values.unset,
        secret: Union[str, object] = values.unset,
    ) -> CredentialInstance:
        """
        Asynchronously create the CredentialInstance

        :param type:
        :param friendly_name:
        :param certificate:
        :param private_key:
        :param sandbox:
        :param api_key:
        :param secret:

        :returns: The created CredentialInstance
        """

        data = values.of(
            {
                "Type": type,
                "FriendlyName": friendly_name,
                "Certificate": certificate,
                "PrivateKey": private_key,
                "Sandbox": sandbox,
                "ApiKey": api_key,
                "Secret": secret,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return CredentialInstance(self._version, payload)

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[CredentialInstance]:
        """
        Streams CredentialInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param limit: Upper limit for the number of records to return. stream()
                      guarantees to never return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, stream() will attempt to read the
                          limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        """
        limits = self._version.read_limits(limit, page_size)
        page = self.page(page_size=limits["page_size"])

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[CredentialInstance]:
        """
        Asynchronously streams CredentialInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param limit: Upper limit for the number of records to return. stream()
                      guarantees to never return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, stream() will attempt to read the
                          limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        """
        limits = self._version.read_limits(limit, page_size)
        page = await self.page_async(page_size=limits["page_size"])

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[CredentialInstance]:
        """
        Lists CredentialInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param limit: Upper limit for the number of records to return. list() guarantees
                      never to return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, list() will attempt to read the limit
                          with the most efficient page size, i.e. min(limit, 1000)

        :returns: list that will contain up to limit results
        """
        return list(
            self.stream(
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[CredentialInstance]:
        """
        Asynchronously lists CredentialInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param limit: Upper limit for the number of records to return. list() guarantees
                      never to return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, list() will attempt to read the limit
                          with the most efficient page size, i.e. min(limit, 1000)

        :returns: list that will contain up to limit results
        """
        return [
            record
            async for record in await self.stream_async(
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> CredentialPage:
        """
        Retrieve a single page of CredentialInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of CredentialInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return CredentialPage(self._version, response)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> CredentialPage:
        """
        Asynchronously retrieve a single page of CredentialInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of CredentialInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return CredentialPage(self._version, response)

    def get_page(self, target_url: str) -> CredentialPage:
        """
        Retrieve a specific page of CredentialInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of CredentialInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return CredentialPage(self._version, response)

    async def get_page_async(self, target_url: str) -> CredentialPage:
        """
        Asynchronously retrieve a specific page of CredentialInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of CredentialInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return CredentialPage(self._version, response)

    def get(self, sid: str) -> CredentialContext:
        """
        Constructs a CredentialContext

        :param sid:
        """
        return CredentialContext(self._version, sid=sid)

    def __call__(self, sid: str) -> CredentialContext:
        """
        Constructs a CredentialContext

        :param sid:
        """
        return CredentialContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.IpMessaging.V2.CredentialList>"
