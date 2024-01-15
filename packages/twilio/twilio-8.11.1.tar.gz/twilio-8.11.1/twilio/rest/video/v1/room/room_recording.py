r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Video
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


class RoomRecordingInstance(InstanceResource):
    class Codec(object):
        VP8 = "VP8"
        H264 = "H264"
        OPUS = "OPUS"
        PCMU = "PCMU"

    class Format(object):
        MKA = "mka"
        MKV = "mkv"

    class Status(object):
        PROCESSING = "processing"
        COMPLETED = "completed"
        DELETED = "deleted"
        FAILED = "failed"

    class Type(object):
        AUDIO = "audio"
        VIDEO = "video"
        DATA = "data"

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the RoomRecording resource.
    :ivar status: 
    :ivar date_created: The date and time in GMT when the resource was created specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar sid: The unique string that we created to identify the RoomRecording resource.
    :ivar source_sid: The SID of the recording source. For a Room Recording, this value is a `track_sid`.
    :ivar size: The size of the recorded track in bytes.
    :ivar url: The absolute URL of the resource.
    :ivar type: 
    :ivar duration: The duration of the recording rounded to the nearest second. Sub-second duration tracks have a `duration` of 1 second
    :ivar container_format: 
    :ivar codec: 
    :ivar grouping_sids: A list of SIDs related to the Recording. Includes the `room_sid` and `participant_sid`.
    :ivar track_name: The name that was given to the source track of the recording. If no name is given, the `source_sid` is used.
    :ivar offset: The time in milliseconds elapsed between an arbitrary point in time, common to all group rooms, and the moment when the source room of this track started. This information provides a synchronization mechanism for recordings belonging to the same room.
    :ivar media_external_location: The URL of the media file associated with the recording when stored externally. See [External S3 Recordings](/docs/video/api/external-s3-recordings) for more details.
    :ivar room_sid: The SID of the Room resource the recording is associated with.
    :ivar links: The URLs of related resources.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        room_sid: str,
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.status: Optional["RoomRecordingInstance.Status"] = payload.get("status")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.sid: Optional[str] = payload.get("sid")
        self.source_sid: Optional[str] = payload.get("source_sid")
        self.size: Optional[int] = payload.get("size")
        self.url: Optional[str] = payload.get("url")
        self.type: Optional["RoomRecordingInstance.Type"] = payload.get("type")
        self.duration: Optional[int] = deserialize.integer(payload.get("duration"))
        self.container_format: Optional["RoomRecordingInstance.Format"] = payload.get(
            "container_format"
        )
        self.codec: Optional["RoomRecordingInstance.Codec"] = payload.get("codec")
        self.grouping_sids: Optional[Dict[str, object]] = payload.get("grouping_sids")
        self.track_name: Optional[str] = payload.get("track_name")
        self.offset: Optional[int] = payload.get("offset")
        self.media_external_location: Optional[str] = payload.get(
            "media_external_location"
        )
        self.room_sid: Optional[str] = payload.get("room_sid")
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "room_sid": room_sid,
            "sid": sid or self.sid,
        }
        self._context: Optional[RoomRecordingContext] = None

    @property
    def _proxy(self) -> "RoomRecordingContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: RoomRecordingContext for this RoomRecordingInstance
        """
        if self._context is None:
            self._context = RoomRecordingContext(
                self._version,
                room_sid=self._solution["room_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the RoomRecordingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the RoomRecordingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "RoomRecordingInstance":
        """
        Fetch the RoomRecordingInstance


        :returns: The fetched RoomRecordingInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "RoomRecordingInstance":
        """
        Asynchronous coroutine to fetch the RoomRecordingInstance


        :returns: The fetched RoomRecordingInstance
        """
        return await self._proxy.fetch_async()

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Video.V1.RoomRecordingInstance {}>".format(context)


