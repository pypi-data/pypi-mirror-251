r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Messaging
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""


from datetime import datetime
from typing import Any, Dict, Optional
from twilio.base import deserialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version


class DomainCertsInstance(InstanceResource):

    """
    :ivar domain_sid: The unique string that we created to identify the Domain resource.
    :ivar date_updated: Date that this Domain was last updated.
    :ivar date_expires: Date that the private certificate associated with this domain expires. You will need to update the certificate before that date to ensure your shortened links will continue to work.
    :ivar date_created: Date that this Domain was registered to the Twilio platform to create a new Domain object.
    :ivar domain_name: Full url path for this domain.
    :ivar certificate_sid: The unique string that we created to identify this Certificate resource.
    :ivar url:
    :ivar cert_in_validation: Optional JSON field describing the status and upload date of a new certificate in the process of validation
    """

    def __init__(
        self,
        version: Version,
        payload: Dict[str, Any],
        domain_sid: Optional[str] = None,
    ):
        super().__init__(version)

        self.domain_sid: Optional[str] = payload.get("domain_sid")
        self.date_updated: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_updated")
        )
        self.date_expires: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_expires")
        )
        self.date_created: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("date_created")
        )
        self.domain_name: Optional[str] = payload.get("domain_name")
        self.certificate_sid: Optional[str] = payload.get("certificate_sid")
        self.url: Optional[str] = payload.get("url")
        self.cert_in_validation: Optional[Dict[str, object]] = payload.get(
            "cert_in_validation"
        )

        self._solution = {
            "domain_sid": domain_sid or self.domain_sid,
        }
        self._context: Optional[DomainCertsContext] = None

    @property
    def _proxy(self) -> "DomainCertsContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: DomainCertsContext for this DomainCertsInstance
        """
        if self._context is None:
            self._context = DomainCertsContext(
                self._version,
                domain_sid=self._solution["domain_sid"],
            )
        return self._context

    def delete(self) -> bool:
        """
        Deletes the DomainCertsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._proxy.delete()

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the DomainCertsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._proxy.delete_async()

    def fetch(self) -> "DomainCertsInstance":
        """
        Fetch the DomainCertsInstance


        :returns: The fetched DomainCertsInstance
        """
        return self._proxy.fetch()

    async def fetch_async(self) -> "DomainCertsInstance":
        """
        Asynchronous coroutine to fetch the DomainCertsInstance


        :returns: The fetched DomainCertsInstance
        """
        return await self._proxy.fetch_async()

    def update(self, tls_cert: str) -> "DomainCertsInstance":
        """
        Update the DomainCertsInstance

        :param tls_cert: Contains the full TLS certificate and private for this domain in PEM format: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail. Twilio uses this information to process HTTPS traffic sent to your domain.

        :returns: The updated DomainCertsInstance
        """
        return self._proxy.update(
            tls_cert=tls_cert,
        )

    async def update_async(self, tls_cert: str) -> "DomainCertsInstance":
        """
        Asynchronous coroutine to update the DomainCertsInstance

        :param tls_cert: Contains the full TLS certificate and private for this domain in PEM format: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail. Twilio uses this information to process HTTPS traffic sent to your domain.

        :returns: The updated DomainCertsInstance
        """
        return await self._proxy.update_async(
            tls_cert=tls_cert,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Messaging.V1.DomainCertsInstance {}>".format(context)


class DomainCertsContext(InstanceContext):
    def __init__(self, version: Version, domain_sid: str):
        """
        Initialize the DomainCertsContext

        :param version: Version that contains the resource
        :param domain_sid: Unique string used to identify the domain that this certificate should be associated with.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "domain_sid": domain_sid,
        }
        self._uri = "/LinkShortening/Domains/{domain_sid}/Certificate".format(
            **self._solution
        )

    def delete(self) -> bool:
        """
        Deletes the DomainCertsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return self._version.delete(
            method="DELETE",
            uri=self._uri,
        )

    async def delete_async(self) -> bool:
        """
        Asynchronous coroutine that deletes the DomainCertsInstance


        :returns: True if delete succeeds, False otherwise
        """
        return await self._version.delete_async(
            method="DELETE",
            uri=self._uri,
        )

    def fetch(self) -> DomainCertsInstance:
        """
        Fetch the DomainCertsInstance


        :returns: The fetched DomainCertsInstance
        """

        payload = self._version.fetch(
            method="GET",
            uri=self._uri,
        )

        return DomainCertsInstance(
            self._version,
            payload,
            domain_sid=self._solution["domain_sid"],
        )

    async def fetch_async(self) -> DomainCertsInstance:
        """
        Asynchronous coroutine to fetch the DomainCertsInstance


        :returns: The fetched DomainCertsInstance
        """

        payload = await self._version.fetch_async(
            method="GET",
            uri=self._uri,
        )

        return DomainCertsInstance(
            self._version,
            payload,
            domain_sid=self._solution["domain_sid"],
        )

    def update(self, tls_cert: str) -> DomainCertsInstance:
        """
        Update the DomainCertsInstance

        :param tls_cert: Contains the full TLS certificate and private for this domain in PEM format: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail. Twilio uses this information to process HTTPS traffic sent to your domain.

        :returns: The updated DomainCertsInstance
        """
        data = values.of(
            {
                "TlsCert": tls_cert,
            }
        )

        payload = self._version.update(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return DomainCertsInstance(
            self._version, payload, domain_sid=self._solution["domain_sid"]
        )

    async def update_async(self, tls_cert: str) -> DomainCertsInstance:
        """
        Asynchronous coroutine to update the DomainCertsInstance

        :param tls_cert: Contains the full TLS certificate and private for this domain in PEM format: https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail. Twilio uses this information to process HTTPS traffic sent to your domain.

        :returns: The updated DomainCertsInstance
        """
        data = values.of(
            {
                "TlsCert": tls_cert,
            }
        )

        payload = await self._version.update_async(
            method="POST",
            uri=self._uri,
            data=data,
        )

        return DomainCertsInstance(
            self._version, payload, domain_sid=self._solution["domain_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Messaging.V1.DomainCertsContext {}>".format(context)


class DomainCertsList(ListResource):
    def __init__(self, version: Version):
        """
        Initialize the DomainCertsList

        :param version: Version that contains the resource

        """
        super().__init__(version)

    def get(self, domain_sid: str) -> DomainCertsContext:
        """
        Constructs a DomainCertsContext

        :param domain_sid: Unique string used to identify the domain that this certificate should be associated with.
        """
        return DomainCertsContext(self._version, domain_sid=domain_sid)

    def __call__(self, domain_sid: str) -> DomainCertsContext:
        """
        Constructs a DomainCertsContext

        :param domain_sid: Unique string used to identify the domain that this certificate should be associated with.
        """
        return DomainCertsContext(self._version, domain_sid=domain_sid)

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Messaging.V1.DomainCertsList>"
