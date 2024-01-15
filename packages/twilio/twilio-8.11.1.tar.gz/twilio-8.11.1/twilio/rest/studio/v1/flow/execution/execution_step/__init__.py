r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Studio
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
from twilio.rest.studio.v1.flow.execution.execution_step.execution_step_context import (
    ExecutionStepContextList,
)


class ExecutionStepInstance(InstanceResource):

    """
    :ivar sid: The unique string that we created to identify the ExecutionStep resource.
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the ExecutionStep resource.
    :ivar flow_sid: The SID of the Flow.
    :ivar execution_sid: The SID of the Step's Execution resource.
    :ivar name: The event that caused the Flow to transition to the Step.
    :ivar context: The current state of the Flow's Execution. As a flow executes, we save its state in this context. We save data that your widgets can access as variables in configuration fields or in text areas as variable substitution.
    :ivar transitioned_from: The Widget that preceded the Widget for the Step.
    :ivar transitioned_to: The Widget that will follow the Widget for the Step.
    :ivar date_created: The date and time in GMT when the resource was created specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar date_updated: The date and time in GMT when the resource was last updated specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar url: The absolute URL of the resource.
    :ivar links: The URLs of related resources.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        flow_sid: str,
        execution_sid: str,
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.flow_sid: Optional[str] = payload.get("flow_sid")
        self.execution_sid: Optional[str] = payload.get("execution_sid")
        self.name: Optional[str] = payload.get("name")
        self.context: Optional[Dict[str, object]] = payload.get("context")
        self.transitioned_from: Optional[str] = payload.get("transitioned_from")
        self.transitioned_to: Optional[str] = payload.get("transitioned_to")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.url: Optional[str] = payload.get("url")
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "flow_sid": flow_sid,
            "execution_sid": execution_sid,
            "sid": sid or self.sid,
        }
        self._context: Optional[ExecutionStepContext] = None

    @property
    def _proxy(self) -> "ExecutionStepContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: ExecutionStepContext for this ExecutionStepInstance
        """
        if self._context is None:
            self._context = ExecutionStepContext(
                self._version,
                flow_sid=self._solution["flow_sid"],
                execution_sid=self._solution["execution_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def fetch(self) -> "ExecutionStepInstance":
        """
        Fetch the ExecutionStepInstance


        :returns: The fetched ExecutionStepInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "ExecutionStepInstance":
        """
        Asynchronous coroutine to fetch the ExecutionStepInstance


        :returns: The fetched ExecutionStepInstance
        """
        return await self._proxy.fetch_async()

    @property
    def step_context(self) -> ExecutionStepContextList:
        """
        Access the step_context
        """
        return self._proxy.step_context

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Studio.V1.ExecutionStepInstance {}>".format(context)


class ExecutionStepContext(InstanceContext):
    def __init__(self, version: Version, flow_sid: str, execution_sid: str, sid: str):
        """
        Initialize the ExecutionStepContext

        :param version: Version that contains the resource
        :param flow_sid: The SID of the Flow with the Step to fetch.
        :param execution_sid: The SID of the Execution resource with the Step to fetch.
        :param sid: The SID of the ExecutionStep resource to fetch.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "flow_sid": flow_sid,
            "execution_sid": execution_sid,
            "sid": sid,
        }
        self._uri = "/Flows/{flow_sid}/Executions/{execution_sid}/Steps/{sid}".format(
            **self._solution
        )

        self._step_context: Optional[ExecutionStepContextList] = None

    def fetch(self) -> ExecutionStepInstance:
        """
        Fetch the ExecutionStepInstance


        :returns: The fetched ExecutionStepInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return ExecutionStepInstance(
            self._version,
            payload,
            flow_sid=self._solution["flow_sid"],
            execution_sid=self._solution["execution_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> ExecutionStepInstance:
        """
        Asynchronous coroutine to fetch the ExecutionStepInstance


        :returns: The fetched ExecutionStepInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return ExecutionStepInstance(
            self._version,
            payload,
            flow_sid=self._solution["flow_sid"],
            execution_sid=self._solution["execution_sid"],
            sid=self._solution["sid"],
        )

    @property
    def step_context(self) -> ExecutionStepContextList:
        """
        Access the step_context
        """
        if self._step_context is None:
            self._step_context = ExecutionStepContextList(
                self._version,
                self._solution["flow_sid"],
                self._solution["execution_sid"],
                self._solution["sid"],
            )
        return self._step_context

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Studio.V1.ExecutionStepContext {}>".format(context)


class ExecutionStepPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> ExecutionStepInstance:
        """
        Build an instance of ExecutionStepInstance

        :param payload: Payload response from the API
        """
        return ExecutionStepInstance(
            self._version,
            payload,
            flow_sid=self._solution["flow_sid"],
            execution_sid=self._solution["execution_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Studio.V1.ExecutionStepPage>"


class ExecutionStepList(ListResource):
    def __init__(self, version: Version, flow_sid: str, execution_sid: str):
        """
        Initialize the ExecutionStepList

        :param version: Version that contains the resource
        :param flow_sid: The SID of the Flow with the Steps to read.
        :param execution_sid: The SID of the Execution with the Steps to read.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "flow_sid": flow_sid,
            "execution_sid": execution_sid,
        }
        self._uri = "/Flows/{flow_sid}/Executions/{execution_sid}/Steps".format(
            **self._solution
        )

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[ExecutionStepInstance]:
        """
        Streams ExecutionStepInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[ExecutionStepInstance]:
        """
        Asynchronously streams ExecutionStepInstance records from the API as a generator stream.
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
    ) -> List[ExecutionStepInstance]:
        """
        Lists ExecutionStepInstance records from the API as a list.
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
    ) -> List[ExecutionStepInstance]:
        """
        Asynchronously lists ExecutionStepInstance records from the API as a list.
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
    ) -> ExecutionStepPage:
        """
        Retrieve a single page of ExecutionStepInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of ExecutionStepInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return ExecutionStepPage(self._version, response, self._solution)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> ExecutionStepPage:
        """
        Asynchronously retrieve a single page of ExecutionStepInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of ExecutionStepInstance
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
        return ExecutionStepPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> ExecutionStepPage:
        """
        Retrieve a specific page of ExecutionStepInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of ExecutionStepInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return ExecutionStepPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> ExecutionStepPage:
        """
        Asynchronously retrieve a specific page of ExecutionStepInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of ExecutionStepInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return ExecutionStepPage(self._version, response, self._solution)

    def get(self, sid: str) -> ExecutionStepContext:
        """
        Constructs a ExecutionStepContext

        :param sid: The SID of the ExecutionStep resource to fetch.
        """
        return ExecutionStepContext(
            self._version,
            flow_sid=self._solution["flow_sid"],
            execution_sid=self._solution["execution_sid"],
            sid=sid,
        )

    def __call__(self, sid: str) -> ExecutionStepContext:
        """
        Constructs a ExecutionStepContext

        :param sid: The SID of the ExecutionStep resource to fetch.
        """
        return ExecutionStepContext(
            self._version,
            flow_sid=self._solution["flow_sid"],
            execution_sid=self._solution["execution_sid"],
            sid=sid,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Studio.V1.ExecutionStepList>"
