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
from typing import Any, Dict, Optional, Union
from twilio.base import deserialize, serialize, values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.version import Version


class WorkspaceCumulativeStatisticsInstance(InstanceResource):

    """
    :ivar account_sid: The SID of the [Account](https://www.twilio.com/docs/iam/api/account) that created the Workspace resource.
    :ivar avg_task_acceptance_time: The average time in seconds between Task creation and acceptance.
    :ivar start_time: The beginning of the interval during which these statistics were calculated, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar end_time: The end of the interval during which these statistics were calculated, in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
    :ivar reservations_created: The total number of Reservations that were created for Workers.
    :ivar reservations_accepted: The total number of Reservations accepted by Workers.
    :ivar reservations_rejected: The total number of Reservations that were rejected.
    :ivar reservations_timed_out: The total number of Reservations that were timed out.
    :ivar reservations_canceled: The total number of Reservations that were canceled.
    :ivar reservations_rescinded: The total number of Reservations that were rescinded.
    :ivar split_by_wait_time: A list of objects that describe the number of Tasks canceled and reservations accepted above and below the thresholds specified in seconds.
    :ivar wait_duration_until_accepted: The wait duration statistics (`avg`, `min`, `max`, `total`) for Tasks that were accepted.
    :ivar wait_duration_until_canceled: The wait duration statistics (`avg`, `min`, `max`, `total`) for Tasks that were canceled.
    :ivar tasks_canceled: The total number of Tasks that were canceled.
    :ivar tasks_completed: The total number of Tasks that were completed.
    :ivar tasks_created: The total number of Tasks created.
    :ivar tasks_deleted: The total number of Tasks that were deleted.
    :ivar tasks_moved: The total number of Tasks that were moved from one queue to another.
    :ivar tasks_timed_out_in_workflow: The total number of Tasks that were timed out of their Workflows (and deleted).
    :ivar workspace_sid: The SID of the Workspace.
    :ivar url: The absolute URL of the Workspace statistics resource.
    """

    def __init__(self, version: Version, payload: Dict[str, Any], workspace_sid: str):
        super().__init__(version)

        self.account_sid: Optional[str] = payload.get("account_sid")
        self.avg_task_acceptance_time: Optional[int] = deserialize.integer(
            payload.get("avg_task_acceptance_time")
        )
        self.start_time: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("start_time")
        )
        self.end_time: Optional[datetime] = deserialize.iso8601_datetime(
            payload.get("end_time")
        )
        self.reservations_created: Optional[int] = deserialize.integer(
            payload.get("reservations_created")
        )
        self.reservations_accepted: Optional[int] = deserialize.integer(
            payload.get("reservations_accepted")
        )
        self.reservations_rejected: Optional[int] = deserialize.integer(
            payload.get("reservations_rejected")
        )
        self.reservations_timed_out: Optional[int] = deserialize.integer(
            payload.get("reservations_timed_out")
        )
        self.reservations_canceled: Optional[int] = deserialize.integer(
            payload.get("reservations_canceled")
        )
        self.reservations_rescinded: Optional[int] = deserialize.integer(
            payload.get("reservations_rescinded")
        )
        self.split_by_wait_time: Optional[Dict[str, object]] = payload.get(
            "split_by_wait_time"
        )
        self.wait_duration_until_accepted: Optional[Dict[str, object]] = payload.get(
            "wait_duration_until_accepted"
        )
        self.wait_duration_until_canceled: Optional[Dict[str, object]] = payload.get(
            "wait_duration_until_canceled"
        )
        self.tasks_canceled: Optional[int] = deserialize.integer(
            payload.get("tasks_canceled")
        )
        self.tasks_completed: Optional[int] = deserialize.integer(
            payload.get("tasks_completed")
        )
        self.tasks_created: Optional[int] = deserialize.integer(
            payload.get("tasks_created")
        )
        self.tasks_deleted: Optional[int] = deserialize.integer(
            payload.get("tasks_deleted")
        )
        self.tasks_moved: Optional[int] = deserialize.integer(
            payload.get("tasks_moved")
        )
        self.tasks_timed_out_in_workflow: Optional[int] = deserialize.integer(
            payload.get("tasks_timed_out_in_workflow")
        )
        self.workspace_sid: Optional[str] = payload.get("workspace_sid")
        self.url: Optional[str] = payload.get("url")

        self._solution = {
            "workspace_sid": workspace_sid,
        }
        self._context: Optional[WorkspaceCumulativeStatisticsContext] = None

    @property
    def _proxy(self) -> "WorkspaceCumulativeStatisticsContext":
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions. All instance actions are proxied to the context

        :returns: WorkspaceCumulativeStatisticsContext for this WorkspaceCumulativeStatisticsInstance
        """
        if self._context is None:
            self._context = WorkspaceCumulativeStatisticsContext(
                self._version,
                workspace_sid=self._solution["workspace_sid"],
            )
        return self._context

    def fetch(
        self,
        end_date: Union[datetime, object] = values.unset,
        minutes: Union[int, object] = values.unset,
        start_date: Union[datetime, object] = values.unset,
        task_channel: Union[str, object] = values.unset,
        split_by_wait_time: Union[str, object] = values.unset,
    ) -> "WorkspaceCumulativeStatisticsInstance":
        """
        Fetch the WorkspaceCumulativeStatisticsInstance

        :param end_date: Only include usage that occurred on or before this date, specified in GMT as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date-time.
        :param minutes: Only calculate statistics since this many minutes in the past. The default 15 minutes. This is helpful for displaying statistics for the last 15 minutes, 240 minutes (4 hours), and 480 minutes (8 hours) to see trends.
        :param start_date: Only calculate statistics from this date and time and later, specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        :param task_channel: Only calculate cumulative statistics on this TaskChannel. Can be the TaskChannel's SID or its `unique_name`, such as `voice`, `sms`, or `default`.
        :param split_by_wait_time: A comma separated list of values that describes the thresholds, in seconds, to calculate statistics on. For each threshold specified, the number of Tasks canceled and reservations accepted above and below the specified thresholds in seconds are computed. For example, `5,30` would show splits of Tasks that were canceled or accepted before and after 5 seconds and before and after 30 seconds. This can be used to show short abandoned Tasks or Tasks that failed to meet an SLA. TaskRouter will calculate statistics on up to 10,000 Tasks for any given threshold.

        :returns: The fetched WorkspaceCumulativeStatisticsInstance
        """
        return self._proxy.fetch(
            end_date=end_date,
            minutes=minutes,
            start_date=start_date,
            task_channel=task_channel,
            split_by_wait_time=split_by_wait_time,
        )

    async def fetch_async(
        self,
        end_date: Union[datetime, object] = values.unset,
        minutes: Union[int, object] = values.unset,
        start_date: Union[datetime, object] = values.unset,
        task_channel: Union[str, object] = values.unset,
        split_by_wait_time: Union[str, object] = values.unset,
    ) -> "WorkspaceCumulativeStatisticsInstance":
        """
        Asynchronous coroutine to fetch the WorkspaceCumulativeStatisticsInstance

        :param end_date: Only include usage that occurred on or before this date, specified in GMT as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date-time.
        :param minutes: Only calculate statistics since this many minutes in the past. The default 15 minutes. This is helpful for displaying statistics for the last 15 minutes, 240 minutes (4 hours), and 480 minutes (8 hours) to see trends.
        :param start_date: Only calculate statistics from this date and time and later, specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        :param task_channel: Only calculate cumulative statistics on this TaskChannel. Can be the TaskChannel's SID or its `unique_name`, such as `voice`, `sms`, or `default`.
        :param split_by_wait_time: A comma separated list of values that describes the thresholds, in seconds, to calculate statistics on. For each threshold specified, the number of Tasks canceled and reservations accepted above and below the specified thresholds in seconds are computed. For example, `5,30` would show splits of Tasks that were canceled or accepted before and after 5 seconds and before and after 30 seconds. This can be used to show short abandoned Tasks or Tasks that failed to meet an SLA. TaskRouter will calculate statistics on up to 10,000 Tasks for any given threshold.

        :returns: The fetched WorkspaceCumulativeStatisticsInstance
        """
        return await self._proxy.fetch_async(
            end_date=end_date,
            minutes=minutes,
            start_date=start_date,
            task_channel=task_channel,
            split_by_wait_time=split_by_wait_time,
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Taskrouter.V1.WorkspaceCumulativeStatisticsInstance {}>".format(
            context
        )


class WorkspaceCumulativeStatisticsContext(InstanceContext):
    def __init__(self, version: Version, workspace_sid: str):
        """
        Initialize the WorkspaceCumulativeStatisticsContext

        :param version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace to fetch.
        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "workspace_sid": workspace_sid,
        }
        self._uri = "/Workspaces/{workspace_sid}/CumulativeStatistics".format(
            **self._solution
        )

    def fetch(
        self,
        end_date: Union[datetime, object] = values.unset,
        minutes: Union[int, object] = values.unset,
        start_date: Union[datetime, object] = values.unset,
        task_channel: Union[str, object] = values.unset,
        split_by_wait_time: Union[str, object] = values.unset,
    ) -> WorkspaceCumulativeStatisticsInstance:
        """
        Fetch the WorkspaceCumulativeStatisticsInstance

        :param end_date: Only include usage that occurred on or before this date, specified in GMT as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date-time.
        :param minutes: Only calculate statistics since this many minutes in the past. The default 15 minutes. This is helpful for displaying statistics for the last 15 minutes, 240 minutes (4 hours), and 480 minutes (8 hours) to see trends.
        :param start_date: Only calculate statistics from this date and time and later, specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        :param task_channel: Only calculate cumulative statistics on this TaskChannel. Can be the TaskChannel's SID or its `unique_name`, such as `voice`, `sms`, or `default`.
        :param split_by_wait_time: A comma separated list of values that describes the thresholds, in seconds, to calculate statistics on. For each threshold specified, the number of Tasks canceled and reservations accepted above and below the specified thresholds in seconds are computed. For example, `5,30` would show splits of Tasks that were canceled or accepted before and after 5 seconds and before and after 30 seconds. This can be used to show short abandoned Tasks or Tasks that failed to meet an SLA. TaskRouter will calculate statistics on up to 10,000 Tasks for any given threshold.

        :returns: The fetched WorkspaceCumulativeStatisticsInstance
        """

        data = values.of(
            {
                "EndDate": serialize.iso8601_datetime(end_date),
                "Minutes": minutes,
                "StartDate": serialize.iso8601_datetime(start_date),
                "TaskChannel": task_channel,
                "SplitByWaitTime": split_by_wait_time,
            }
        )

        payload = self._version.fetch(method="GET", uri=self._uri, params=data)

        return WorkspaceCumulativeStatisticsInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
        )

    async def fetch_async(
        self,
        end_date: Union[datetime, object] = values.unset,
        minutes: Union[int, object] = values.unset,
        start_date: Union[datetime, object] = values.unset,
        task_channel: Union[str, object] = values.unset,
        split_by_wait_time: Union[str, object] = values.unset,
    ) -> WorkspaceCumulativeStatisticsInstance:
        """
        Asynchronous coroutine to fetch the WorkspaceCumulativeStatisticsInstance

        :param end_date: Only include usage that occurred on or before this date, specified in GMT as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date-time.
        :param minutes: Only calculate statistics since this many minutes in the past. The default 15 minutes. This is helpful for displaying statistics for the last 15 minutes, 240 minutes (4 hours), and 480 minutes (8 hours) to see trends.
        :param start_date: Only calculate statistics from this date and time and later, specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        :param task_channel: Only calculate cumulative statistics on this TaskChannel. Can be the TaskChannel's SID or its `unique_name`, such as `voice`, `sms`, or `default`.
        :param split_by_wait_time: A comma separated list of values that describes the thresholds, in seconds, to calculate statistics on. For each threshold specified, the number of Tasks canceled and reservations accepted above and below the specified thresholds in seconds are computed. For example, `5,30` would show splits of Tasks that were canceled or accepted before and after 5 seconds and before and after 30 seconds. This can be used to show short abandoned Tasks or Tasks that failed to meet an SLA. TaskRouter will calculate statistics on up to 10,000 Tasks for any given threshold.

        :returns: The fetched WorkspaceCumulativeStatisticsInstance
        """

        data = values.of(
            {
                "EndDate": serialize.iso8601_datetime(end_date),
                "Minutes": minutes,
                "StartDate": serialize.iso8601_datetime(start_date),
                "TaskChannel": task_channel,
                "SplitByWaitTime": split_by_wait_time,
            }
        )

        payload = await self._version.fetch_async(
            method="GET", uri=self._uri, params=data
        )

        return WorkspaceCumulativeStatisticsInstance(
            self._version,
            payload,
            workspace_sid=self._solution["workspace_sid"],
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        context = " ".join("{}={}".format(k, v) for k, v in self._solution.items())
        return "<Twilio.Taskrouter.V1.WorkspaceCumulativeStatisticsContext {}>".format(
            context
        )


class WorkspaceCumulativeStatisticsList(ListResource):
    def __init__(self, version: Version, workspace_sid: str):
        """
        Initialize the WorkspaceCumulativeStatisticsList

        :param version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace to fetch.

        """
        super().__init__(version)

        # Path Solution
        self._solution = {
            "workspace_sid": workspace_sid,
        }

    def get(self) -> WorkspaceCumulativeStatisticsContext:
        """
        Constructs a WorkspaceCumulativeStatisticsContext

        """
        return WorkspaceCumulativeStatisticsContext(
            self._version, workspace_sid=self._solution["workspace_sid"]
        )

    def __call__(self) -> WorkspaceCumulativeStatisticsContext:
        """
        Constructs a WorkspaceCumulativeStatisticsContext

        """
        return WorkspaceCumulativeStatisticsContext(
            self._version, workspace_sid=self._solution["workspace_sid"]
        )

    def __repr__(self) -> str:
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        """
        return "<Twilio.Taskrouter.V1.WorkspaceCumulativeStatisticsList>"
