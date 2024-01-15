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


from typing import Optional


from twilio.base.list_resource import ListResource
from twilio.base.version import Version

from twilio.rest.api.v2010.account.sip.domain.auth_types.auth_type_calls import (
    AuthTypeCallsList,
)
from twilio.rest.api.v2010.account.sip.domain.auth_types.auth_type_registrations import (
    AuthTypeRegistrationsList,
)


class AuthTypesList(ListResource):
    def __init__(self, version: Version, account_sid: str, domain_sid: str):
        """
        Initialize the AuthTypesList

        :param version: Version that contains the resource
        :param account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the CredentialListMapping resource to fetch.
        :param domain_sid: The SID of the SIP domain that contains the resource to fetch.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "account_sid": account_sid,
            "domain_sid": domain_sid,
        }
        self._uri = "/Accounts/{account_sid}/SIP/Domains/{domain_sid}/Auth.json".format(
            **self._solution
        )

        self._calls: Optional[AuthTypeCallsList] = None
        self._registrations: Optional[AuthTypeRegistrationsList] = None

    @property
    def calls(self) -> AuthTypeCallsList:
        """
        Access the calls
        """
        if self._calls is None:
            self._calls = AuthTypeCallsList(
                self._version,
                account_sid=self._solution["account_sid"],
                domain_sid=self._solution["domain_sid"],
            )
        return self._calls

    @property
    def registrations(self) -> AuthTypeRegistrationsList:
        """
        Access the registrations
        """
        if self._registrations is None:
            self._registrations = AuthTypeRegistrationsList(
                self._version,
                account_sid=self._solution["account_sid"],
                domain_sid=self._solution["domain_sid"],
            )
        return self._registrations

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Api.V2010.AuthTypesList>"
