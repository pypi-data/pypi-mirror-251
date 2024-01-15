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
from twilio.rest.preview.sync.service.document.document_permission import (
    DocumentPermissionList,
)


class DocumentInstance(InstanceResource):

    """
    :ivar sid:
    :ivar unique_name:
    :ivar account_sid:
    :ivar service_sid:
    :ivar url:
    :ivar links:
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
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.unique_name: Optional[str] = payload.get("unique_name")
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.service_sid: Optional[str] = payload.get("service_sid")
        self.url: Optional[str] = payload.get("url")
        self.links: Optional[Dict[str, object]] = payload.get("links")
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
            "sid": sid or self.sid,
        }
        self._context: Optional[DocumentContext] = None

    @property
    def _proxy(self) -> "DocumentContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: DocumentContext for this DocumentInstance
        """
        if self._context is None:
            self._context = DocumentContext(
                self._version,
                service_sid=self._solution["service_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the DocumentInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the DocumentInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "DocumentInstance":
        """
        Fetch the DocumentInstance


        :returns: The fetched DocumentInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "DocumentInstance":
        """
        Asynchronous coroutine to fetch the DocumentInstance


        :returns: The fetched DocumentInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> "DocumentInstance":
        """
        Update the DocumentInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated DocumentInstance
        """
        return self._proxy.update(
            data=data,
            if_match=if_match,
        )

    async def update_async(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> "DocumentInstance":
        """
        Asynchronous coroutine to update the DocumentInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated DocumentInstance
        """
        return await self._proxy.update_async(
            data=data,
            if_match=if_match,
        )

    @property
    def document_permissions(self) -> DocumentPermissionList:
        """
        Access the document_permissions
        """
        return self._proxy.document_permissions

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Preview.Sync.DocumentInstance {}>".format(context)


class DocumentContext(InstanceContext):
    def __init__(self, version: Version, service_sid: str, sid: str):
        """
        Initialize the DocumentContext

        :param version: Version that contains the resource
        :param service_sid:
        :param sid:
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "service_sid": service_sid,
            "sid": sid,
        }
        self._uri = "/Services/{service_sid}/Documents/{sid}".format(**self._solution)

        self._document_permissions: Optional[DocumentPermissionList] = None

    def delete(self) -> bool:
        """
        Deletes the DocumentInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the DocumentInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> DocumentInstance:
        """
        Fetch the DocumentInstance


        :returns: The fetched DocumentInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return DocumentInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> DocumentInstance:
        """
        Asynchronous coroutine to fetch the DocumentInstance


        :returns: The fetched DocumentInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return DocumentInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            sid=self._solution["sid"],
        )

    def update(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> DocumentInstance:
        """
        Update the DocumentInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated DocumentInstance
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

        return DocumentInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            sid=self._solution["sid"],
        )

    async def update_async(
        self, data: object, if_match: Union[str, object] = values.unset
    ) -> DocumentInstance:
        """
        Asynchronous coroutine to update the DocumentInstance

        :param data:
        :param if_match: The If-Match HTTP request header

        :returns: The updated DocumentInstance
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

        return DocumentInstance(
            self._version,
            payload,
            service_sid=self._solution["service_sid"],
            sid=self._solution["sid"],
        )

    @property
    def document_permissions(self) -> DocumentPermissionList:
        """
        Access the document_permissions
        """
        if self._document_permissions is None:
            self._document_permissions = DocumentPermissionList(
                self._version,
                self._solution["service_sid"],
                self._solution["sid"],
            )
        return self._document_permissions

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Preview.Sync.DocumentContext {}>".format(context)


class DocumentPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> DocumentInstance:
        """
        Build an instance of DocumentInstance

        :param payload: Payload response from the API
        """
        return DocumentInstance(
            self._version, payload, service_sid=self._solution["service_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Preview.Sync.DocumentPage>"


class DocumentList(ListResource):
    def __init__(self, version: Version, service_sid: str):
        """
        Initialize the DocumentList

        :param version: Version that contains the resource
        :param service_sid:

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "service_sid": service_sid,
        }
        self._uri = "/Services/{service_sid}/Documents".format(**self._solution)

    def create(
        self,
        unique_name: Union[str, object] = values.unset,
        data: Union[object, object] = values.unset,
    ) -> DocumentInstance:
        """
        Create the DocumentInstance

        :param unique_name:
        :param data:

        :returns: The created DocumentInstance
        """

        data = values.of(
            {
                "UniqueName": unique_name,
                "Data": serialize.object(data),
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return DocumentInstance(
            self._version, payload, service_sid=self._solution["service_sid"]
        )

    async def create_async(
        self,
        unique_name: Union[str, object] = values.unset,
        data: Union[object, object] = values.unset,
    ) -> DocumentInstance:
        """
        Asynchronously create the DocumentInstance

        :param unique_name:
        :param data:

        :returns: The created DocumentInstance
        """

        data = values.of(
            {
                "UniqueName": unique_name,
                "Data": serialize.object(data),
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return DocumentInstance(
            self._version, payload, service_sid=self._solution["service_sid"]
        )

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[DocumentInstance]:
        """
        Streams DocumentInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[DocumentInstance]:
        """
        Asynchronously streams DocumentInstance records from the API as a generator stream.
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
    ) -> List[DocumentInstance]:
        """
        Lists DocumentInstance records from the API as a list.
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
    ) -> List[DocumentInstance]:
        """
        Asynchronously lists DocumentInstance records from the API as a list.
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
    ) -> DocumentPage:
        """
        Retrieve a single page of DocumentInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of DocumentInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return DocumentPage(self._version, response, self._solution)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> DocumentPage:
        """
        Asynchronously retrieve a single page of DocumentInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of DocumentInstance
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
        return DocumentPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> DocumentPage:
        """
        Retrieve a specific page of DocumentInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of DocumentInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return DocumentPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> DocumentPage:
        """
        Asynchronously retrieve a specific page of DocumentInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of DocumentInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return DocumentPage(self._version, response, self._solution)

    def get(self, sid: str) -> DocumentContext:
        """
        Constructs a DocumentContext

        :param sid:
        """
        return DocumentContext(
            self._version, service_sid=self._solution["service_sid"], sid=sid
        )

    def __call__(self, sid: str) -> DocumentContext:
        """
        Constructs a DocumentContext

        :param sid:
        """
        return DocumentContext(
            self._version, service_sid=self._solution["service_sid"], sid=sid
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Preview.Sync.DocumentList>"
