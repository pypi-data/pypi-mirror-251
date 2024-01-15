r"""
    This code was generated by
   ___ _ _ _ _ _    _ ____    ____ ____ _    ____ ____ _  _ ____ ____ ____ ___ __   __
    |  | | | | |    | |  | __ |  | |__| | __ | __ |___ |\ | |___ |__/ |__|  | |  | |__/
    |  |_|_| | |___ | |__|    |__| |  | |    |__] |___ | \| |___ |  \ |  |  | |__| |  \

    Twilio - Media
    This is the public Twilio REST API.

    NOTE: This class is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
    Do not edit the class manually.
"""

from typing import Optional
from twilio.base.version import Version
from twilio.base.domain import Domain
from twilio.rest.media.v1.media_processor import MediaProcessorList
from twilio.rest.media.v1.media_recording import MediaRecordingList
from twilio.rest.media.v1.player_streamer import PlayerStreamerList


class V1(Version):
    def __init__(self, domain: Domain):
        """
        Initialize the V1 version of Media

        :param domain: The Twilio.media domain
        """
        super().__init__(domain, "v1")
        self._media_processor: Optional[MediaProcessorList] = None
        self._media_recording: Optional[MediaRecordingList] = None
        self._player_streamer: Optional[PlayerStreamerList] = None

    @property
    def media_processor(self) -> MediaProcessorList:
        if self._media_processor is None:
            self._media_processor = MediaProcessorList(self)
        return self._media_processor

    @property
    def media_recording(self) -> MediaRecordingList:
        if self._media_recording is None:
            self._media_recording = MediaRecordingList(self)
        return self._media_recording

    @property
    def player_streamer(self) -> PlayerStreamerList:
        if self._player_streamer is None:
            self._player_streamer = PlayerStreamerList(self)
        return self._player_streamer

    def __repr__(self) -> str:
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        """
        return "<Twilio.Media.V1>"
