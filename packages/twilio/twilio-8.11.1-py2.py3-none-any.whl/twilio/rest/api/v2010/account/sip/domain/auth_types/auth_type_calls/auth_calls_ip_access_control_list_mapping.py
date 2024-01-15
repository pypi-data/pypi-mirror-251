r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Api
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


class AuthCallsIpAccessControlListMappingInstance(InstanceResource):

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the IpAccessControlListMapping resource.
    :ivar date_created: The date and time in GMT that the resource was created specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar date_updated: The date and time in GMT that the resource was last updated specified in [RFC 2822](https://www.ietf.org/rfc/rfc2822.txt) format.
    :ivar friendly_name: The string that you assigned to describe the resource.
    :ivar sid: The unique string that that we created to identify the IpAccessControlListMapping resource.
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        account_sid: str,
        domain_sid: str,
        sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.date_created: Optional[datetime] = deserialize.rfc2822_datetime(
            payload.get("date_created")
        )
        self.date_updated: Optional[datetime] = deserialize.rfc2822_datetime(
            payload.get("date_updated")
        )
        self.friendly_name: Optional[str] = payload.get("friendly_name")
        self.sid: Optional[str] = payload.get("sid")

        self._solution = {
            "account_sid": account_sid,
            "domain_sid": domain_sid,
            "sid": sid or self.sid,
        }
        self._context: Optional[AuthCallsIpAccessControlListMappingContext] = None

    @property
    def _proxy(self) -> "AuthCallsIpAccessControlListMappingContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: AuthCallsIpAccessControlListMappingContext for this AuthCallsIpAccessControlListMappingInstance
        """
        if self._context is None:
            self._context = AuthCallsIpAccessControlListMappingContext(
                self._version,
                account_sid=self._solution["account_sid"],
                domain_sid=self._solution["domain_sid"],
                sid=self._solution["sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the AuthCallsIpAccessControlListMappingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the AuthCallsIpAccessControlListMappingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "AuthCallsIpAccessControlListMappingInstance":
        """
        Fetch the AuthCallsIpAccessControlListMappingInstance


        :returns: The fetched AuthCallsIpAccessControlListMappingInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "AuthCallsIpAccessControlListMappingInstance":
        """
        Asynchronous coroutine to fetch the AuthCallsIpAccessControlListMappingInstance


        :returns: The fetched AuthCallsIpAccessControlListMappingInstance
        """
        return await self._proxy.fetch_async()

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return (
            "<Twilio.Api.V2010.AuthCallsIpAccessControlListMappingInstance {}>".format(
                context
            )
        )


class AuthCallsIpAccessControlListMappingContext(InstanceContext):
    def __init__(self, version: Version, account_sid: str, domain_sid: str, sid: str):
        """
        Initialize the AuthCallsIpAccessControlListMappingContext

        :param version: Version that contains the resource
        :param account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the IpAccessControlListMapping resource to fetch.
        :param domain_sid: The SID of the SIP domain that contains the resource to fetch.
        :param sid: The Twilio-provided string that uniquely identifies the IpAccessControlListMapping resource to fetch.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "account_sid": account_sid,
            "domain_sid": domain_sid,
            "sid": sid,
        }
        self._uri = "/Accounts/{account_sid}/SIP/Domains/{domain_sid}/Auth/Calls/IpAccessControlListMappings/{sid}.json".format(
            **self._solution
        )

    def delete(self) -> bool:
        """
        Deletes the AuthCallsIpAccessControlListMappingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the AuthCallsIpAccessControlListMappingInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> AuthCallsIpAccessControlListMappingInstance:
        """
        Fetch the AuthCallsIpAccessControlListMappingInstance


        :returns: The fetched AuthCallsIpAccessControlListMappingInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return AuthCallsIpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
            sid=self._solution["sid"],
        )

    async def fetch_async(self) -> AuthCallsIpAccessControlListMappingInstance:
        """
        Asynchronous coroutine to fetch the AuthCallsIpAccessControlListMappingInstance


        :returns: The fetched AuthCallsIpAccessControlListMappingInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return AuthCallsIpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
            sid=self._solution["sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return (
            "<Twilio.Api.V2010.AuthCallsIpAccessControlListMappingContext {}>".format(
                context
            )
        )


class AuthCallsIpAccessControlListMappingPage(Page):
    def get_instance(
        self, payload: Dict[str, Any]
    ) -> AuthCallsIpAccessControlListMappingInstance:
        """
        Build an instance of AuthCallsIpAccessControlListMappingInstance

        :param payload: Payload response from the API
        """
        return AuthCallsIpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Api.V2010.AuthCallsIpAccessControlListMappingPage>"


class AuthCallsIpAccessControlListMappingList(ListResource):
    def __init__(self, version: Version, account_sid: str, domain_sid: str):
        """
        Initialize the AuthCallsIpAccessControlListMappingList

        :param version: Version that contains the resource
        :param account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the IpAccessControlListMapping resources to read.
        :param domain_sid: The SID of the SIP domain that contains the resources to read.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "account_sid": account_sid,
            "domain_sid": domain_sid,
        }
        self._uri = "/Accounts/{account_sid}/SIP/Domains/{domain_sid}/Auth/Calls/IpAccessControlListMappings.json".format(
            **self._solution
        )

    def create(
        self, ip_access_control_list_sid: str
    ) -> AuthCallsIpAccessControlListMappingInstance:
        """
        Create the AuthCallsIpAccessControlListMappingInstance

        :param ip_access_control_list_sid: The SID of the IpAccessControlList resource to map to the SIP domain.

        :returns: The created AuthCallsIpAccessControlListMappingInstance
        """

        data = values.of(
            {
                "IpAccessControlListSid": ip_access_control_list_sid,
            }
        )

        payload = self._version.create(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return AuthCallsIpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
        )

    async def create_async(
        self, ip_access_control_list_sid: str
    ) -> AuthCallsIpAccessControlListMappingInstance:
        """
        Asynchronously create the AuthCallsIpAccessControlListMappingInstance

        :param ip_access_control_list_sid: The SID of the IpAccessControlList resource to map to the SIP domain.

        :returns: The created AuthCallsIpAccessControlListMappingInstance
        """

        data = values.of(
            {
                "IpAccessControlListSid": ip_access_control_list_sid,
            }
        )

        payload = await self._version.create_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return AuthCallsIpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
        )

    def stream(
        self,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[AuthCallsIpAccessControlListMappingInstance]:
        """
        Streams AuthCallsIpAccessControlListMappingInstance records from the API as a generator stream.
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
    ) -> AsyncIterator[AuthCallsIpAccessControlListMappingInstance]:
        """
        Asynchronously streams AuthCallsIpAccessControlListMappingInstance records from the API as a generator stream.
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
    ) -> List[AuthCallsIpAccessControlListMappingInstance]:
        """
        Lists AuthCallsIpAccessControlListMappingInstance records from the API as a list.
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
    ) -> List[AuthCallsIpAccessControlListMappingInstance]:
        """
        Asynchronously lists AuthCallsIpAccessControlListMappingInstance records from the API as a list.
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
    ) -> AuthCallsIpAccessControlListMappingPage:
        """
        Retrieve a single page of AuthCallsIpAccessControlListMappingInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of AuthCallsIpAccessControlListMappingInstance
        """
        data = values.of(
            {
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return AuthCallsIpAccessControlListMappingPage(
            self._version, response, self._solution
        )

    async def page_async(
        self,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> AuthCallsIpAccessControlListMappingPage:
        """
        Asynchronously retrieve a single page of AuthCallsIpAccessControlListMappingInstance records from the API.
        Request is executed immediately

        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of AuthCallsIpAccessControlListMappingInstance
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
        return AuthCallsIpAccessControlListMappingPage(
            self._version, response, self._solution
        )

    def get_page(self, target_url: str) -> AuthCallsIpAccessControlListMappingPage:
        """
        Retrieve a specific page of AuthCallsIpAccessControlListMappingInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of AuthCallsIpAccessControlListMappingInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return AuthCallsIpAccessControlListMappingPage(
            self._version, response, self._solution
        )

    async def get_page_async(
        self, target_url: str
    ) -> AuthCallsIpAccessControlListMappingPage:
        """
        Asynchronously retrieve a specific page of AuthCallsIpAccessControlListMappingInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of AuthCallsIpAccessControlListMappingInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return AuthCallsIpAccessControlListMappingPage(
            self._version, response, self._solution
        )

    def get(self, sid: str) -> AuthCallsIpAccessControlListMappingContext:
        """
        Constructs a AuthCallsIpAccessControlListMappingContext

        :param sid: The Twilio-provided string that uniquely identifies the IpAccessControlListMapping resource to fetch.
        """
        return AuthCallsIpAccessControlListMappingContext(
            self._version,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
            sid=sid,
        )

    def __call__(self, sid: str) -> AuthCallsIpAccessControlListMappingContext:
        """
        Constructs a AuthCallsIpAccessControlListMappingContext

        :param sid: The Twilio-provided string that uniquely identifies the IpAccessControlListMapping resource to fetch.
        """
        return AuthCallsIpAccessControlListMappingContext(
            self._version,
            account_sid=self._solution["account_sid"],
            domain_sid=self._solution["domain_sid"],
            sid=sid,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Api.V2010.AuthCallsIpAccessControlListMappingList>"
