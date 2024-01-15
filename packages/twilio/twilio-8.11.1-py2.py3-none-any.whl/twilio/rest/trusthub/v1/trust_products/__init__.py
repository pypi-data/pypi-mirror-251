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


from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import deserialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page
from twilio.rest.trusthub.v1.trust_products.trust_products_channel_endpoint_assignment import (
    TrustProductsChannelEndpointAssignmentList,
)
from twilio.rest.trusthub.v1.trust_products.trust_products_entity_assignments import (
    TrustProductsEntityAssignmentsList,
)
from twilio.rest.trusthub.v1.trust_products.trust_products_evaluations import (
    TrustProductsEvaluationsList,
)


class TrustProductsInstance(InstanceResource):
    class Status(object):
        DRAFT = "draft"
        PENDING_REVIEW = "pending-review"
        IN_REVIEW = "in-review"
        TWILIO_REJECTED = "twilio-rejected"
        TWILIO_APPROVED = "twilio-approved"

    """
    :ivar sid: The unique string that we created to identify the Customer-Profile resource.
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the Customer-Profile resource.
    :ivar policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
    :ivar friendly_name: The string that you assigned to describe the resource.
    :ivar status: 
    :ivar valid_until: The date and time in GMT in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format when the resource will be valid until.
    :ivar email: The email address that will receive updates when the Customer-Profile resource changes status.
    :ivar status_callback: The URL we call to inform your application of status changes.
    :ivar date_created: The date and time in GMT when the resource was created specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar date_updated: The date and time in GMT when the resource was last updated specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar url: The absolute URL of the Customer-Profile resource.
    :ivar links: The URLs of the Assigned Items of the Customer-Profile resource.
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.policy_sid: Optional[str] = payload.get("policy_sid")
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.status: Optional["TrustProductsInstance.Status"] = payload.get("status")
        self.valid_until: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("valid_until")
        )
        self.email: Optional[str] = payload.get("email")
        self.status_callback: Optional[str] = payload.get("status_callback")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.url: Optional[str] = payload.get("url")
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "sid": sid or self.sid,
        }
        self._context: Optional[TrustProductsContext] = None

    @property
    def _proxy(self) -> "TrustProductsContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: TrustProductsContext for this TrustProductsInstance
        """
        if self._context is None:
            self._context = TrustProductsContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the TrustProductsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the TrustProductsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "TrustProductsInstance":
        """
        Fetch the TrustProductsInstance


        :returns: The fetched TrustProductsInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "TrustProductsInstance":
        """
        Asynchronous coroutine to fetch the TrustProductsInstance


        :returns: The fetched TrustProductsInstance
        """
        return await self._proxy.fetch_async()

    def update(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        status_callback: Union[str, object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        email: Union[str, object] = values.unset,
    ) -> "TrustProductsInstance":
        """
        Update the TrustProductsInstance

        :param status:
        :param status_callback: The URL we call to inform your application of status changes.
        :param friendly_name: The string that you assigned to describe the resource.
        :param email: The email address that will receive updates when the Customer-Profile resource changes status.

        :returns: The updated TrustProductsInstance
        """
        return self._proxy.update(
            status=status,
            status_callback=status_callback,
            friendly_name=friendly_name,
            email=email,
        )

    async def update_async(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        status_callback: Union[str, object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        email: Union[str, object] = values.unset,
    ) -> "TrustProductsInstance":
        """
        Asynchronous coroutine to update the TrustProductsInstance

        :param status:
        :param status_callback: The URL we call to inform your application of status changes.
        :param friendly_name: The string that you assigned to describe the resource.
        :param email: The email address that will receive updates when the Customer-Profile resource changes status.

        :returns: The updated TrustProductsInstance
        """
        return await self._proxy.update_async(
            status=status,
            status_callback=status_callback,
            friendly_name=friendly_name,
            email=email,
        )

    @property
    def trust_products_channel_endpoint_assignment(
        self,
    ) -> TrustProductsChannelEndpointAssignmentList:
        """
        Access the trust_products_channel_endpoint_assignment
        """
        return self._proxy.trust_products_channel_endpoint_assignment

    @property
    def trust_products_entity_assignments(self) -> TrustProductsEntityAssignmentsList:
        """
        Access the trust_products_entity_assignments
        """
        return self._proxy.trust_products_entity_assignments

    @property
    def trust_products_evaluations(self) -> TrustProductsEvaluationsList:
        """
        Access the trust_products_evaluations
        """
        return self._proxy.trust_products_evaluations

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Trusthub.V1.TrustProductsInstance {}>".format(context)


class TrustProductsContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the TrustProductsContext

        :param version: Version that contains the resource
        :param sid: The unique string that we created to identify the Customer-Profile resource.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/TrustProducts/{sid}".format(**self._solution)

        self._trust_products_channel_endpoint_assignment: Optional[
            TrustProductsChannelEndpointAssignmentList
        ] = None
        self._trust_products_entity_assignments: Optional[
            TrustProductsEntityAssignmentsList
        ] = None
        self._trust_products_evaluations: Optional[TrustProductsEvaluationsList] = None

    def delete(self) -> bool:
        """
        Deletes the TrustProductsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the TrustProductsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> TrustProductsInstance:
        """
        Fetch the TrustProductsInstance


        :returns: The fetched TrustProductsInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return TrustProductsInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> TrustProductsInstance:
        """
        Asynchronous coroutine to fetch the TrustProductsInstance


        :returns: The fetched TrustProductsInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return TrustProductsInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    def update(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        status_callback: Union[str, object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        email: Union[str, object] = values.unset,
    ) -> TrustProductsInstance:
        """
        Update the TrustProductsInstance

        :param status:
        :param status_callback: The URL we call to inform your application of status changes.
        :param friendly_name: The string that you assigned to describe the resource.
        :param email: The email address that will receive updates when the Customer-Profile resource changes status.

        :returns: The updated TrustProductsInstance
        """
        data = values.of(
            {
                "Status": status,
                "StatusCallback": status_callback,
                "FriendlyName": friendly_name,
                "Email": email,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TrustProductsInstance(self._version, payload, sid=self._solution["sid"])

    async def update_async(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        status_callback: Union[str, object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        email: Union[str, object] = values.unset,
    ) -> TrustProductsInstance:
        """
        Asynchronous coroutine to update the TrustProductsInstance

        :param status:
        :param status_callback: The URL we call to inform your application of status changes.
        :param friendly_name: The string that you assigned to describe the resource.
        :param email: The email address that will receive updates when the Customer-Profile resource changes status.

        :returns: The updated TrustProductsInstance
        """
        data = values.of(
            {
                "Status": status,
                "StatusCallback": status_callback,
                "FriendlyName": friendly_name,
                "Email": email,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TrustProductsInstance(self._version, payload, sid=self._solution["sid"])

    @property
    def trust_products_channel_endpoint_assignment(
        self,
    ) -> TrustProductsChannelEndpointAssignmentList:
        """
        Access the trust_products_channel_endpoint_assignment
        """
        if self._trust_products_channel_endpoint_assignment is None:
            self._trust_products_channel_endpoint_assignment = (
                TrustProductsChannelEndpointAssignmentList(
                    self._version,
                    self._solution["sid"],
                )
            )
        return self._trust_products_channel_endpoint_assignment

    @property
    def trust_products_entity_assignments(self) -> TrustProductsEntityAssignmentsList:
        """
        Access the trust_products_entity_assignments
        """
        if self._trust_products_entity_assignments is None:
            self._trust_products_entity_assignments = (
                TrustProductsEntityAssignmentsList(
                    self._version,
                    self._solution["sid"],
                )
            )
        return self._trust_products_entity_assignments

    @property
    def trust_products_evaluations(self) -> TrustProductsEvaluationsList:
        """
        Access the trust_products_evaluations
        """
        if self._trust_products_evaluations is None:
            self._trust_products_evaluations = TrustProductsEvaluationsList(
                self._version,
                self._solution["sid"],
            )
        return self._trust_products_evaluations

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Trusthub.V1.TrustProductsContext {}>".format(context)


class TrustProductsPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> TrustProductsInstance:
        """
        Build an instance of TrustProductsInstance

        :param payload: Payload response from the API
        """
        return TrustProductsInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Trusthub.V1.TrustProductsPage>"


class TrustProductsList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the TrustProductsList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/TrustProducts"

    def create(
        self,
        friendly_name: str,
        email: str,
        policy_sid: str,
        status_callback: Union[str, object] = values.unset,
    ) -> TrustProductsInstance:
        """
        Create the TrustProductsInstance

        :param friendly_name: The string that you assigned to describe the resource.
        :param email: The email address that will receive updates when the Customer-Profile resource changes status.
        :param policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
        :param status_callback: The URL we call to inform your application of status changes.

        :returns: The created TrustProductsInstance
        """

        data = values.of(
            {
                "FriendlyName": friendly_name,
                "Email": email,
                "PolicySid": policy_sid,
                "StatusCallback": status_callback,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TrustProductsInstance(self._version, payload)

    async def create_async(
        self,
        friendly_name: str,
        email: str,
        policy_sid: str,
        status_callback: Union[str, object] = values.unset,
    ) -> TrustProductsInstance:
        """
        Asynchronously create the TrustProductsInstance

        :param friendly_name: The string that you assigned to describe the resource.
        :param email: The email address that will receive updates when the Customer-Profile resource changes status.
        :param policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
        :param status_callback: The URL we call to inform your application of status changes.

        :returns: The created TrustProductsInstance
        """

        data = values.of(
            {
                "FriendlyName": friendly_name,
                "Email": email,
                "PolicySid": policy_sid,
                "StatusCallback": status_callback,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return TrustProductsInstance(self._version, payload)

    def stream(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        policy_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[TrustProductsInstance]:
        """
        Streams TrustProductsInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param &quot;TrustProductsInstance.Status&quot; status: The verification status of the Customer-Profile resource.
        :param str friendly_name: The string that you assigned to describe the resource.
        :param str policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
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
            friendly_name=friendly_name,
            policy_sid=policy_sid,
            page_size=limits["page_size"],
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        policy_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[TrustProductsInstance]:
        """
        Asynchronously streams TrustProductsInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param &quot;TrustProductsInstance.Status&quot; status: The verification status of the Customer-Profile resource.
        :param str friendly_name: The string that you assigned to describe the resource.
        :param str policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
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
            friendly_name=friendly_name,
            policy_sid=policy_sid,
            page_size=limits["page_size"],
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        policy_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[TrustProductsInstance]:
        """
        Lists TrustProductsInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param &quot;TrustProductsInstance.Status&quot; status: The verification status of the Customer-Profile resource.
        :param str friendly_name: The string that you assigned to describe the resource.
        :param str policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
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
                friendly_name=friendly_name,
                policy_sid=policy_sid,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        policy_sid: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[TrustProductsInstance]:
        """
        Asynchronously lists TrustProductsInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param &quot;TrustProductsInstance.Status&quot; status: The verification status of the Customer-Profile resource.
        :param str friendly_name: The string that you assigned to describe the resource.
        :param str policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
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
                friendly_name=friendly_name,
                policy_sid=policy_sid,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        policy_sid: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> TrustProductsPage:
        """
        Retrieve a single page of TrustProductsInstance records from the API.
        Request is executed immediately

        :param status: The verification status of the Customer-Profile resource.
        :param friendly_name: The string that you assigned to describe the resource.
        :param policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of TrustProductsInstance
        """
        data = values.of(
            {
                "Status": status,
                "FriendlyName": friendly_name,
                "PolicySid": policy_sid,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return TrustProductsPage(self._version, response)

    async def page_async(
        self,
        status: Union["TrustProductsInstance.Status", object] = values.unset,
        friendly_name: Union[str, object] = values.unset,
        policy_sid: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> TrustProductsPage:
        """
        Asynchronously retrieve a single page of TrustProductsInstance records from the API.
        Request is executed immediately

        :param status: The verification status of the Customer-Profile resource.
        :param friendly_name: The string that you assigned to describe the resource.
        :param policy_sid: The unique string of a policy that is associated to the Customer-Profile resource.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of TrustProductsInstance
        """
        data = values.of(
            {
                "Status": status,
                "FriendlyName": friendly_name,
                "PolicySid": policy_sid,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return TrustProductsPage(self._version, response)

    def get_page(self, target_url: str) -> TrustProductsPage:
        """
        Retrieve a specific page of TrustProductsInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of TrustProductsInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return TrustProductsPage(self._version, response)

    async def get_page_async(self, target_url: str) -> TrustProductsPage:
        """
        Asynchronously retrieve a specific page of TrustProductsInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of TrustProductsInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return TrustProductsPage(self._version, response)

    def get(self, sid: str) -> TrustProductsContext:
        """
        Constructs a TrustProductsContext

        :param sid: The unique string that we created to identify the Customer-Profile resource.
        """
        return TrustProductsContext(self._version, sid=sid)

    def __call__(self, sid: str) -> TrustProductsContext:
        """
        Constructs a TrustProductsContext

        :param sid: The unique string that we created to identify the Customer-Profile resource.
        """
        return TrustProductsContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Trusthub.V1.TrustProductsList>"