class RoomRecordingContext(InstanceContext):
    def __init__(self, version: Version, room_sid: str, sid: str):
        """
        Initialize the RoomRecordingContext

        :param version: Version that contains the resource
        :param room_sid: The SID of the Room resource with the recording to fetch.
        :param sid: The SID of the RoomRecording resource to fetch.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "room_sid": room_sid,
            "sid": sid,
        }
        self._uri = "/Rooms/{room_sid}/Recordings/{sid}".format(**self._solution)

    def delete(self) -> bool:
        """
        Deletes the RoomRecordingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the RoomRecordingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> RoomRecordingInstance:
        """
        Fetch the RoomRecordingInstance


        :returns: The fetched RoomRecordingInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return RoomRecordingInstance(
            self._version,
            payload,
            room_sid=self._solution["room_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> RoomRecordingInstance:
        """
        Asynchronous coroutine to fetch the RoomRecordingInstance


        :returns: The fetched RoomRecordingInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return RoomRecordingInstance(
            self._version,
            payload,
            room_sid=self._solution["room_sid"],
            sid=self._solution["sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Video.V1.RoomRecordingContext {}>".format(context)


class RoomRecordingPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> RoomRecordingInstance:
        """
        Build an instance of RoomRecordingInstance

        :param payload: Payload response from the API
        """
        return RoomRecordingInstance(
            self._version, payload, room_sid=self._solution["room_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Video.V1.RoomRecordingPage>"


class RoomRecordingList(ListResource):
    def __init__(self, version: Version, room_sid: str):
        """
        Initialize the RoomRecordingList

        :param version: Version that contains the resource
        :param room_sid: The SID of the room with the RoomRecording resources to read.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "room_sid": room_sid,
        }
        self._uri = "/Rooms/{room_sid}/Recordings".format(**self._solution)

    def stream(
        self,
        status: Union["RoomRecordingInstance.Status", object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        date_created_after: Union[datetime, object] = values.unset,
        date_created_before: Union[datetime, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[RoomRecordingInstance]:
        """
        Streams RoomRecordingInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param &quot;RoomRecordingInstance.Status&quot; status: Read only the recordings with this status. Can be: `processing`, `completed`, or `deleted`.
        :param str source_sid: Read only the recordings that have this `source_sid`.
        :param datetime date_created_after: Read only recordings that started on or after this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param datetime date_created_before: Read only Recordings that started before this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
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
            status=status,
            source_sid=source_sid,
            date_created_after=date_created_after,
            date_created_before=date_created_before,
            page_size=limits["page_size"],
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        status: Union["RoomRecordingInstance.Status", object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        date_created_after: Union[datetime, object] = values.unset,
        date_created_before: Union[datetime, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[RoomRecordingInstance]:
        """
        Asynchronously streams RoomRecordingInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param &quot;RoomRecordingInstance.Status&quot; status: Read only the recordings with this status. Can be: `processing`, `completed`, or `deleted`.
        :param str source_sid: Read only the recordings that have this `source_sid`.
        :param datetime date_created_after: Read only recordings that started on or after this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param datetime date_created_before: Read only Recordings that started before this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
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
            status=status,
            source_sid=source_sid,
            date_created_after=date_created_after,
            date_created_before=date_created_before,
            page_size=limits["page_size"],
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        status: Union["RoomRecordingInstance.Status", object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        date_created_after: Union[datetime, object] = values.unset,
        date_created_before: Union[datetime, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[RoomRecordingInstance]:
        """
        Lists RoomRecordingInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param &quot;RoomRecordingInstance.Status&quot; status: Read only the recordings with this status. Can be: `processing`, `completed`, or `deleted`.
        :param str source_sid: Read only the recordings that have this `source_sid`.
        :param datetime date_created_after: Read only recordings that started on or after this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param datetime date_created_before: Read only Recordings that started before this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
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
                status=status,
                source_sid=source_sid,
                date_created_after=date_created_after,
                date_created_before=date_created_before,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        status: Union["RoomRecordingInstance.Status", object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        date_created_after: Union[datetime, object] = values.unset,
        date_created_before: Union[datetime, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[RoomRecordingInstance]:
        """
        Asynchronously lists RoomRecordingInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param &quot;RoomRecordingInstance.Status&quot; status: Read only the recordings with this status. Can be: `processing`, `completed`, or `deleted`.
        :param str source_sid: Read only the recordings that have this `source_sid`.
        :param datetime date_created_after: Read only recordings that started on or after this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param datetime date_created_before: Read only Recordings that started before this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
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
                status=status,
                source_sid=source_sid,
                date_created_after=date_created_after,
                date_created_before=date_created_before,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        status: Union["RoomRecordingInstance.Status", object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        date_created_after: Union[datetime, object] = values.unset,
        date_created_before: Union[datetime, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> RoomRecordingPage:
        """
        Retrieve a single page of RoomRecordingInstance records from the API.
        Request is executed immediately

        :param status: Read only the recordings with this status. Can be: `processing`, `completed`, or `deleted`.
        :param source_sid: Read only the recordings that have this `source_sid`.
        :param date_created_after: Read only recordings that started on or after this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param date_created_before: Read only Recordings that started before this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of RoomRecordingInstance
        """
        data = values.of(
            {
                "Status": status,
                "SourceSid": source_sid,
                "DateCreatedAfter": serialize.iso8601_datetime(date_created_after),
                "DateCreatedBefore": serialize.iso8601_datetime(date_created_before),
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return RoomRecordingPage(self._version, response, self._solution)

    async def page_async(
        self,
        status: Union["RoomRecordingInstance.Status", object] = values.unset,
        source_sid: Union[str, object] = values.unset,
        date_created_after: Union[datetime, object] = values.unset,
        date_created_before: Union[datetime, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> RoomRecordingPage:
        """
        Asynchronously retrieve a single page of RoomRecordingInstance records from the API.
        Request is executed immediately

        :param status: Read only the recordings with this status. Can be: `processing`, `completed`, or `deleted`.
        :param source_sid: Read only the recordings that have this `source_sid`.
        :param date_created_after: Read only recordings that started on or after this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param date_created_before: Read only Recordings that started before this [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) datetime with time zone.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of RoomRecordingInstance
        """
        data = values.of(
            {
                "Status": status,
                "SourceSid": source_sid,
                "DateCreatedAfter": serialize.iso8601_datetime(date_created_after),
                "DateCreatedBefore": serialize.iso8601_datetime(date_created_before),
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return RoomRecordingPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> RoomRecordingPage:
        """
        Retrieve a specific page of RoomRecordingInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of RoomRecordingInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return RoomRecordingPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> RoomRecordingPage:
        """
        Asynchronously retrieve a specific page of RoomRecordingInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of RoomRecordingInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return RoomRecordingPage(self._version, response, self._solution)

    def get(self, sid: str) -> RoomRecordingContext:
        """
        Constructs a RoomRecordingContext

        :param sid: The SID of the RoomRecording resource to fetch.
        """
        return RoomRecordingContext(
            self._version, room_sid=self._solution["room_sid"], sid=sid
        )

    def __call__(self, sid: str) -> RoomRecordingContext:
        """
        Constructs a RoomRecordingContext

        :param sid: The SID of the RoomRecording resource to fetch.
        """
        return RoomRecordingContext(
            self._version, room_sid=self._solution["room_sid"], sid=sid
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Video.V1.RoomRecordingList>"
