r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Taskrouter
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


class WorkerChannelInstance(InstanceResource):

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the Worker resource.
    :ivar assigned_tasks: The total number of Tasks assigned to Worker for the TaskChannel type.
    :ivar available: Whether the Worker should receive Tasks of the TaskChannel type.
    :ivar available_capacity_percentage: The current percentage of capacity the TaskChannel has available. Can be a number between `0` and `100`. A value of `0` indicates that TaskChannel has no capacity available and a value of `100` means the  Worker is available to receive any Tasks of this TaskChannel type.
    :ivar configured_capacity: The current configured capacity for the WorkerChannel. TaskRouter will not create any reservations after the assigned Tasks for the Worker reaches the value.
    :ivar date_created: The date and time in GMT when the resource was created specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar date_updated: The date and time in GMT when the resource was last updated specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar sid: The unique string that we created to identify the WorkerChannel resource.
    :ivar task_channel_sid: The SID of the TaskChannel.
    :ivar task_channel_unique_name: The unique name of the TaskChannel, such as `voice` or `sms`.
    :ivar worker_sid: The SID of the Worker that contains the WorkerChannel.
    :ivar workspace_sid: The SID of the Workspace that contains the WorkerChannel.
    :ivar url: The absolute URL of the WorkerChannel resource.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        workspace_sid: str,
        worker_sid: str,
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.assigned_tasks: Optional[int] = deserialize.integer(
            payload.get("assigned_tasks")
        )
        self.available: Optional[bool] = payload.get("available")
        self.available_capacity_percentage: Optional[int] = deserialize.integer(
            payload.get("available_capacity_percentage")
        )
        self.configured_capacity: Optional[int] = deserialize.integer(
            payload.get("configured_capacity")
        )
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.sid: Optional[str] = payload.get("sid")
        self.task_channel_sid: Optional[str] = payload.get("task_channel_sid")
        self.task_channel_unique_name: Optional[str] = payload.get(
            "task_channel_unique_name"
        )
        self.worker_sid: Optional[str] = payload.get("worker_sid")
        self.workspace_sid: Optional[str] = payload.get("workspace_sid")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "workspace_sid": workspace_sid,
            "worker_sid": worker_sid,
            "sid": sid or self.sid,
        }
        self._context: Optional[WorkerChannelContext] = None

    @property
    def _proxy(self) -> "WorkerChannelContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: WorkerChannelContext for this WorkerChannelInstance
        """
        if self._context is None:
            self._context = WorkerChannelContext(
                self._version,
                workspace_sid=self._solution["workspace_sid"],
                worker_sid=self._solution["worker_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def fetch(self) -> "WorkerChannelInstance":
        """
        Fetch the WorkerChannelInstance


        :returns: The fetched WorkerChannelInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "WorkerChannelInstance":
        """
        Asynchronous coroutine to fetch the WorkerChannelInstance


        :returns: The fetched WorkerChannelInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self,
        capacity: Union[int, object] = values.unset,
        available: Union[bool, object] = values.unset,
    ) -> "WorkerChannelInstance":
        """
        Update the WorkerChannelInstance

        :param capacity: The total number of Tasks that the Worker should handle for the TaskChannel type. TaskRouter creates reservations for Tasks of this TaskChannel type up to the specified capacity. If the capacity is 0, no new reservations will be created.
        :param available: Whether the WorkerChannel is available. Set to `false` to prevent the Worker from receiving any new Tasks of this TaskChannel type.

        :returns: The updated WorkerChannelInstance
        """
        return self._proxy.update(
            capacity=capacity,
            available=available,
        )

    async def update_async(
        self,
        capacity: Union[int, object] = values.unset,
        available: Union[bool, object] = values.unset,
    ) -> "WorkerChannelInstance":
        """
        Asynchronous coroutine to update the WorkerChannelInstance

        :param capacity: The total number of Tasks that the Worker should handle for the TaskChannel type. TaskRouter creates reservations for Tasks of this TaskChannel type up to the specified capacity. If the capacity is 0, no new reservations will be created.
        :param available: Whether the WorkerChannel is available. Set to `false` to prevent the Worker from receiving any new Tasks of this TaskChannel type.

        :returns: The updated WorkerChannelInstance
        """
        return await self._proxy.update_async(
            capacity=capacity,
            available=available,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Taskrouter.V1.WorkerChannelInstance {}>".format(context)


class WorkerChannelContext(InstanceContext):
    def __init__(self, version: Version, workspace_sid: str, worker_sid: str, sid: str):
        """
        Initialize the WorkerChannelContext

        :param version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the WorkerChannel to update.
        :param worker_sid: The SID of the Worker with the WorkerChannel to update.
        :param sid: The SID of the WorkerChannel to update.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "workspace_sid": workspace_sid,
            "worker_sid": worker_sid,
            "sid": sid,
        }
        self._uri = (
            "/Workspaces/{workspace_sid}/Workers/{worker_sid}/Channels/{sid}".format(
                **self._solution
            )
        )

    def fetch(self) -> WorkerChannelInstance:
        """
        Fetch the WorkerChannelInstance


        :returns: The fetched WorkerChannelInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> WorkerChannelInstance:
        """
        Asynchronous coroutine to fetch the WorkerChannelInstance


        :returns: The fetched WorkerChannelInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
            sid=self._solution["sid"],
        )

    def update(
        self,
        capacity: Union[int, object] = values.unset,
        available: Union[bool, object] = values.unset,
    ) -> WorkerChannelInstance:
        """
        Update the WorkerChannelInstance

        :param capacity: The total number of Tasks that the Worker should handle for the TaskChannel type. TaskRouter creates reservations for Tasks of this TaskChannel type up to the specified capacity. If the capacity is 0, no new reservations will be created.
        :param available: Whether the WorkerChannel is available. Set to `false` to prevent the Worker from receiving any new Tasks of this TaskChannel type.

        :returns: The updated WorkerChannelInstance
        """
        data = values.of(
            {
                "Capacity": capacity,
                "Available": available,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
            sid=self._solution["sid"],
        )

    async def update_async(
        self,
        capacity: Union[int, object] = values.unset,
        available: Union[bool, object] = values.unset,
    ) -> WorkerChannelInstance:
        """
        Asynchronous coroutine to update the WorkerChannelInstance

        :param capacity: The total number of Tasks that the Worker should handle for the TaskChannel type. TaskRouter creates reservations for Tasks of this TaskChannel type up to the specified capacity. If the capacity is 0, no new reservations will be created.
        :param available: Whether the WorkerChannel is available. Set to `false` to prevent the Worker from receiving any new Tasks of this TaskChannel type.

        :returns: The updated WorkerChannelInstance
        """
        data = values.of(
            {
                "Capacity": capacity,
                "Available": available,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
            sid=self._solution["sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Taskrouter.V1.WorkerChannelContext {}>".format(context)


class WorkerChannelPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> WorkerChannelInstance:
        """
        Build an instance of WorkerChannelInstance

        :param payload: Payload response from the API
        """
        return WorkerChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Taskrouter.V1.WorkerChannelPage>"


class WorkerChannelList(ListResource):
    def __init__(self, version: Version, workspace_sid: str, worker_sid: str):
        """
        Initialize the WorkerChannelList

        :param version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the WorkerChannels to read.
        :param worker_sid: The SID of the Worker with the WorkerChannels to read.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "workspace_sid": workspace_sid,
            "worker_sid": worker_sid,
        }
        self._uri = "/Workspaces/{workspace_sid}/Workers/{worker_sid}/Channels".format(
            **self._solution
        )

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[WorkerChannelInstance]:
        """
        Streams WorkerChannelInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[WorkerChannelInstance]:
        """
        Asynchronously streams WorkerChannelInstance records from the API as a generator stream.
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
    ) -> List[WorkerChannelInstance]:
        """
        Lists WorkerChannelInstance records from the API as a list.
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
    ) -> List[WorkerChannelInstance]:
        """
        Asynchronously lists WorkerChannelInstance records from the API as a list.
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
    ) -> WorkerChannelPage:
        """
        Retrieve a single page of WorkerChannelInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of WorkerChannelInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return WorkerChannelPage(self._version, response, self._solution)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> WorkerChannelPage:
        """
        Asynchronously retrieve a single page of WorkerChannelInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of WorkerChannelInstance
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
        return WorkerChannelPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> WorkerChannelPage:
        """
        Retrieve a specific page of WorkerChannelInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of WorkerChannelInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return WorkerChannelPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> WorkerChannelPage:
        """
        Asynchronously retrieve a specific page of WorkerChannelInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of WorkerChannelInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return WorkerChannelPage(self._version, response, self._solution)

    def get(self, sid: str) -> WorkerChannelContext:
        """
        Constructs a WorkerChannelContext

        :param sid: The SID of the WorkerChannel to update.
        """
        return WorkerChannelContext(
            self._version,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
            sid=sid,
        )

    def __call__(self, sid: str) -> WorkerChannelContext:
        """
        Constructs a WorkerChannelContext

        :param sid: The SID of the WorkerChannel to update.
        """
        return WorkerChannelContext(
            self._version,
            workspace_sid=self._solution["workspace_sid"],
            worker_sid=self._solution["worker_sid"],
            sid=sid,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Taskrouter.V1.WorkerChannelList>"
