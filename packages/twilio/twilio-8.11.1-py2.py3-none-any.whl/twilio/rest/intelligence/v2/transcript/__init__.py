r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Intelligence
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
from twilio.rest.intelligence.v2.transcript.media import MediaList
from twilio.rest.intelligence.v2.transcript.operator_result import OperatorResultList
from twilio.rest.intelligence.v2.transcript.sentence import SentenceList


class TranscriptInstance(InstanceResource):
    class Status(object):
        QUEUED = "queued"
        IN_PROGRESS = "in-progress"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELED = "canceled"

    """
    :ivar account_sid: The unique SID identifier of the Account.
    :ivar service_sid: The unique SID identifier of the Service.
    :ivar sid: A 34 character string that uniquely identifies this Transcript.
    :ivar date_created: The date that this Transcript was created, given in ISO 8601 format.
    :ivar date_updated: The date that this Transcript was updated, given in ISO 8601 format.
    :ivar status: 
    :ivar channel: Media Channel describing Transcript Source and Participant Mapping
    :ivar data_logging: Data logging allows Twilio to improve the quality of the speech recognition & language understanding services through using customer data to refine, fine tune and evaluate machine learning models. Note: Data logging cannot be activated via API, only via www.twilio.com, as it requires additional consent.
    :ivar language_code: The default language code of the audio.
    :ivar customer_key: 
    :ivar media_start_time: The date that this Transcript's media was started, given in ISO 8601 format.
    :ivar duration: The duration of this Transcript's source
    :ivar url: The URL of this resource.
    :ivar redaction: If the transcript has been redacted, a redacted alternative of the transcript will be available.
    :ivar links: 
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.service_sid: Optional[str] = payload.get("service_sid")
        self.sid: Optional[str] = payload.get("sid")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.status: Optional["TranscriptInstance.Status"] = payload.get("status")
        self.channel: Optional[Dict[str, object]] = payload.get("channel")
        self.data_logging: Optional[bool] = payload.get("data_logging")
        self.language_code: Optional[str] = payload.get("language_code")
        self.customer_key: Optional[str] = payload.get("customer_key")
        self.media_start_time: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("media_start_time")
        )
        self.duration: Optional[int] = deserialize.integer(payload.get("duration"))
        self.url: Optional[str] = payload.get("url")
        self.redaction: Optional[bool] = payload.get("redaction")
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "sid": sid or self.sid,
        }
        self._context: Optional[TranscriptContext] = None

    @property
    def _proxy(self) -> "TranscriptContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: TranscriptContext for this TranscriptInstance
        """
        if self._context is None:
            self._context = TranscriptContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the TranscriptInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the TranscriptInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "TranscriptInstance":
        """
        Fetch the TranscriptInstance


        :returns: The fetched TranscriptInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "TranscriptInstance":
        """
        Asynchronous coroutine to fetch the TranscriptInstance


        :returns: The fetched TranscriptInstance
        """
        return await self._proxy.fetch_async()

    @property
    def media(self) -> MediaList:
        """
        Access the media
        """
        return self._proxy.media

    @property
    def operator_results(self) -> OperatorResultList:
        """
        Access the operator_results
        """
        return self._proxy.operator_results

    @property
    def sentences(self) -> SentenceList:
        """
        Access the sentences
        """
        return self._proxy.sentences

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Intelligence.V2.TranscriptInstance {}>".format(context)


class TranscriptContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the TranscriptContext

        :param version: Version that contains the resource
        :param sid: A 34 character string that uniquely identifies this Transcript.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/Transcripts/{sid}".format(**self._solution)

        self._media: Optional[MediaList] = None
        self._operator_results: Optional[OperatorResultList] = None
        self._sentences: Optional[SentenceList] = None

    def delete(self) -> bool:
        """
        Deletes the TranscriptInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the TranscriptInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> TranscriptInstance:
        """
        Fetch the TranscriptInstance


        :returns: The fetched TranscriptInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return TranscriptInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> TranscriptInstance:
        """
        Asynchronous coroutine to fetch the TranscriptInstance


        :returns: The fetched TranscriptInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return TranscriptInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    @property
    def media(self) -> MediaList:
        """
        Access the media
        """
        if self._media is None:
            self._media = MediaList(
                self._version,
                self._solution["sid"],
            )
        return self._media

    @property
    def operator_results(self) -> OperatorResultList:
        """
        Access the operator_results
        """
        if self._operator_results is None:
            self._operator_results = OperatorResultList(
                self._version,
                self._solution["sid"],
            )
        return self._operator_results

    @property
    def sentences(self) -> SentenceList:
        """
        Access the sentences
        """
        if self._sentences is None:
            self._sentences = SentenceList(
                self._version,
                self._solution["sid"],
            )
        return self._sentences

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Intelligence.V2.TranscriptContext {}>".format(context)


class TranscriptPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> TranscriptInstance:
        """
        Build an instance of TranscriptInstance

        :param payload: Payload response from the API
        """
        return TranscriptInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Intelligence.V2.TranscriptPage>"


class TranscriptList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the TranscriptList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/Transcripts"

    def create(
        self,
        service_sid: str,
        channel: object,
        customer_key: Union[str, object] = values.unset,
        media_start_time: Union[datetime, object] = values.unset,
    ) -> TranscriptInstance:
        """
        Create the TranscriptInstance

        :param service_sid: The unique SID identifier of the Service.
        :param channel: JSON object describing Media Channel including Source and Participants
        :param customer_key: Used to store client provided metadata. Maximum of 64 double-byte UTF8 characters.
        :param media_start_time: The date that this Transcript's media was started, given in ISO 8601 format.

        :returns: The created TranscriptInstance
        """

        data = values.of(
            {
                "ServiceSid": service_sid,
                "Channel": serialize.object(channel),
                "CustomerKey": customer_key,
                "MediaStartTime": serialize.iso8601_datetime(media_start_time),
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TranscriptInstance(self._version, payload)

    async def create_async(
        self,
        service_sid: str,
        channel: object,
        customer_key: Union[str, object] = values.unset,
        media_start_time: Union[datetime, object] = values.unset,
    ) -> TranscriptInstance:
        """
        Asynchronously create the TranscriptInstance

        :param service_sid: The unique SID identifier of the Service.
        :param channel: JSON object describing Media Channel including Source and Participants
        :param customer_key: Used to store client provided metadata. Maximum of 64 double-byte UTF8 characters.
        :param media_start_time: The date that this Transcript's media was started, given in ISO 8601 format.

        :returns: The created TranscriptInstance
        """

        data = values.of(
            {
                "ServiceSid": service_sid,
                "Channel": serialize.object(channel),
                "CustomerKey": customer_key,
                "MediaStartTime": serialize.iso8601_datetime(media_start_time),
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TranscriptInstance(self._version, payload)

    def stream(
        self,
        service_sid: Union[str, object] = values.unset,
        before_start_time: Union[str, object] = values.unset,
        after_start_time: Union[str, object] = values.unset,
        before_date_created: Union[str, object] = values.unset,
        after_date_created: Union[str, object] = values.unset,
        status: Union[str, object] = values.unset,
        language_code: Union[str, object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[TranscriptInstance]:
        """
        Streams TranscriptInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param str service_sid: The unique SID identifier of the Service.
        :param str before_start_time: Filter by before StartTime.
        :param str after_start_time: Filter by after StartTime.
        :param str before_date_created: Filter by before DateCreated.
        :param str after_date_created: Filter by after DateCreated.
        :param str status: Filter by status.
        :param str language_code: Filter by Language Code.
        :param str source_sid: Filter by SourceSid.
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
            service_sid=service_sid,
            before_start_time=before_start_time,
            after_start_time=after_start_time,
            before_date_created=before_date_created,
            after_date_created=after_date_created,
            status=status,
            language_code=language_code,
            source_sid=source_sid,
            page_size=limits["page_size"],
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        service_sid: Union[str, object] = values.unset,
        before_start_time: Union[str, object] = values.unset,
        after_start_time: Union[str, object] = values.unset,
        before_date_created: Union[str, object] = values.unset,
        after_date_created: Union[str, object] = values.unset,
        status: Union[str, object] = values.unset,
        language_code: Union[str, object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[TranscriptInstance]:
        """
        Asynchronously streams TranscriptInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param str service_sid: The unique SID identifier of the Service.
        :param str before_start_time: Filter by before StartTime.
        :param str after_start_time: Filter by after StartTime.
        :param str before_date_created: Filter by before DateCreated.
        :param str after_date_created: Filter by after DateCreated.
        :param str status: Filter by status.
        :param str language_code: Filter by Language Code.
        :param str source_sid: Filter by SourceSid.
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
            service_sid=service_sid,
            before_start_time=before_start_time,
            after_start_time=after_start_time,
            before_date_created=before_date_created,
            after_date_created=after_date_created,
            status=status,
            language_code=language_code,
            source_sid=source_sid,
            page_size=limits["page_size"],
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        service_sid: Union[str, object] = values.unset,
        before_start_time: Union[str, object] = values.unset,
        after_start_time: Union[str, object] = values.unset,
        before_date_created: Union[str, object] = values.unset,
        after_date_created: Union[str, object] = values.unset,
        status: Union[str, object] = values.unset,
        language_code: Union[str, object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[TranscriptInstance]:
        """
        Lists TranscriptInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param str service_sid: The unique SID identifier of the Service.
        :param str before_start_time: Filter by before StartTime.
        :param str after_start_time: Filter by after StartTime.
        :param str before_date_created: Filter by before DateCreated.
        :param str after_date_created: Filter by after DateCreated.
        :param str status: Filter by status.
        :param str language_code: Filter by Language Code.
        :param str source_sid: Filter by SourceSid.
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
                service_sid=service_sid,
                before_start_time=before_start_time,
                after_start_time=after_start_time,
                before_date_created=before_date_created,
                after_date_created=after_date_created,
                status=status,
                language_code=language_code,
                source_sid=source_sid,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        service_sid: Union[str, object] = values.unset,
        before_start_time: Union[str, object] = values.unset,
        after_start_time: Union[str, object] = values.unset,
        before_date_created: Union[str, object] = values.unset,
        after_date_created: Union[str, object] = values.unset,
        status: Union[str, object] = values.unset,
        language_code: Union[str, object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[TranscriptInstance]:
        """
        Asynchronously lists TranscriptInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param str service_sid: The unique SID identifier of the Service.
        :param str before_start_time: Filter by before StartTime.
        :param str after_start_time: Filter by after StartTime.
        :param str before_date_created: Filter by before DateCreated.
        :param str after_date_created: Filter by after DateCreated.
        :param str status: Filter by status.
        :param str language_code: Filter by Language Code.
        :param str source_sid: Filter by SourceSid.
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
                service_sid=service_sid,
                before_start_time=before_start_time,
                after_start_time=after_start_time,
                before_date_created=before_date_created,
                after_date_created=after_date_created,
                status=status,
                language_code=language_code,
                source_sid=source_sid,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        service_sid: Union[str, object] = values.unset,
        before_start_time: Union[str, object] = values.unset,
        after_start_time: Union[str, object] = values.unset,
        before_date_created: Union[str, object] = values.unset,
        after_date_created: Union[str, object] = values.unset,
        status: Union[str, object] = values.unset,
        language_code: Union[str, object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> TranscriptPage:
        """
        Retrieve a single page of TranscriptInstance records from the API.
        Request is executed immediately

        :param service_sid: The unique SID identifier of the Service.
        :param before_start_time: Filter by before StartTime.
        :param after_start_time: Filter by after StartTime.
        :param before_date_created: Filter by before DateCreated.
        :param after_date_created: Filter by after DateCreated.
        :param status: Filter by status.
        :param language_code: Filter by Language Code.
        :param source_sid: Filter by SourceSid.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of TranscriptInstance
        """
        data = values.of(
            {
                "ServiceSid": service_sid,
                "BeforeStartTime": before_start_time,
                "AfterStartTime": after_start_time,
                "BeforeDateCreated": before_date_created,
                "AfterDateCreated": after_date_created,
                "Status": status,
                "LanguageCode": language_code,
                "SourceSid": source_sid,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return TranscriptPage(self._version, response)

    async def page_async(
        self,
        service_sid: Union[str, object] = values.unset,
        before_start_time: Union[str, object] = values.unset,
        after_start_time: Union[str, object] = values.unset,
        before_date_created: Union[str, object] = values.unset,
        after_date_created: Union[str, object] = values.unset,
        status: Union[str, object] = values.unset,
        language_code: Union[str, object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> TranscriptPage:
        """
        Asynchronously retrieve a single page of TranscriptInstance records from the API.
        Request is executed immediately

        :param service_sid: The unique SID identifier of the Service.
        :param before_start_time: Filter by before StartTime.
        :param after_start_time: Filter by after StartTime.
        :param before_date_created: Filter by before DateCreated.
        :param after_date_created: Filter by after DateCreated.
        :param status: Filter by status.
        :param language_code: Filter by Language Code.
        :param source_sid: Filter by SourceSid.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of TranscriptInstance
        """
        data = values.of(
            {
                "ServiceSid": service_sid,
                "BeforeStartTime": before_start_time,
                "AfterStartTime": after_start_time,
                "BeforeDateCreated": before_date_created,
                "AfterDateCreated": after_date_created,
                "Status": status,
                "LanguageCode": language_code,
                "SourceSid": source_sid,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return TranscriptPage(self._version, response)

    def get_page(self, target_url: str) -> TranscriptPage:
        """
        Retrieve a specific page of TranscriptInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of TranscriptInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return TranscriptPage(self._version, response)

    async def get_page_async(self, target_url: str) -> TranscriptPage:
        """
        Asynchronously retrieve a specific page of TranscriptInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of TranscriptInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return TranscriptPage(self._version, response)

    def get(self, sid: str) -> TranscriptContext:
        """
        Constructs a TranscriptContext

        :param sid: A 34 character string that uniquely identifies this Transcript.
        """
        return TranscriptContext(self._version, sid=sid)

    def __call__(self, sid: str) -> TranscriptContext:
        """
        Constructs a TranscriptContext

        :param sid: A 34 character string that uniquely identifies this Transcript.
        """
        return TranscriptContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Intelligence.V2.TranscriptList>"
