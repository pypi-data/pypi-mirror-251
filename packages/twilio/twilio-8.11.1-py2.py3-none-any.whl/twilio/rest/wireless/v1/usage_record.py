r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Wireless
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import serialize, values

from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class UsageRecordInstance(InstanceResource):
    class Granularity(object):
        HOURLY = "hourly"
        DAILY = "daily"
        ALL = "all"

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the AccountUsageRecord resource.
    :ivar period: The time period for which usage is reported. Contains `start` and `end` properties that describe the period using GMT date-time values specified in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format.
    :ivar commands: An object that describes the aggregated Commands usage for all SIMs during the specified period. See [Commands Usage Object](https://www.twilio.com/docs/iot/wireless/api/account-usagerecord-resource#commands-usage-object).
    :ivar data: An object that describes the aggregated Data usage for all SIMs over the period. See [Data Usage Object](https://www.twilio.com/docs/iot/wireless/api/account-usagerecord-resource#data-usage-object).
    """

    def __init__(self, version: Version, payload: Dict[str, Any]):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.period: Optional[Dict[str, object]] = payload.get("period")
        self.commands: Optional[Dict[str, object]] = payload.get("commands")
        self.data: Optional[Dict[str, object]] = payload.get("data")

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """

        return "<Twilio.Wireless.V1.UsageRecordInstance>"


class UsageRecordPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> UsageRecordInstance:
        """
        Build an instance of UsageRecordInstance

        :param payload: Payload response from the API
        """
        return UsageRecordInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Wireless.V1.UsageRecordPage>"


class UsageRecordList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the UsageRecordList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/UsageRecords"

    def stream(
        self,
        end: Union[datetime, object] = values.unset,
        start: Union[datetime, object] = values.unset,
        granularity: Union["UsageRecordInstance.Granularity", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[UsageRecordInstance]:
        """
        Streams UsageRecordInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param datetime end: Only include usage that has occurred on or before this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param datetime start: Only include usage that has occurred on or after this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param &quot;UsageRecordInstance.Granularity&quot; granularity: How to summarize the usage by time. Can be: `daily`, `hourly`, or `all`. A value of `all` returns one Usage Record that describes the usage for the entire period.
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
            end=end, start=start, granularity=granularity, page_size=limits["page_size"]
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        end: Union[datetime, object] = values.unset,
        start: Union[datetime, object] = values.unset,
        granularity: Union["UsageRecordInstance.Granularity", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[UsageRecordInstance]:
        """
        Asynchronously streams UsageRecordInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param datetime end: Only include usage that has occurred on or before this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param datetime start: Only include usage that has occurred on or after this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param &quot;UsageRecordInstance.Granularity&quot; granularity: How to summarize the usage by time. Can be: `daily`, `hourly`, or `all`. A value of `all` returns one Usage Record that describes the usage for the entire period.
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
            end=end, start=start, granularity=granularity, page_size=limits["page_size"]
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        end: Union[datetime, object] = values.unset,
        start: Union[datetime, object] = values.unset,
        granularity: Union["UsageRecordInstance.Granularity", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[UsageRecordInstance]:
        """
        Lists UsageRecordInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param datetime end: Only include usage that has occurred on or before this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param datetime start: Only include usage that has occurred on or after this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param &quot;UsageRecordInstance.Granularity&quot; granularity: How to summarize the usage by time. Can be: `daily`, `hourly`, or `all`. A value of `all` returns one Usage Record that describes the usage for the entire period.
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
                end=end,
                start=start,
                granularity=granularity,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        end: Union[datetime, object] = values.unset,
        start: Union[datetime, object] = values.unset,
        granularity: Union["UsageRecordInstance.Granularity", object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[UsageRecordInstance]:
        """
        Asynchronously lists UsageRecordInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param datetime end: Only include usage that has occurred on or before this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param datetime start: Only include usage that has occurred on or after this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param &quot;UsageRecordInstance.Granularity&quot; granularity: How to summarize the usage by time. Can be: `daily`, `hourly`, or `all`. A value of `all` returns one Usage Record that describes the usage for the entire period.
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
                end=end,
                start=start,
                granularity=granularity,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        end: Union[datetime, object] = values.unset,
        start: Union[datetime, object] = values.unset,
        granularity: Union["UsageRecordInstance.Granularity", object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> UsageRecordPage:
        """
        Retrieve a single page of UsageRecordInstance records from the API.
        Request is executed immediately

        :param end: Only include usage that has occurred on or before this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param start: Only include usage that has occurred on or after this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param granularity: How to summarize the usage by time. Can be: `daily`, `hourly`, or `all`. A value of `all` returns one Usage Record that describes the usage for the entire period.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of UsageRecordInstance
        """
        data = values.of(
            {
                "End": serialize.iso8601_datetime(end),
                "Start": serialize.iso8601_datetime(start),
                "Granularity": granularity,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return UsageRecordPage(self._version, response)

    async def page_async(
        self,
        end: Union[datetime, object] = values.unset,
        start: Union[datetime, object] = values.unset,
        granularity: Union["UsageRecordInstance.Granularity", object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> UsageRecordPage:
        """
        Asynchronously retrieve a single page of UsageRecordInstance records from the API.
        Request is executed immediately

        :param end: Only include usage that has occurred on or before this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param start: Only include usage that has occurred on or after this date. Format is [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).
        :param granularity: How to summarize the usage by time. Can be: `daily`, `hourly`, or `all`. A value of `all` returns one Usage Record that describes the usage for the entire period.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of UsageRecordInstance
        """
        data = values.of(
            {
                "End": serialize.iso8601_datetime(end),
                "Start": serialize.iso8601_datetime(start),
                "Granularity": granularity,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return UsageRecordPage(self._version, response)

    def get_page(self, target_url: str) -> UsageRecordPage:
        """
        Retrieve a specific page of UsageRecordInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of UsageRecordInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return UsageRecordPage(self._version, response)

    async def get_page_async(self, target_url: str) -> UsageRecordPage:
        """
        Asynchronously retrieve a specific page of UsageRecordInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of UsageRecordInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return UsageRecordPage(self._version, response)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Wireless.V1.UsageRecordList>"
