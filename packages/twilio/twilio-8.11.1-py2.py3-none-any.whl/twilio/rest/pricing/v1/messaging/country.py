r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Pricing
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


class CountryInstance(InstanceResource):

    """
    :ivar country: The name of the country.
    :ivar iso_country: The [ISO country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    :ivar outbound_sms_prices: The list of [OutboundSMSPrice](https://www.twilio.com/docs/sms/api/pricing#outbound-sms-price) records that represent the price to send a message for each MCC/MNC applicable in this country.
    :ivar inbound_sms_prices: The list of [InboundPrice](https://www.twilio.com/docs/sms/api/pricing#inbound-price) records that describe the price to receive an inbound SMS to the different Twilio phone number types supported in this country
    :ivar price_unit: The currency in which prices are measured, specified in [ISO 4127](http://www.iso.org/iso/home/standards/currency_codes.htm) format (e.g. `usd`, `eur`, `jpy`).
    :ivar url: The absolute URL of the resource.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        iso_country: Optional[str] = None,
    ):
        super().__init__(version)

        self.country: Optional[str] = payload.get("country")
        self.iso_country: Optional[str] = payload.get("iso_country")
        self.outbound_sms_prices: Optional[List[str]] = payload.get(
            "outbound_sms_prices"
        )
        self.inbound_sms_prices: Optional[List[str]] = payload.get("inbound_sms_prices")
        self.price_unit: Optional[str] = payload.get("price_unit")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "iso_country": iso_country or self.iso_country,
        }
        self._context: Optional[CountryContext] = None

    @property
    def _proxy(self) -> "CountryContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: CountryContext for this CountryInstance
        """
        if self._context is None:
            self._context = CountryContext(
                self._version,
                iso_country=self._solution["iso_country"],
            )
        return self._context

    def fetch(self) -> "CountryInstance":
        """
        Fetch the CountryInstance


        :returns: The fetched CountryInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "CountryInstance":
        """
        Asynchronous coroutine to fetch the CountryInstance


        :returns: The fetched CountryInstance
        """
        return await self._proxy.fetch_async()

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Pricing.V1.CountryInstance {}>".format(context)


class CountryContext(InstanceContext):
    def __init__(self, version: Version, iso_country: str):
        """
        Initialize the CountryContext

        :param version: Version that contains the resource
        :param iso_country: The [ISO country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the pricing information to fetch.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "iso_country": iso_country,
        }
        self._uri = "/Messaging/Countries/{iso_country}".format(**self._solution)

    def fetch(self) -> CountryInstance:
        """
        Fetch the CountryInstance


        :returns: The fetched CountryInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return CountryInstance(
            self._version,
            payload,
            iso_country=self._solution["iso_country"],
        )

    async def fetch_async(self) -> CountryInstance:
        """
        Asynchronous coroutine to fetch the CountryInstance


        :returns: The fetched CountryInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return CountryInstance(
            self._version,
            payload,
            iso_country=self._solution["iso_country"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Pricing.V1.CountryContext {}>".format(context)


class CountryPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> CountryInstance:
        """
        Build an instance of CountryInstance

        :param payload: Payload response from the API
        """
        return CountryInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Pricing.V1.CountryPage>"


class CountryList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the CountryList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/Messaging/Countries"

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[CountryInstance]:
        """
        Streams CountryInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[CountryInstance]:
        """
        Asynchronously streams CountryInstance records from the API as a generator stream.
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
    ) -> List[CountryInstance]:
        """
        Lists CountryInstance records from the API as a list.
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
    ) -> List[CountryInstance]:
        """
        Asynchronously lists CountryInstance records from the API as a list.
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
    ) -> CountryPage:
        """
        Retrieve a single page of CountryInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of CountryInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return CountryPage(self._version, response)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> CountryPage:
        """
        Asynchronously retrieve a single page of CountryInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of CountryInstance
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
        return CountryPage(self._version, response)

    def get_page(self, target_url: str) -> CountryPage:
        """
        Retrieve a specific page of CountryInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of CountryInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return CountryPage(self._version, response)

    async def get_page_async(self, target_url: str) -> CountryPage:
        """
        Asynchronously retrieve a specific page of CountryInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of CountryInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return CountryPage(self._version, response)

    def get(self, iso_country: str) -> CountryContext:
        """
        Constructs a CountryContext

        :param iso_country: The [ISO country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the pricing information to fetch.
        """
        return CountryContext(self._version, iso_country=iso_country)

    def __call__(self, iso_country: str) -> CountryContext:
        """
        Constructs a CountryContext

        :param iso_country: The [ISO country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the pricing information to fetch.
        """
        return CountryContext(self._version, iso_country=iso_country)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Pricing.V1.CountryList>"
