r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Conversations
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from twilio.base import deserialize, values

from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version
from twilio.base.page import Page


class ParticipantConversationInstance(InstanceResource):
    class State(object):
        INACTIVE = "inactive"
        ACTIVE = "active"
        CLOSED = "closed"

    """
    :ivar account_sid: The unique ID of the [Account](https://www.twilio.com/docs/iam/api/account) responsible for this conversation.
    :ivar chat_service_sid: The unique ID of the [Conversation Service](https://www.twilio.com/docs/conversations/api/service-resource) this conversation belongs to.
    :ivar participant_sid: The unique ID of the [Participant](https://www.twilio.com/docs/conversations/api/conversation-participant-resource).
    :ivar participant_user_sid: The unique string that identifies the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource).
    :ivar participant_identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
    :ivar participant_messaging_binding: Information about how this participant exchanges messages with the conversation. A JSON parameter consisting of type and address fields of the participant.
    :ivar conversation_sid: The unique ID of the [Conversation](https://www.twilio.com/docs/conversations/api/conversation-resource) this Participant belongs to.
    :ivar conversation_unique_name: An application-defined string that uniquely identifies the Conversation resource.
    :ivar conversation_friendly_name: The human-readable name of this conversation, limited to 256 characters. Optional.
    :ivar conversation_attributes: An optional string metadata field you can use to store any data you wish. The string value must contain structurally valid JSON if specified.  **Note** that if the attributes are not set \"{}\" will be returned.
    :ivar conversation_date_created: The date that this conversation was created, given in ISO 8601 format.
    :ivar conversation_date_updated: The date that this conversation was last updated, given in ISO 8601 format.
    :ivar conversation_created_by: Identity of the creator of this Conversation.
    :ivar conversation_state: 
    :ivar conversation_timers: Timer date values representing state update for this conversation.
    :ivar links: Contains absolute URLs to access the [participant](https://www.twilio.com/docs/conversations/api/conversation-participant-resource) and [conversation](https://www.twilio.com/docs/conversations/api/conversation-resource) of this conversation.
    """

    def __init__(
        self, version: Version, payload: Dict[str, Any], chat_service_sid: str
    ):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.chat_service_sid: Optional[str] = payload.get("chat_service_sid")
        self.participant_sid: Optional[str] = payload.get("participant_sid")
        self.participant_user_sid: Optional[str] = payload.get("participant_user_sid")
        self.participant_identity: Optional[str] = payload.get("participant_identity")
        self.participant_messaging_binding: Optional[Dict[str, object]] = payload.get(
            "participant_messaging_binding"
        )
        self.conversation_sid: Optional[str] = payload.get("conversation_sid")
        self.conversation_unique_name: Optional[str] = payload.get(
            "conversation_unique_name"
        )
        self.conversation_friendly_name: Optional[str] = payload.get(
            "conversation_friendly_name"
        )
        self.conversation_attributes: Optional[str] = payload.get(
            "conversation_attributes"
        )
        self.conversation_date_created: Optional[
            datetime
        ] = deserialize.iso8601_datetime(payload.get("conversation_date_created"))
        self.conversation_date_updated: Optional[
            datetime
        ] = deserialize.iso8601_datetime(payload.get("conversation_date_updated"))
        self.conversation_created_by: Optional[str] = payload.get(
            "conversation_created_by"
        )
        self.conversation_state: Optional[
            "ParticipantConversationInstance.State"
        ] = payload.get("conversation_state")
        self.conversation_timers: Optional[Dict[str, object]] = payload.get(
            "conversation_timers"
        )
        self.links: Optional[Dict[str, object]] = payload.get("links")

        self._solution = {
            "chat_service_sid": chat_service_sid,
        }

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Conversations.V1.ParticipantConversationInstance {}>".format(
            context
        )


