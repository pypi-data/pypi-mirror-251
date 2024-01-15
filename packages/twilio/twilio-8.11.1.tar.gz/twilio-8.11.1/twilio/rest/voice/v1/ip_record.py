r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Voice
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


class IpRecordInstance(InstanceResource):

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the IP Record resource.
    :ivar sid: The unique string that we created to identify the IP Record resource.
    :ivar friendly_name: The string that you assigned to describe the resource.
    :ivar ip_address: An IP address in dotted decimal notation, IPv4 only.
    :ivar cidr_prefix_length: An integer representing the length of the [CIDR](https://tools.ietf.org/html/rfc4632) prefix to use with this IP address. By default the entire IP address is used, which for IPv4 is value 32.
    :ivar date_created: The date and time in GMT that the resource was created specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar date_updated: The date and time in GMT that the resource was last updated specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar url: The absolute URL of the resource.
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.sid: Optional[str] = payload.get("sid")
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.ip_address: Optional[str] = payload.get("ip_address")
        self.cidr_prefix_length: Optional[int] = deserialize.integer(
            payload.get("cidr_prefix_length")
        )
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
        self._context: Optional[IpRecordContext] = None

    @property
    def _proxy(self) -> "IpRecordContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: IpRecordContext for this IpRecordInstance
        """
        if self._context is None:
            self._context = IpRecordContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the IpRecordInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the IpRecordInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "IpRecordInstance":
        """
        Fetch the IpRecordInstance


        :returns: The fetched IpRecordInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "IpRecordInstance":
        """
        Asynchronous coroutine to fetch the IpRecordInstance


        :returns: The fetched IpRecordInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self, friendly_name: Union[str, object] = values.unset
    ) -> "IpRecordInstance":
        """
        Update the IpRecordInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It is not unique and can be up to 255 characters long.

        :returns: The updated IpRecordInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
        )

    async def update_async(
        self, friendly_name: Union[str, object] = values.unset
    ) -> "IpRecordInstance":
        """
        Asynchronous coroutine to update the IpRecordInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It is not unique and can be up to 255 characters long.

        :returns: The updated IpRecordInstance
        """
        return await self._proxy.update_async(
            friendly_name=friendly_name,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Voice.V1.IpRecordInstance {}>".format(context)


class IpRecordContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the IpRecordContext

        :param version: Version that contains the resource
        :param sid: The Twilio-provided string that uniquely identifies the IP Record resource to update.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/IpRecords/{sid}".format(**self._solution)

    def delete(self) -> bool:
        """
        Deletes the IpRecordInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the IpRecordInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> IpRecordInstance:
        """
        Fetch the IpRecordInstance


        :returns: The fetched IpRecordInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return IpRecordInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> IpRecordInstance:
        """
        Asynchronous coroutine to fetch the IpRecordInstance


        :returns: The fetched IpRecordInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return IpRecordInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    def update(
        self, friendly_name: Union[str, object] = values.unset
    ) -> IpRecordInstance:
        """
        Update the IpRecordInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It is not unique and can be up to 255 characters long.

        :returns: The updated IpRecordInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return IpRecordInstance(self._version, payload, sid=self._solution["sid"])

    async def update_async(
        self, friendly_name: Union[str, object] = values.unset
    ) -> IpRecordInstance:
        """
        Asynchronous coroutine to update the IpRecordInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It is not unique and can be up to 255 characters long.

        :returns: The updated IpRecordInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return IpRecordInstance(self._version, payload, sid=self._solution["sid"])

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Voice.V1.IpRecordContext {}>".format(context)


class IpRecordPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> IpRecordInstance:
        """
        Build an instance of IpRecordInstance

        :param payload: Payload response from the API
        """
        return IpRecordInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Voice.V1.IpRecordPage>"


class IpRecordList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the IpRecordList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/IpRecords"

    def create(
        self,
        ip_address: str,
        friendly_name: Union[str, object] = values.unset,
        cidr_prefix_length: Union[int, object] = values.unset,
    ) -> IpRecordInstance:
        """
        Create the IpRecordInstance

        :param ip_address: An IP address in dotted decimal notation, IPv4 only.
        :param friendly_name: A descriptive string that you create to describe the resource. It is not unique and can be up to 255 characters long.
        :param cidr_prefix_length: An integer representing the length of the [CIDR](https://tools.ietf.org/html/rfc4632) prefix to use with this IP address. By default the entire IP address is used, which for IPv4 is value 32.

        :returns: The created IpRecordInstance
        """

        data = values.of(
            {
                "IpAddress": ip_address,
                "FriendlyName": friendly_name,
                "CidrPrefixLength": cidr_prefix_length,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return IpRecordInstance(self._version, payload)

    async def create_async(
        self,
        ip_address: str,
        friendly_name: Union[str, object] = values.unset,
        cidr_prefix_length: Union[int, object] = values.unset,
    ) -> IpRecordInstance:
        """
        Asynchronously create the IpRecordInstance

        :param ip_address: An IP address in dotted decimal notation, IPv4 only.
        :param friendly_name: A descriptive string that you create to describe the resource. It is not unique and can be up to 255 characters long.
        :param cidr_prefix_length: An integer representing the length of the [CIDR](https://tools.ietf.org/html/rfc4632) prefix to use with this IP address. By default the entire IP address is used, which for IPv4 is value 32.

        :returns: The created IpRecordInstance
        """

        data = values.of(
            {
                "IpAddress": ip_address,
                "FriendlyName": friendly_name,
                "CidrPrefixLength": cidr_prefix_length,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return IpRecordInstance(self._version, payload)

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[IpRecordInstance]:
        """
        Streams IpRecordInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[IpRecordInstance]:
        """
        Asynchronously streams IpRecordInstance records from the API as a generator stream.
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
    ) -> List[IpRecordInstance]:
        """
        Lists IpRecordInstance records from the API as a list.
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
    ) -> List[IpRecordInstance]:
        """
        Asynchronously lists IpRecordInstance records from the API as a list.
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
    ) -> IpRecordPage:
        """
        Retrieve a single page of IpRecordInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of IpRecordInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return IpRecordPage(self._version, response)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> IpRecordPage:
        """
        Asynchronously retrieve a single page of IpRecordInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of IpRecordInstance
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
        return IpRecordPage(self._version, response)

    def get_page(self, target_url: str) -> IpRecordPage:
        """
        Retrieve a specific page of IpRecordInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of IpRecordInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return IpRecordPage(self._version, response)

    async def get_page_async(self, target_url: str) -> IpRecordPage:
        """
        Asynchronously retrieve a specific page of IpRecordInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of IpRecordInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return IpRecordPage(self._version, response)

    def get(self, sid: str) -> IpRecordContext:
        """
        Constructs a IpRecordContext

        :param sid: The Twilio-provided string that uniquely identifies the IP Record resource to update.
        """
        return IpRecordContext(self._version, sid=sid)

    def __call__(self, sid: str) -> IpRecordContext:
        """
        Constructs a IpRecordContext

        :param sid: The Twilio-provided string that uniquely identifies the IP Record resource to update.
        """
        return IpRecordContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Voice.V1.IpRecordList>"
