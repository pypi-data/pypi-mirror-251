r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Flex
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import serialize, values

from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class InsightsSegmentsInstance(InstanceResource):

    """
    :ivar segment_id: To unique id of the segment
    :ivar external_id: The unique id for the conversation.
    :ivar queue:
    :ivar external_contact:
    :ivar external_segment_link_id: The uuid for the external_segment_link.
    :ivar date: The date of the conversation.
    :ivar account_id: The unique id for the account.
    :ivar external_segment_link: The hyperlink to recording of the task event.
    :ivar agent_id: The unique id for the agent.
    :ivar agent_phone: The phone number of the agent.
    :ivar agent_name: The name of the agent.
    :ivar agent_team_name: The team name to which agent belongs.
    :ivar agent_team_name_in_hierarchy: he team name to which agent belongs.
    :ivar agent_link: The link to the agent conversation.
    :ivar customer_phone: The phone number of the customer.
    :ivar customer_name: The name of the customer.
    :ivar customer_link: The link to the customer conversation.
    :ivar segment_recording_offset: The offset value for the recording.
    :ivar media: The media identifiers of the conversation.
    :ivar assessment_type: The type of the assessment.
    :ivar assessment_percentage: The percentage scored on the Assessments.
    :ivar url:
    """

    def __init__(self, version: Version, payload: Dict[str, Any]):
        super().__init__(version)

        self.segment_id: Optional[str] = payload.get("segment_id")
        self.external_id: Optional[str] = payload.get("external_id")
        self.queue: Optional[str] = payload.get("queue")
        self.external_contact: Optional[str] = payload.get("external_contact")
        self.external_segment_link_id: Optional[str] = payload.get(
            "external_segment_link_id"
        )
        self.date: Optional[str] = payload.get("date")
        self.account_id: Optional[str] = payload.get("account_id")
        self.external_segment_link: Optional[str] = payload.get("external_segment_link")
        self.agent_id: Optional[str] = payload.get("agent_id")
        self.agent_phone: Optional[str] = payload.get("agent_phone")
        self.agent_name: Optional[str] = payload.get("agent_name")
        self.agent_team_name: Optional[str] = payload.get("agent_team_name")
        self.agent_team_name_in_hierarchy: Optional[str] = payload.get(
            "agent_team_name_in_hierarchy"
        )
        self.agent_link: Optional[str] = payload.get("agent_link")
        self.customer_phone: Optional[str] = payload.get("customer_phone")
        self.customer_name: Optional[str] = payload.get("customer_name")
        self.customer_link: Optional[str] = payload.get("customer_link")
        self.segment_recording_offset: Optional[str] = payload.get(
            "segment_recording_offset"
        )
        self.media: Optional[Dict[str, object]] = payload.get("media")
        self.assessment_type: Optional[Dict[str, object]] = payload.get(
            "assessment_type"
        )
        self.assessment_percentage: Optional[Dict[str, object]] = payload.get(
            "assessment_percentage"
        )
        self.url: Optional[str] = payload.get("url")

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """

        return "<Twilio.FlexApi.V1.InsightsSegmentsInstance>"


class InsightsSegmentsPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> InsightsSegmentsInstance:
        """
        Build an instance of InsightsSegmentsInstance

        :param payload: Payload response from the API
        """
        return InsightsSegmentsInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.FlexApi.V1.InsightsSegmentsPage>"


class InsightsSegmentsList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the InsightsSegmentsList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/Insights/Segments"

    def stream(
        self,
        authorization: Union[str, object] = values.unset,
        segment_id: Union[str, object] = values.unset,
        reservation_id: Union[List[str], object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[InsightsSegmentsInstance]:
        """
        Streams InsightsSegmentsInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param str authorization: The Authorization HTTP request header
        :param str segment_id: To unique id of the segment
        :param List[str] reservation_id: The list of reservation Ids
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
            authorization=authorization,
            segment_id=segment_id,
            reservation_id=reservation_id,
            page_size=limits["page_size"],
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        authorization: Union[str, object] = values.unset,
        segment_id: Union[str, object] = values.unset,
        reservation_id: Union[List[str], object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[InsightsSegmentsInstance]:
        """
        Asynchronously streams InsightsSegmentsInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param str authorization: The Authorization HTTP request header
        :param str segment_id: To unique id of the segment
        :param List[str] reservation_id: The list of reservation Ids
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
            authorization=authorization,
            segment_id=segment_id,
            reservation_id=reservation_id,
            page_size=limits["page_size"],
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        authorization: Union[str, object] = values.unset,
        segment_id: Union[str, object] = values.unset,
        reservation_id: Union[List[str], object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[InsightsSegmentsInstance]:
        """
        Lists InsightsSegmentsInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param str authorization: The Authorization HTTP request header
        :param str segment_id: To unique id of the segment
        :param List[str] reservation_id: The list of reservation Ids
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
                authorization=authorization,
                segment_id=segment_id,
                reservation_id=reservation_id,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        authorization: Union[str, object] = values.unset,
        segment_id: Union[str, object] = values.unset,
        reservation_id: Union[List[str], object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[InsightsSegmentsInstance]:
        """
        Asynchronously lists InsightsSegmentsInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param str authorization: The Authorization HTTP request header
        :param str segment_id: To unique id of the segment
        :param List[str] reservation_id: The list of reservation Ids
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
                authorization=authorization,
                segment_id=segment_id,
                reservation_id=reservation_id,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        authorization: Union[str, object] = values.unset,
        segment_id: Union[str, object] = values.unset,
        reservation_id: Union[List[str], object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> InsightsSegmentsPage:
        """
        Retrieve a single page of InsightsSegmentsInstance records from the API.
        Request is executed immediately

        :param authorization: The Authorization HTTP request header
        :param segment_id: To unique id of the segment
        :param reservation_id: The list of reservation Ids
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of InsightsSegmentsInstance
        """
        data = values.of(
            {
                "Authorization": authorization,
                "SegmentId": segment_id,
                "ReservationId": serialize.map(reservation_id, lambda e: e),
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return InsightsSegmentsPage(self._version, response)

    async def page_async(
        self,
        authorization: Union[str, object] = values.unset,
        segment_id: Union[str, object] = values.unset,
        reservation_id: Union[List[str], object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> InsightsSegmentsPage:
        """
        Asynchronously retrieve a single page of InsightsSegmentsInstance records from the API.
        Request is executed immediately

        :param authorization: The Authorization HTTP request header
        :param segment_id: To unique id of the segment
        :param reservation_id: The list of reservation Ids
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of InsightsSegmentsInstance
        """
        data = values.of(
            {
                "Authorization": authorization,
                "SegmentId": segment_id,
                "ReservationId": serialize.map(reservation_id, lambda e: e),
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return InsightsSegmentsPage(self._version, response)

    def get_page(self, target_url: str) -> InsightsSegmentsPage:
        """
        Retrieve a specific page of InsightsSegmentsInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of InsightsSegmentsInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return InsightsSegmentsPage(self._version, response)

    async def get_page_async(self, target_url: str) -> InsightsSegmentsPage:
        """
        Asynchronously retrieve a specific page of InsightsSegmentsInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of InsightsSegmentsInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return InsightsSegmentsPage(self._version, response)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.FlexApi.V1.InsightsSegmentsList>"