class ParticipantConversationPage(Page):
    def get_instance(self, payload: Dict[str, Any]) -> ParticipantConversationInstance:
        """
        Build an instance of ParticipantConversationInstance

        :param payload: Payload response from the API
        """
        return ParticipantConversationInstance(
            self._version, payload, chat_service_sid=self._solution["chat_service_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Conversations.V1.ParticipantConversationPage>"


class ParticipantConversationList(ListResource):
    def __init__(self, version: Version, chat_service_sid: str):
        """
        Initialize the ParticipantConversationList

        :param version: Version that contains the resource
        :param chat_service_sid: The SID of the [Conversation Service](https://www.twilio.com/docs/conversations/api/service-resource) the Participant Conversations resource is associated with.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "chat_service_sid": chat_service_sid,
        }
        self._uri = "/Services/{chat_service_sid}/ParticipantConversations".format(
            **self._solution
        )

    def stream(
        self,
        identity: Union[str, object] = values.unset,
        address: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[ParticipantConversationInstance]:
        """
        Streams ParticipantConversationInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param str identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
        :param str address: A unique string identifier for the conversation participant who's not a Conversation User. This parameter could be found in messaging_binding.address field of Participant resource. It should be url-encoded.
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
            identity=identity, address=address, page_size=limits["page_size"]
        )

        return self._version.stream(page, limits["limit"])

    async def stream_async(
        self,
        identity: Union[str, object] = values.unset,
        address: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> AsyncIterator[ParticipantConversationInstance]:
        """
        Asynchronously streams ParticipantConversationInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param str identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
        :param str address: A unique string identifier for the conversation participant who's not a Conversation User. This parameter could be found in messaging_binding.address field of Participant resource. It should be url-encoded.
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
            identity=identity, address=address, page_size=limits["page_size"]
        )

        return self._version.stream_async(page, limits["limit"])

    def list(
        self,
        identity: Union[str, object] = values.unset,
        address: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[ParticipantConversationInstance]:
        """
        Lists ParticipantConversationInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param str identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
        :param str address: A unique string identifier for the conversation participant who's not a Conversation User. This parameter could be found in messaging_binding.address field of Participant resource. It should be url-encoded.
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
                identity=identity,
                address=address,
                limit=limit,
                page_size=page_size,
            )
        )

    async def list_async(
        self,
        identity: Union[str, object] = values.unset,
        address: Union[str, object] = values.unset,
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[ParticipantConversationInstance]:
        """
        Asynchronously lists ParticipantConversationInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param str identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
        :param str address: A unique string identifier for the conversation participant who's not a Conversation User. This parameter could be found in messaging_binding.address field of Participant resource. It should be url-encoded.
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
                identity=identity,
                address=address,
                limit=limit,
                page_size=page_size,
            )
        ]

    def page(
        self,
        identity: Union[str, object] = values.unset,
        address: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> ParticipantConversationPage:
        """
        Retrieve a single page of ParticipantConversationInstance records from the API.
        Request is executed immediately

        :param identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
        :param address: A unique string identifier for the conversation participant who's not a Conversation User. This parameter could be found in messaging_binding.address field of Participant resource. It should be url-encoded.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of ParticipantConversationInstance
        """
        data = values.of(
            {
                "Identity": identity,
                "Address": address,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = self._version.page(method="GET", uri=self._uri, params=data)
        return ParticipantConversationPage(self._version, response, self._solution)

    async def page_async(
        self,
        identity: Union[str, object] = values.unset,
        address: Union[str, object] = values.unset,
        page_token: Union[str, object] = values.unset,
        page_number: Union[int, object] = values.unset,
        page_size: Union[int, object] = values.unset,
    ) -> ParticipantConversationPage:
        """
        Asynchronously retrieve a single page of ParticipantConversationInstance records from the API.
        Request is executed immediately

        :param identity: A unique string identifier for the conversation participant as [Conversation User](https://www.twilio.com/docs/conversations/api/user-resource). This parameter is non-null if (and only if) the participant is using the Conversations SDK to communicate. Limited to 256 characters.
        :param address: A unique string identifier for the conversation participant who's not a Conversation User. This parameter could be found in messaging_binding.address field of Participant resource. It should be url-encoded.
        :param page_token: PageToken provided by the API
        :param page_number: Page Number, this value is simply for client state
        :param page_size: Number of records to return, defaults to 50

        :returns: Page of ParticipantConversationInstance
        """
        data = values.of(
            {
                "Identity": identity,
                "Address": address,
                "PageToken": page_token,
                "Page": page_number,
                "PageSize": page_size,
            }
        )

        response = await self._version.page_async(
            method="GET", uri=self._uri, params=data
        )
        return ParticipantConversationPage(self._version, response, self._solution)

    def get_page(self, target_url: str) -> ParticipantConversationPage:
        """
        Retrieve a specific page of ParticipantConversationInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of ParticipantConversationInstance
        """
        response = self._version.domain.twilio.request("GET", target_url)
        return ParticipantConversationPage(self._version, response, self._solution)

    async def get_page_async(self, target_url: str) -> ParticipantConversationPage:
        """
        Asynchronously retrieve a specific page of ParticipantConversationInstance records from the API.
        Request is executed immediately

        :param target_url: API-generated URL for the requested results page

        :returns: Page of ParticipantConversationInstance
        """
        response = await self._version.domain.twilio.request_async("GET", target_url)
        return ParticipantConversationPage(self._version, response, self._solution)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Conversations.V1.ParticipantConversationList>"
