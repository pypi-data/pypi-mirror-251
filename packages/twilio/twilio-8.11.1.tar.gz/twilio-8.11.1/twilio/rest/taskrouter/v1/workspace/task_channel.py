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


class TaskChannelInstance(InstanceResource):

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the Task Channel resource.
    :ivar date_created: The date and time in GMT when the resource was created specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar date_updated: The date and time in GMT when the resource was last updated specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar friendly_name: The string that you assigned to describe the resource.
    :ivar sid: The unique string that we created to identify the Task Channel resource.
    :ivar unique_name: An application-defined string that uniquely identifies the Task Channel, such as `voice` or `sms`.
    :ivar workspace_sid: The SID of the Workspace that contains the Task Channel.
    :ivar channel_optimized_routing: Whether the Task Channel will prioritize Workers that have been idle. When `true`, Workers that have been idle the longest are prioritized.
    :ivar url: The absolute URL of the Task Channel resource.
    :ivar links: The URLs of related resources.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        workspace_sid: str,
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.sid: Optional[str] = payload.get("sid")
        self.unique_name: Optional[str] = payload.get("unique_name")
        self.workspace_sid: Optional[str] = payload.get("workspace_sid")
        self.channel_optimized_routing: Optional[bool] = payload.get(
            "channel_optimized_routing"
        )
        self.url: Optional[str] = payload.get("url")
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "workspace_sid": workspace_sid,
            "sid": sid or self.sid,
        }
        self._context: Optional[TaskChannelContext] = None

    @property
    def _proxy(self) -> "TaskChannelContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: TaskChannelContext for this TaskChannelInstance
        """
        if self._context is None:
            self._context = TaskChannelContext(
                self._version,
                workspace_sid=self._solution["workspace_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the TaskChannelInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the TaskChannelInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "TaskChannelInstance":
        """
        Fetch the TaskChannelInstance


        :returns: The fetched TaskChannelInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "TaskChannelInstance":
        """
        Asynchronous coroutine to fetch the TaskChannelInstance


        :returns: The fetched TaskChannelInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self,
        friendly_name: Union[str, object] = values.unset,
        channel_optimized_routing: Union[bool, object] = values.unset,
    ) -> "TaskChannelInstance":
        """
        Update the TaskChannelInstance

        :param friendly_name: A descriptive string that you create to describe the Task Channel. It can be up to 64 characters long.
        :param channel_optimized_routing: Whether the TaskChannel should prioritize Workers that have been idle. If `true`, Workers that have been idle the longest are prioritized.

        :returns: The updated TaskChannelInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            channel_optimized_routing=channel_optimized_routing,
        )

    async def update_async(
        self,
        friendly_name: Union[str, object] = values.unset,
        channel_optimized_routing: Union[bool, object] = values.unset,
    ) -> "TaskChannelInstance":
        """
        Asynchronous coroutine to update the TaskChannelInstance

        :param friendly_name: A descriptive string that you create to describe the Task Channel. It can be up to 64 characters long.
        :param channel_optimized_routing: Whether the TaskChannel should prioritize Workers that have been idle. If `true`, Workers that have been idle the longest are prioritized.

        :returns: The updated TaskChannelInstance
        """
        return await self._proxy.update_async(
            friendly_name=friendly_name,
            channel_optimized_routing=channel_optimized_routing,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Taskrouter.V1.TaskChannelInstance {}>".format(context)


class TaskChannelContext(InstanceContext):
    def __init__(self, version: Version, workspace_sid: str, sid: str):
        """
        Initialize the TaskChannelContext

        :param version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the Task Channel to update.
        :param sid: The SID of the Task Channel resource to update.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "workspace_sid": workspace_sid,
            "sid": sid,
        }
        self._uri = "/Workspaces/{workspace_sid}/TaskChannels/{sid}".format(
            **self._solution
        )

    def delete(self) -> bool:
        """
        Deletes the TaskChannelInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the TaskChannelInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> TaskChannelInstance:
        """
        Fetch the TaskChannelInstance


        :returns: The fetched TaskChannelInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return TaskChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> TaskChannelInstance:
        """
        Asynchronous coroutine to fetch the TaskChannelInstance


        :returns: The fetched TaskChannelInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return TaskChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            sid=self._solution["sid"],
        )

    def update(
        self,
        friendly_name: Union[str, object] = values.unset,
        channel_optimized_routing: Union[bool, object] = values.unset,
    ) -> TaskChannelInstance:
        """
        Update the TaskChannelInstance

        :param friendly_name: A descriptive string that you create to describe the Task Channel. It can be up to 64 characters long.
        :param channel_optimized_routing: Whether the TaskChannel should prioritize Workers that have been idle. If `true`, Workers that have been idle the longest are prioritized.

        :returns: The updated TaskChannelInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
                "ChannelOptimizedRouting": channel_optimized_routing,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TaskChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            sid=self._solution["sid"],
        )

    async def update_async(
        self,
        friendly_name: Union[str, object] = values.unset,
        channel_optimized_routing: Union[bool, object] = values.unset,
    ) -> TaskChannelInstance:
        """
        Asynchronous coroutine to update the TaskChannelInstance

        :param friendly_name: A descriptive string that you create to describe the Task Channel. It can be up to 64 characters long.
        :param channel_optimized_routing: Whether the TaskChannel should prioritize Workers that have been idle. If `true`, Workers that have been idle the longest are prioritized.

        :returns: The updated TaskChannelInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
                "ChannelOptimizedRouting": channel_optimized_routing,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TaskChannelInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
            sid=self._solution["sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Taskrouter.V1.TaskChannelContext {}>".format(context)


class TaskChannelPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> TaskChannelInstance:
        """
        Build an instance of TaskChannelInstance

        :param payload: Payload response from the API
        """
        return TaskChannelInstance(
            self._version, payload, workspace_sid=self._solution["workspace_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Taskrouter.V1.TaskChannelPage>"


class TaskChannelList(ListResource):
    def __init__(self, version: Version, workspace_sid: str):
        """
        Initialize the TaskChannelList

        :param version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the Task Channel to read.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "workspace_sid": workspace_sid,
        }
        self._uri = "/Workspaces/{workspace_sid}/TaskChannels".format(**self._solution)

    def create(
        self,
        friendly_name: str,
        unique_name: str,
        channel_optimized_routing: Union[bool, object] = values.unset,
    ) -> TaskChannelInstance:
        """
        Create the TaskChannelInstance

        :param friendly_name: A descriptive string that you create to describe the Task Channel. It can be up to 64 characters long.
        :param unique_name: An application-defined string that uniquely identifies the Task Channel, such as `voice` or `sms`.
        :param channel_optimized_routing: Whether the Task Channel should prioritize Workers that have been idle. If `true`, Workers that have been idle the longest are prioritized.

        :returns: The created TaskChannelInstance
        """

        data = values.of(
            {
                "FriendlyName": friendly_name,
                "UniqueName": unique_name,
                "ChannelOptimizedRouting": channel_optimized_routing,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TaskChannelInstance(
            self._version, payload, workspace_sid=self._solution["workspace_sid"]
        )

    async def create_async(
        self,
        friendly_name: str,
        unique_name: str,
        channel_optimized_routing: Union[bool, object] = values.unset,
    ) -> TaskChannelInstance:
        """
        Asynchronously create the TaskChannelInstance

        :param friendly_name: A descriptive string that you create to describe the Task Channel. It can be up to 64 characters long.
        :param unique_name: An application-defined string that uniquely identifies the Task Channel, such as `voice` or `sms`.
        :param channel_optimized_routing: Whether the Task Channel should prioritize Workers that have been idle. If `true`, Workers that have been idle the longest are prioritized.

        :returns: The created TaskChannelInstance
        """

        data = values.of(
            {
                "FriendlyName": friendly_name,
                "UniqueName": unique_name,
                "ChannelOptimizedRouting": channel_optimized_routing,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TaskChannelInstance(
            self._version, payload, workspace_sid=self._solution["workspace_sid"]
        )

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[TaskChannelInstance]:
        """
        Streams TaskChannelInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[TaskChannelInstance]:
        """
        Asynchronously streams TaskChannelInstance records from the API as a generator stream.
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
    ) -> List[TaskChannelInstance]:
        """
        Lists TaskChannelInstance records from the API as a list.
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
    ) -> List[TaskChannelInstance]:
        """
        Asynchronously lists TaskChannelInstance records from the API as a list.
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
    ) -> TaskChannelPage:
        """
        Retrieve a single page of TaskChannelInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of TaskChannelInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return TaskChannelPage(self._version, response, self._solution)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> TaskChannelPage:
        """
        Asynchronously retrieve a single page of TaskChannelInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of TaskChannelInstance
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
        return TaskChannelPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> TaskChannelPage:
        """
        Retrieve a specific page of TaskChannelInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of TaskChannelInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return TaskChannelPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> TaskChannelPage:
        """
        Asynchronously retrieve a specific page of TaskChannelInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of TaskChannelInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return TaskChannelPage(self._version, response, self._solution)

    def get(self, sid: str) -> TaskChannelContext:
        """
        Constructs a TaskChannelContext

        :param sid: The SID of the Task Channel resource to update.
        """
        return TaskChannelContext(
            self._version, workspace_sid=self._solution["workspace_sid"], sid=sid
        )

    def __call__(self, sid: str) -> TaskChannelContext:
        """
        Constructs a TaskChannelContext

        :param sid: The SID of the Task Channel resource to update.
        """
        return TaskChannelContext(
            self._version, workspace_sid=self._solution["workspace_sid"], sid=sid
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Taskrouter.V1.TaskChannelList>"
