r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Trusthub
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class SupportingDocumentTypeInstance(InstanceResource):

    """
    :ivar sid: The unique string that identifies the Supporting Document Type resource.
    :ivar friendly_name: A human-readable description of the Supporting Document Type resource.
    :ivar machine_name: The machine-readable description of the Supporting Document Type resource.
    :ivar fields: The required information for creating a Supporting Document. The required fields will change as regulatory needs change and will differ for businesses and individuals.
    :ivar url: The absolute URL of the Supporting Document Type resource.
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.machine_name: Optional[str] = payload.get("machine_name")
        self.fields: Optional[List[Dict[str, object]]] = payload.get("fields")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "sid": sid or self.sid,
        }
        self._context: Optional[SupportingDocumentTypeContext] = None

    @property
    def _proxy(self) -> "SupportingDocumentTypeContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: SupportingDocumentTypeContext for this SupportingDocumentTypeInstance
        """
        if self._context is None:
            self._context = SupportingDocumentTypeContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def fetch(self) -> "SupportingDocumentTypeInstance":
        """
        Fetch the SupportingDocumentTypeInstance


        :returns: The fetched SupportingDocumentTypeInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "SupportingDocumentTypeInstance":
        """
        Asynchronous coroutine to fetch the SupportingDocumentTypeInstance


        :returns: The fetched SupportingDocumentTypeInstance
        """
        return await self._proxy.fetch_async()

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Trusthub.V1.SupportingDocumentTypeInstance {}>".format(context)


class SupportingDocumentTypeContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the SupportingDocumentTypeContext

        :param version: Version that contains the resource
        :param sid: The unique string that identifies the Supporting Document Type resource.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/SupportingDocumentTypes/{sid}".format(**self._solution)

    def fetch(self) -> SupportingDocumentTypeInstance:
        """
        Fetch the SupportingDocumentTypeInstance


        :returns: The fetched SupportingDocumentTypeInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return SupportingDocumentTypeInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> SupportingDocumentTypeInstance:
        """
        Asynchronous coroutine to fetch the SupportingDocumentTypeInstance


        :returns: The fetched SupportingDocumentTypeInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return SupportingDocumentTypeInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Trusthub.V1.SupportingDocumentTypeContext {}>".format(context)


class SupportingDocumentTypePage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> SupportingDocumentTypeInstance:
        """
        Build an instance of SupportingDocumentTypeInstance

        :param payload: Payload response from the API
        """
        return SupportingDocumentTypeInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Trusthub.V1.SupportingDocumentTypePage>"


class SupportingDocumentTypeList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the SupportingDocumentTypeList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/SupportingDocumentTypes"

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[SupportingDocumentTypeInstance]:
        """
        Streams SupportingDocumentTypeInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[SupportingDocumentTypeInstance]:
        """
        Asynchronously streams SupportingDocumentTypeInstance records from the API as a generator stream.
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
    ) -> List[SupportingDocumentTypeInstance]:
        """
        Lists SupportingDocumentTypeInstance records from the API as a list.
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
    ) -> List[SupportingDocumentTypeInstance]:
        """
        Asynchronously lists SupportingDocumentTypeInstance records from the API as a list.
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
    ) -> SupportingDocumentTypePage:
        """
        Retrieve a single page of SupportingDocumentTypeInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SupportingDocumentTypeInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return SupportingDocumentTypePage(self._version, response)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> SupportingDocumentTypePage:
        """
        Asynchronously retrieve a single page of SupportingDocumentTypeInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SupportingDocumentTypeInstance
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
        return SupportingDocumentTypePage(self._version, response)

    def get_page(self, target_url: str) -> SupportingDocumentTypePage:
        """
        Retrieve a specific page of SupportingDocumentTypeInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SupportingDocumentTypeInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return SupportingDocumentTypePage(self._version, response)

    async def get_page_async(self, target_url: str) -> SupportingDocumentTypePage:
        """
        Asynchronously retrieve a specific page of SupportingDocumentTypeInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SupportingDocumentTypeInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return SupportingDocumentTypePage(self._version, response)

    def get(self, sid: str) -> SupportingDocumentTypeContext:
        """
        Constructs a SupportingDocumentTypeContext

        :param sid: The unique string that identifies the Supporting Document Type resource.
        """
        return SupportingDocumentTypeContext(self._version, sid=sid)

    def __call__(self, sid: str) -> SupportingDocumentTypeContext:
        """
        Constructs a SupportingDocumentTypeContext

        :param sid: The unique string that identifies the Supporting Document Type resource.
        """
        return SupportingDocumentTypeContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Trusthub.V1.SupportingDocumentTypeList>"
