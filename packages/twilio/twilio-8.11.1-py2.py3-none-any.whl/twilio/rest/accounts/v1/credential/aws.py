r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Accounts
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


class AwsInstance(InstanceResource):

    """
    :ivar sid: The unique string that we created to identify the AWS resource.
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the AWS resource.
    :ivar friendly_name: The string that you assigned to describe the resource.
    :ivar date_created: The date and time in GMT when the resource was created specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar date_updated: The date and time in GMT when the resource was last updated specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar url: The URI for this resource, relative to `https://accounts.twilio.com`
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], sid: Optional[str] = None
    ):
        super().__init__(version)

        self.sid: Optional[str] = payload.get("sid")
        self.account_sid: Optional[str] = payload.get("account_sid")
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "sid": sid or self.sid,
        }
        self._context: Optional[AwsContext] = None

    @property
    def _proxy(self) -> "AwsContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: AwsContext for this AwsInstance
        """
        if self._context is None:
            self._context = AwsContext(
                self._version,
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the AwsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the AwsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "AwsInstance":
        """
        Fetch the AwsInstance


        :returns: The fetched AwsInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "AwsInstance":
        """
        Asynchronous coroutine to fetch the AwsInstance


        :returns: The fetched AwsInstance
        """
        return await self._proxy.fetch_async()

    def update(self, friendly_name: Union[str, object] = values.unset) -> "AwsInstance":
        """
        Update the AwsInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It can be up to 64 characters long.

        :returns: The updated AwsInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
        )

    async def update_async(
        self, friendly_name: Union[str, object] = values.unset
    ) -> "AwsInstance":
        """
        Asynchronous coroutine to update the AwsInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It can be up to 64 characters long.

        :returns: The updated AwsInstance
        """
        return await self._proxy.update_async(
            friendly_name=friendly_name,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Accounts.V1.AwsInstance {}>".format(context)


class AwsContext(InstanceContext):
    def __init__(self, version: Version, sid: str):
        """
        Initialize the AwsContext

        :param version: Version that contains the resource
        :param sid: The Twilio-provided string that uniquely identifies the AWS resource to update.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "sid": sid,
        }
        self._uri = "/Credentials/AWS/{sid}".format(**self._solution)

    def delete(self) -> bool:
        """
        Deletes the AwsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the AwsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> AwsInstance:
        """
        Fetch the AwsInstance


        :returns: The fetched AwsInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return AwsInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> AwsInstance:
        """
        Asynchronous coroutine to fetch the AwsInstance


        :returns: The fetched AwsInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return AwsInstance(
            self._version,
            payload,
            sid=self._solution["sid"],
        )

    def update(self, friendly_name: Union[str, object] = values.unset) -> AwsInstance:
        """
        Update the AwsInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It can be up to 64 characters long.

        :returns: The updated AwsInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return AwsInstance(self._version, payload, sid=self._solution["sid"])

    async def update_async(
        self, friendly_name: Union[str, object] = values.unset
    ) -> AwsInstance:
        """
        Asynchronous coroutine to update the AwsInstance

        :param friendly_name: A descriptive string that you create to describe the resource. It can be up to 64 characters long.

        :returns: The updated AwsInstance
        """
        data = values.of(
            {
                "FriendlyName": friendly_name,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return AwsInstance(self._version, payload, sid=self._solution["sid"])

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Accounts.V1.AwsContext {}>".format(context)


class AwsPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> AwsInstance:
        """
        Build an instance of AwsInstance

        :param payload: Payload response from the API
        """
        return AwsInstance(self._version, payload)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Accounts.V1.AwsPage>"


class AwsList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the AwsList

        :param version: Version that contains the resource

        """
        super().__init__(version)

        self._uri = "/Credentials/AWS"

    def create(
        self,
        credentials: str,
        friendly_name: Union[str, object] = values.unset,
        account_sid: Union[str, object] = values.unset,
    ) -> AwsInstance:
        """
        Create the AwsInstance

        :param credentials: A string that contains the AWS access credentials in the format `<AWS_ACCESS_KEY_ID>:<AWS_SECRET_ACCESS_KEY>`. For example, `AKIAIOSFODNN7EXAMPLE:wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
        :param friendly_name: A descriptive string that you create to describe the resource. It can be up to 64 characters long.
        :param account_sid: The SID of the Subaccount that this Credential should be associated with. Must be a valid Subaccount of the account issuing the request.

        :returns: The created AwsInstance
        """

        data = values.of(
            {
                "Credentials": credentials,
                "FriendlyName": friendly_name,
                "AccountSid": account_sid,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return AwsInstance(self._version, payload)

    async def create_async(
        self,
        credentials: str,
        friendly_name: Union[str, object] = values.unset,
        account_sid: Union[str, object] = values.unset,
    ) -> AwsInstance:
        """
        Asynchronously create the AwsInstance

        :param credentials: A string that contains the AWS access credentials in the format `<AWS_ACCESS_KEY_ID>:<AWS_SECRET_ACCESS_KEY>`. For example, `AKIAIOSFODNN7EXAMPLE:wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
        :param friendly_name: A descriptive string that you create to describe the resource. It can be up to 64 characters long.
        :param account_sid: The SID of the Subaccount that this Credential should be associated with. Must be a valid Subaccount of the account issuing the request.

        :returns: The created AwsInstance
        """

        data = values.of(
            {
                "Credentials": credentials,
                "FriendlyName": friendly_name,
                "AccountSid": account_sid,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return AwsInstance(self._version, payload)

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[AwsInstance]:
        """
        Streams AwsInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[AwsInstance]:
        """
        Asynchronously streams AwsInstance records from the API as a generator stream.
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
    ) -> List[AwsInstance]:
        """
        Lists AwsInstance records from the API as a list.
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
    ) -> List[AwsInstance]:
        """
        Asynchronously lists AwsInstance records from the API as a list.
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
    ) -> AwsPage:
        """
        Retrieve a single page of AwsInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of AwsInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return AwsPage(self._version, response)

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> AwsPage:
        """
        Asynchronously retrieve a single page of AwsInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of AwsInstance
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
        return AwsPage(self._version, response)

    def get_page(self, target_url: str) -> AwsPage:
        """
        Retrieve a specific page of AwsInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of AwsInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return AwsPage(self._version, response)

    async def get_page_async(self, target_url: str) -> AwsPage:
        """
        Asynchronously retrieve a specific page of AwsInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of AwsInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return AwsPage(self._version, response)

    def get(self, sid: str) -> AwsContext:
        """
        Constructs a AwsContext

        :param sid: The Twilio-provided string that uniquely identifies the AWS resource to update.
        """
        return AwsContext(self._version, sid=sid)

    def __call__(self, sid: str) -> AwsContext:
        """
        Constructs a AwsContext

        :param sid: The Twilio-provided string that uniquely identifies the AWS resource to update.
        """
        return AwsContext(self._version, sid=sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Accounts.V1.AwsList>"
