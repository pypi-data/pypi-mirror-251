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
from twilio.base import deserialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class SubscribedTrackInstance(InstanceResource):
    class Kind(object):
        AUDIO = "audio"
        VIDEO = "video"
        DATA = "data"

    """
    :ivar sid: The unique string that we created to identify the RoomParticipantSubscribedTrack resource.
    :ivar participant_sid: The SID of the participant that subscribes to the track.
    :ivar publisher_sid: The SID of the participant that publishes the track.
    :ivar room_sid: The SID of the room where the track is published.
    :ivar name: The track name. Must have no more than 128 characters and be unique among the participant's published tracks.
    :ivar date_created: The date and time in GMT when the resource was created specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar date_updated: The date and time in GMT when the resource was last updated specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar enabled: Whether the track is enabled.
    :ivar kind: 
    :ivar url: The absolute URL of the resource.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        room_sid: str,
        participant_sid: str,
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.participant_sid: Optional[str] = payload.get("participant_sid")
        self.publisher_sid: Optional[str] = payload.get("publisher_sid")
        self.room_sid: Optional[str] = payload.get("room_sid")
        self.name: Optional[str] = payload.get("name")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.enabled: Optional[bool] = payload.get("enabled")
        self.kind: Optional["SubscribedTrackInstance.Kind"] = payload.get("kind")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "room_sid": room_sid,
            "participant_sid": participant_sid,
            "sid": sid or self.sid,
        }
        self._context: Optional[SubscribedTrackContext] = None

    @property
    def _proxy(self) -> "SubscribedTrackContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: SubscribedTrackContext for this SubscribedTrackInstance
        """
        if self._context is None:
            self._context = SubscribedTrackContext(
                self._version,
                room_sid=self._solution["room_sid"],
                participant_sid=self._solution["participant_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def fetch(self) -> "SubscribedTrackInstance":
        """
        Fetch the SubscribedTrackInstance


        :returns: The fetched SubscribedTrackInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "SubscribedTrackInstance":
        """
        Asynchronous coroutine to fetch the SubscribedTrackInstance


        :returns: The fetched SubscribedTrackInstance
        """
        return await self._proxy.fetch_async()

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Video.V1.SubscribedTrackInstance {}>".format(context)


class SubscribedTrackContext(InstanceContext):
    def __init__(self, version: Version, room_sid: str, participant_sid: str, sid: str):
        """
        Initialize the SubscribedTrackContext

        :param version: Version that contains the resource
        :param room_sid: The SID of the Room where the Track resource to fetch is subscribed.
        :param participant_sid: The SID of the participant that subscribes to the Track resource to fetch.
        :param sid: The SID of the RoomParticipantSubscribedTrack resource to fetch.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "room_sid": room_sid,
            "participant_sid": participant_sid,
            "sid": sid,
        }
        self._uri = "/Rooms/{room_sid}/Participants/{participant_sid}/SubscribedTracks/{sid}".format(
            **self._solution
        )

    def fetch(self) -> SubscribedTrackInstance:
        """
        Fetch the SubscribedTrackInstance


        :returns: The fetched SubscribedTrackInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return SubscribedTrackInstance(
            self._version,
            payload,
            room_sid=self._solution["room_sid"],
            participant_sid=self._solution["participant_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> SubscribedTrackInstance:
        """
        Asynchronous coroutine to fetch the SubscribedTrackInstance


        :returns: The fetched SubscribedTrackInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return SubscribedTrackInstance(
            self._version,
            payload,
            room_sid=self._solution["room_sid"],
            participant_sid=self._solution["participant_sid"],
            sid=self._solution["sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Video.V1.SubscribedTrackContext {}>".format(context)


class SubscribedTrackPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> SubscribedTrackInstance:
        """
        Build an instance of SubscribedTrackInstance

        :param payload: Payload response from the API
        """
        return SubscribedTrackInstance(
            self._version,
            payload,
            room_sid=self._solution["room_sid"],
            participant_sid=self._solution["participant_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Video.V1.SubscribedTrackPage>"


class SubscribedTrackList(ListResource):
    def __init__(self, version: Version, room_sid: str, participant_sid: str):
        """
        Initialize the SubscribedTrackList

        :param version: Version that contains the resource
        :param room_sid: The SID of the Room resource with the Track resources to read.
        :param participant_sid: The SID of the participant that subscribes to the Track resources to read.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "room_sid": room_sid,
            "participant_sid": participant_sid,
        }
        self._uri = (
            "/Rooms/{room_sid}/Participants/{participant_sid}/SubscribedTracks".format(
                **self._solution
            )
        )

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[SubscribedTrackInstance]:
        """
        Streams SubscribedTrackInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[SubscribedTrackInstance]:
        """
        Asynchronously streams SubscribedTrackInstance records from the API as a generator stream.
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
    ) -> List[SubscribedTrackInstance]:
        """
        Lists SubscribedTrackInstance records from the API as a list.
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
    ) -> List[SubscribedTrackInstance]:
        """
        Asynchronously lists SubscribedTrackInstance records from the API as a list.
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
    ) -> SubscribedTrackPage:
        """
        Retrieve a single page of SubscribedTrackInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SubscribedTrackInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return SubscribedTrackPage(self._version, response, self._solution)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> SubscribedTrackPage:
        """
        Asynchronously retrieve a single page of SubscribedTrackInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of SubscribedTrackInstance
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
        return SubscribedTrackPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> SubscribedTrackPage:
        """
        Retrieve a specific page of SubscribedTrackInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SubscribedTrackInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return SubscribedTrackPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> SubscribedTrackPage:
        """
        Asynchronously retrieve a specific page of SubscribedTrackInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of SubscribedTrackInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return SubscribedTrackPage(self._version, response, self._solution)

    def get(self, sid: str) -> SubscribedTrackContext:
        """
        Constructs a SubscribedTrackContext

        :param sid: The SID of the RoomParticipantSubscribedTrack resource to fetch.
        """
        return SubscribedTrackContext(
            self._version,
            room_sid=self._solution["room_sid"],
            participant_sid=self._solution["participant_sid"],
            sid=sid,
        )

    def __call__(self, sid: str) -> SubscribedTrackContext:
        """
        Constructs a SubscribedTrackContext

        :param sid: The SID of the RoomParticipantSubscribedTrack resource to fetch.
        """
        return SubscribedTrackContext(
            self._version,
            room_sid=self._solution["room_sid"],
            participant_sid=self._solution["participant_sid"],
            sid=sid,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Video.V1.SubscribedTrackList>"
