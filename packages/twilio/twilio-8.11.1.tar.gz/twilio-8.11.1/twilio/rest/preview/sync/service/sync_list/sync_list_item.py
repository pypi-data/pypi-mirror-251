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


from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import deserialize, serialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class SyncListItemInstance(InstanceResource):
    class QueryFromBoundType(object):
        INCLUSIVE = "inclusive"
        EXCLUSIVE = "exclusive"

    class QueryResultOrder(object):
        ASC = "asc"
        DESC = "desc"

    """
    :ivar index: 
    :ivar account_sid: 
    :ivar service_sid: 
    :ivar list_sid: 
    :ivar url: 
    :ivar revision: 
    :ivar data: 
    :ivar date_created: 
    :ivar date_updated: 
    :ivar created_by: 
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        service_sid: str,
        list_sid: str,
        index: Optional[int] = None,
    ):
        super().__init__(version)

        self.index: Optional[int] = deserialize.integer(payload.get("index"))
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.service_sid: Optional[str] = payload.get("service_sid")
        self.list_sid: Optional[str] = payload.get("list_sid")
        self.url: Optional[str] = payload.get("url")
        self.revision: Optional[str] = payload.get("revision")
        self.data: Optional[Dict[str, object]] = payload.get("data")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.created_by: Optional[str] = payload.get("created_by")

        self._solution = {
            "service_sid": service_sid,
            "list_sid": list_sid,
            "index": index or self.index,
        }
        self._context: Optional[SyncListItemContext] = None

    @property
    def _proxy(self) -> "SyncListItemContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: SyncListItemContext for this SyncListItemInstance
        """
        if self._context is None:
            self._context = SyncListItemContext(
                self._version,
                service_sid=self._solution["service_sid"],
                list_sid=self._solution["list_sid"],
                index=self._solution["index"],
            )
        return self._context

    def delete(self, if_match: Union[str, object] = values.unset) -> bool:
        """
        Deletes the SyncListItemInstance

        :param if_match: The If-Match HTTP request header

        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete(
            if_match=if_match,
        )

    async def delete_async(self, if_match: Union[str, object] = values.unset) -> bool:
        """
        Asynchronous coroutine that deletes the SyncListItemInstance

        :param if_match: The If-Match HTTP request header

        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async(
            if_match=if_match,
        )

    def fetch(self) -> "SyncListItemInstance":
        """
        Fetch the SyncListItemInstance


        :returns: The fetched SyncListItemInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "SyncListItemInstance":
        """
        Asynchronous coroutine to fetch the SyncListItemInstance


        :returns: The fetched SyncListItemInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> "SyncListItemInstance":
        """
        Update the SyncListItemInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated SyncListItemInstance
        """
        return self._proxy.update(
            data=data,
            if_match=if_match,
        )

    async def update_async(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> "SyncListItemInstance":
        """
        Asynchronous coroutine to update the SyncListItemInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated SyncListItemInstance
        """
        return await self._proxy.update_async(
            data=data,
            if_match=if_match,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Preview.Sync.SyncListItemInstance {}>".format(context)


class SyncListItemContext(InstanceContext):
    def __init__(self, version: Version, service_sid: str, list_sid: str, index: int):
        """
        Initialize the SyncListItemContext

        :param version: Version that contains the resource
        :param service_sid:
        :param list_sid:
        :param index:
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "service_sid": service_sid,
            "list_sid": list_sid,
            "index": index,
        }
        self._uri = "/Services/{service_sid}/Lists/{list_sid}/Items/{index}".format(
            **self._solution
        )

    def delete(self, if_match: Union[str, object] = values.unset) -> bool:
        """
        Deletes the SyncListItemInstance

        :param if_match: The If-Match HTTP request header

        :returns: True if delete succeeds, False otherwise
        """
        headers = values.of(
            {
                "If-Match": if_match,
            }
        )

        return self._version.delete(method="DELETE", uri=self._uri, headers=headers)

    async def delete_async(self, if_match: Union[str, object] = values.unset) -> bool:
        """
        Asynchronous coroutine that deletes the SyncListItemInstance

        :param if_match: The If-Match HTTP request header

        :returns: True if delete succeeds, False otherwise
        """
        headers = values.of(
            {
                "If-Match": if_match,
            }
        )

        return await self._version.delete_async(
            method="DELETE", uri=self._uri, headers=headers
        )

    def fetch(self) -> SyncListItemInstance:
        """
        Fetch the SyncListItemInstance


        :returns: The fetched SyncListItemInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
            index=self._solution["index"],
        )

    async def fetch_async(self) -> SyncListItemInstance:
        """
        Asynchronous coroutine to fetch the SyncListItemInstance


        :returns: The fetched SyncListItemInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
            index=self._solution["index"],
        )

    def update(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> SyncListItemInstance:
        """
        Update the SyncListItemInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated SyncListItemInstance
        """
        data = values.of(
            {
                "Data": serialize.object(data),
            }
        )
        headers = values.of(
            {
                "If-Match": if_match,
            }
        )

        payload = self._version.update(
            method="POST", uri=self._uri, data=data, headers=headers
        )

        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
            index=self._solution["index"],
        )

    async def update_async(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> SyncListItemInstance:
        """
        Asynchronous coroutine to update the SyncListItemInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated SyncListItemInstance
        """
        data = values.of(
            {
                "Data": serialize.object(data),
            }
        )
        headers = values.of(
            {
                "If-Match": if_match,
            }
        )

        payload = await self._version.update_async(
            method="POST", uri=self._uri, data=data, headers=headers
        )

        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
            index=self._solution["index"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Preview.Sync.SyncListItemContext {}>".format(context)


class SyncListItemPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> SyncListItemInstance:
        """
        Build an instance of SyncListItemInstance

        :param payload: Payload response from the API
        """
        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Preview.Sync.SyncListItemPage>"


class SyncListItemList(ListResource):
    def __init__(self, version: Version, service_sid: str, list_sid: str):
        """
        Initialize the SyncListItemList

        :param version: Version that contains the resource
        :param service_sid:
        :param list_sid:

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "service_sid": service_sid,
            "list_sid": list_sid,
        }
        self._uri = "/Services/{service_sid}/Lists/{list_sid}/Items".format(
            **self._solution
        )

    def create(self, data: object) -> SyncListItemInstance:
        """
        Create the SyncListItemInstance

        :param data:

        :returns: The created SyncListItemInstance
        """

        data = values.of(
            {
                "Data": serialize.object(data),
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
        )

    async def create_async(self, data: object) -> SyncListItemInstance:
        """
        Asynchronously create the SyncListItemInstance

        :param data:

        :returns: The created SyncListItemInstance
        """

        data = values.of(
            {
                "Data": serialize.object(data),
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return SyncListItemInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
        )

    def stream(
        self,
        order: Union["SyncListItemInstance.QueryResultOrder", object] = values.unset,
        from_: Union[str, object] = values.unset,
        bounds: Union["SyncListItemInstance.QueryFromBoundType", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[SyncListItemInstance]:
        """
        Streams SyncListItemInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param &quot;SyncListItemInstance.QueryResultOrder&quot; order:
        :param str from_:
        :param &quot;SyncListItemInstance.QueryFromBoundType&quot; bounds:
        :param limit: Upper limit for the number of records to return. stream()
                      guarantees to never return more than limit.  Default is no limit
        :param page_size: Number of records to fetch per request, when not set will use
                          the default value of 50 records.  If no page_size is defined
                          but a limit is defined, stream() will attempt to read the
                          limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        """
        limits = self._version.read_limits(limit, page_size)
        page = self.page(
            order=order, from_=from_, bounds=bounds, page_size=limits["page_size"]
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        order: Union["SyncListItemInstance.QueryResultOrder", object] = values.unset,
        from_: Union[str, object] = values.unset,
        bounds: Union["SyncListItemInstance.QueryFromBoundType", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[SyncListItemInstance]:
        """
        Asynchronously streams SyncListItemInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param &quot;SyncListItemInstance.QueryResultOrder&quot; order:
        :param str from_:
        :param &quot;SyncListItemInstance.QueryFromBoundType&quot; bounds:
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
            order=order, from_=from_, bounds=bounds, page_size=limits["page_size"]
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        order: Union["SyncListItemInstance.QueryResultOrder", object] = values.unset,
        from_: Union[str, object] = values.unset,
        bounds: Union["SyncListItemInstance.QueryFromBoundType", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[SyncListItemInstance]:
        """
        Lists SyncListItemInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param &quot;SyncListItemInstance.QueryResultOrder&quot; order:
        :param str from_:
        :param &quot;SyncListItemInstance.QueryFromBoundType&quot; bounds:
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
                order=order,
                from_=from_,
                bounds=bounds,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        order: Union["SyncListItemInstance.QueryResultOrder", object] = values.unset,
        from_: Union[str, object] = values.unset,
        bounds: Union["SyncListItemInstance.QueryFromBoundType", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[SyncListItemInstance]:
        """
        Asynchronously lists SyncListItemInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param &quot;SyncListItemInstance.QueryResultOrder&quot; order:
        :param str from_:
        :param &quot;SyncListItemInstance.QueryFromBoundType&quot; bounds:
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
                order=order,
                from_=from_,
                bounds=bounds,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        order: Union["SyncListItemInstance.QueryResultOrder", object] = values.unset,
        from_: Union[str, object] = values.unset,
        bounds: Union["SyncListItemInstance.QueryFromBoundType", object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> SyncListItemPage:
        """
        Retrieve a single page of SyncListItemInstance records from the API.
        Request is executed immediately

        :param order:
        :param from_:
        :param bounds:
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SyncListItemInstance
        """
        data = values.of(
            {
                "Order": order,
                "From": from_,
                "Bounds": bounds,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return SyncListItemPage(self._version, response, self._solution)

    async def page_async(
        self,
        order: Union["SyncListItemInstance.QueryResultOrder", object] = values.unset,
        from_: Union[str, object] = values.unset,
        bounds: Union["SyncListItemInstance.QueryFromBoundType", object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> SyncListItemPage:
        """
        Asynchronously retrieve a single page of SyncListItemInstance records from the API.
        Request is executed immediately

        :param order:
        :param from_:
        :param bounds:
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SyncListItemInstance
        """
        data = values.of(
            {
                "Order": order,
                "From": from_,
                "Bounds": bounds,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return SyncListItemPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> SyncListItemPage:
        """
        Retrieve a specific page of SyncListItemInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SyncListItemInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return SyncListItemPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> SyncListItemPage:
        """
        Asynchronously retrieve a specific page of SyncListItemInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SyncListItemInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return SyncListItemPage(self._version, response, self._solution)

    def get(self, index: int) -> SyncListItemContext:
        """
        Constructs a SyncListItemContext

        :param index:
        """
        return SyncListItemContext(
            self._version,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
            index=index,
        )

    def __call__(self, index: int) -> SyncListItemContext:
        """
        Constructs a SyncListItemContext

        :param index:
        """
        return SyncListItemContext(
            self._version,
            service_sid=self._solution["service_sid"],
            list_sid=self._solution["list_sid"],
            index=index,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Preview.Sync.SyncListItemList>"
