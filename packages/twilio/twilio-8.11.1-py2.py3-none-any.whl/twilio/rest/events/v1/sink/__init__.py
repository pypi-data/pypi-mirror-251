r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Events
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import deserialize, serialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page
from twilio.rest.events.v1.sink.sink_test import SinkTestList
from twilio.rest.events.v1.sink.sink_validate import SinkValidateList


class SinkInstance(InstanceResource):
    class SinkType(object):
        KINESIS = "kinesis"
        WEBHOOK = "webhook"
        SEGMENT = "segment"

    class Status(object):
        INITIALIZED = "initialized"
        VALIDATING = "validating"
        ACTIVE = "active"
        FAILED = "failed"

    """
    :ivar date_created: The date that this Sink was created, given in ISO 8601 format.
    :ivar date_updated: The date that this Sink was updated, given in ISO 8601 format.
    :ivar description: A human readable description for the Sink
    :ivar sid: A 34 character string that uniquely identifies this Sink.
    :ivar sink_configuration: The information required for Twilio to connect to the provided Sink encoded as JSON.
    :ivar sink_type: 
    :ivar status: 
    :ivar url: The URL of this resource.
    :ivar links: Contains a dictionary of URL links to nested resources of this Sink.
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.description: Optional[str] = payload.get("description")
        self.sid: Optional[str] = payload.get("sid")
        self.sink_configuration: Optional[Dict[str, object]] = payload.get(
            "sink_configuration"
        )
        self.sink_type: Optional["SinkInstance.SinkType"] = payload.get("sink_type")
        self.status: Optional["SinkInstance.Status"] = payload.get("status")
        self.url: Optional[str] = payload.get("url")
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "sid": sid or self.sid,
        }
        self._context: Optional[SinkContext] = None

    @property
    def _proxy(self) -> "SinkContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: SinkContext for this SinkInstance
        """
        if self._context is None:
            self._context = SinkContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the SinkInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the SinkInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "SinkInstance":
        """
        Fetch the SinkInstance


        :returns: The fetched SinkInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "SinkInstance":
        """
        Asynchronous coroutine to fetch the SinkInstance


        :returns: The fetched SinkInstance
        """
        return await self._proxy.fetch_async()

    def update(self, description: str) -> "SinkInstance":
        """
        Update the SinkInstance

        :param description: A human readable description for the Sink **This value should not contain PII.**

        :returns: The updated SinkInstance
        """
        return self._proxy.update(
            description=description,
        )

    async def update_async(self, description: str) -> "SinkInstance":
        """
        Asynchronous coroutine to update the SinkInstance

        :param description: A human readable description for the Sink **This value should not contain PII.**

        :returns: The updated SinkInstance
        """
        return await self._proxy.update_async(
            description=description,
        )

    @property
    def sink_test(self) -> SinkTestList:
        """
        Access the sink_test
        """
        return self._proxy.sink_test

    @property
    def sink_validate(self) -> SinkValidateList:
        """
        Access the sink_validate
        """
        return self._proxy.sink_validate

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Events.V1.SinkInstance {}>".format(context)


class SinkContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the SinkContext

        :param version: Version that contains the resource
        :param sid: A 34 character string that uniquely identifies this Sink.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/Sinks/{sid}".format(**self._solution)

        self._sink_test: Optional[SinkTestList] = None
        self._sink_validate: Optional[SinkValidateList] = None

    def delete(self) -> bool:
        """
        Deletes the SinkInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the SinkInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> SinkInstance:
        """
        Fetch the SinkInstance


        :returns: The fetched SinkInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return SinkInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> SinkInstance:
        """
        Asynchronous coroutine to fetch the SinkInstance


        :returns: The fetched SinkInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return SinkInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    def update(self, description: str) -> SinkInstance:
        """
        Update the SinkInstance

        :param description: A human readable description for the Sink **This value should not contain PII.**

        :returns: The updated SinkInstance
        """
        data = values.of(
            {
                "Description": description,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return SinkInstance(self._version, payload, sid=self._solution["sid"])

    async def update_async(self, description: str) -> SinkInstance:
        """
        Asynchronous coroutine to update the SinkInstance

        :param description: A human readable description for the Sink **This value should not contain PII.**

        :returns: The updated SinkInstance
        """
        data = values.of(
            {
                "Description": description,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return SinkInstance(self._version, payload, sid=self._solution["sid"])

    @property
    def sink_test(self) -> SinkTestList:
        """
        Access the sink_test
        """
        if self._sink_test is None:
            self._sink_test = SinkTestList(
                self._version,
                self._solution["sid"],
            )
        return self._sink_test

    @property
    def sink_validate(self) -> SinkValidateList:
        """
        Access the sink_validate
        """
        if self._sink_validate is None:
            self._sink_validate = SinkValidateList(
                self._version,
                self._solution["sid"],
            )
        return self._sink_validate

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Events.V1.SinkContext {}>".format(context)


class SinkPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> SinkInstance:
        """
        Build an instance of SinkInstance

        :param payload: Payload response from the API
        """
        return SinkInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Events.V1.SinkPage>"


class SinkList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the SinkList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/Sinks"

    def create(
        self,
        description: str,
        sink_configuration: object,
        sink_type: "SinkInstance.SinkType",
    ) -> SinkInstance:
        """
        Create the SinkInstance

        :param description: A human readable description for the Sink **This value should not contain PII.**
        :param sink_configuration: The information required for Twilio to connect to the provided Sink encoded as JSON.
        :param sink_type:

        :returns: The created SinkInstance
        """

        data = values.of(
            {
                "Description": description,
                "SinkConfiguration": serialize.object(sink_configuration),
                "SinkType": sink_type,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return SinkInstance(self._version, payload)

    async def create_async(
        self,
        description: str,
        sink_configuration: object,
        sink_type: "SinkInstance.SinkType",
    ) -> SinkInstance:
        """
        Asynchronously create the SinkInstance

        :param description: A human readable description for the Sink **This value should not contain PII.**
        :param sink_configuration: The information required for Twilio to connect to the provided Sink encoded as JSON.
        :param sink_type:

        :returns: The created SinkInstance
        """

        data = values.of(
            {
                "Description": description,
                "SinkConfiguration": serialize.object(sink_configuration),
                "SinkType": sink_type,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return SinkInstance(self._version, payload)

    def stream(
        self,
        in_use: Union[bool, object] = values.unset,
        status: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[SinkInstance]:
        """
        Streams SinkInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param bool in_use: A boolean query parameter filtering the results to return sinks used/not used by a subscription.
        :param str status: A String query parameter filtering the results by status `initialized`, `validating`, `active` or `failed`.
        :param limit: Upper limit for the number of records to return. stream()
                      guarantees to never return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, stream() will attempt to read the
                          limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        """
        limits = self._version.read_limits(limit, page_size)
        page = self.page(in_use=in_use, status=status, page_size=limits["page_size"])

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        in_use: Union[bool, object] = values.unset,
        status: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[SinkInstance]:
        """
        Asynchronously streams SinkInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param bool in_use: A boolean query parameter filtering the results to return sinks used/not used by a subscription.
        :param str status: A String query parameter filtering the results by status `initialized`, `validating`, `active` or `failed`.
        :param limit: Upper limit for the number of records to return. stream()
                      guarantees to never return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, stream() will attempt to read the
                          limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        """
        limits = self._version.read_limits(limit, page_size)
        page = await self.page_async(
            in_use=in_use, status=status, page_size=limits["page_size"]
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        in_use: Union[bool, object] = values.unset,
        status: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[SinkInstance]:
        """
        Lists SinkInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param bool in_use: A boolean query parameter filtering the results to return sinks used/not used by a subscription.
        :param str status: A String query parameter filtering the results by status `initialized`, `validating`, `active` or `failed`.
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
                in_use=in_use,
                status=status,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        in_use: Union[bool, object] = values.unset,
        status: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[SinkInstance]:
        """
        Asynchronously lists SinkInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param bool in_use: A boolean query parameter filtering the results to return sinks used/not used by a subscription.
        :param str status: A String query parameter filtering the results by status `initialized`, `validating`, `active` or `failed`.
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
                in_use=in_use,
                status=status,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        in_use: Union[bool, object] = values.unset,
        status: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> SinkPage:
        """
        Retrieve a single page of SinkInstance records from the API.
        Request is executed immediately

        :param in_use: A boolean query parameter filtering the results to return sinks used/not used by a subscription.
        :param status: A String query parameter filtering the results by status `initialized`, `validating`, `active` or `failed`.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SinkInstance
        """
        data = values.of(
            {
                "InUse": in_use,
                "Status": status,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return SinkPage(self._version, response)

    async def page_async(
        self,
        in_use: Union[bool, object] = values.unset,
        status: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> SinkPage:
        """
        Asynchronously retrieve a single page of SinkInstance records from the API.
        Request is executed immediately

        :param in_use: A boolean query parameter filtering the results to return sinks used/not used by a subscription.
        :param status: A String query parameter filtering the results by status `initialized`, `validating`, `active` or `failed`.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SinkInstance
        """
        data = values.of(
            {
                "InUse": in_use,
                "Status": status,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return SinkPage(self._version, response)

    def get_page(self, target_url: str) -> SinkPage:
        """
        Retrieve a specific page of SinkInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SinkInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return SinkPage(self._version, response)

    async def get_page_async(self, target_url: str) -> SinkPage:
        """
        Asynchronously retrieve a specific page of SinkInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SinkInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return SinkPage(self._version, response)

    def get(self, sid: str) -> SinkContext:
        """
        Constructs a SinkContext

        :param sid: A 34 character string that uniquely identifies this Sink.
        """
        return SinkContext(self._version, sid=sid)

    def __call__(self, sid: str) -> SinkContext:
        """
        Constructs a SinkContext

        :param sid: A 34 character string that uniquely identifies this Sink.
        """
        return SinkContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Events.V1.SinkList>"
