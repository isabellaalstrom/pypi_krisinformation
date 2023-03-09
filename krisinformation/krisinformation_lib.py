"""
Module krisinformation_lib contains the code to get news from
Krisinformation through the open API:s
"""
import abc
from datetime import datetime
import copy
import json
from collections import OrderedDict
from urllib.request import urlopen
from typing import List
import aiohttp


APIURL = "http://api.krisinformation.se/v3/news"


class KrisinformationException(Exception):
    """Exception thrown if failing to access API"""

    pass


class KrisinformationNews:
    """
    Class to hold news data
    """

    def __init__(
        self,
        identifier: str,
        push_message: str,
        updated: datetime,
        published: datetime,
        headline: str,
        preamble: str,
        body_text: str,
        image_link: str,
        links,
        area,
        web: str,
        language: str,
        event: str,
        sender_name: str,
        push: bool,
        body_links,
        source_id: int,
    ) -> None:
        """Constructor"""
        self._identifier = identifier
        self._push_message = push_message
        self._updated = updated
        self._published = published
        self._headline = headline
        self._preamble = preamble
        self._body_text = body_text
        self._image_link = image_link
        self._links = links
        self._area = area
        self._web = web
        self._language = language
        self._event = event
        self._sender_name = sender_name
        self._push = push
        self._body_links = body_links
        self._source_id = source_id

    @property
    def identifier(self) -> str:
        """Identifing ID"""
        return self._identifier

    @property
    def push_message(self) -> str:
        """Identifing ID"""
        return self._push_message

    @property
    def updated(self) -> datetime:
        """Identifing ID"""
        return self._updated

    @property
    def published(self) -> datetime:
        """Identifing ID"""
        return self._published

    @property
    def headline(self) -> str:
        """Identifing ID"""
        return self._headline

    @property
    def preamble(self) -> str:
        """Air temperature (Celcius)"""
        return self._preamble

    @property
    def body_text(self) -> str:
        """Air temperature max during the day (Celcius)"""
        return self._body_text

    @property
    def image_link(self) -> str:
        """Air temperature min during the day (Celcius)"""
        return self._image_link

    @property
    def links(self) -> str:
        """Air humidity (Percent)"""
        return self._links

    @property
    def area(self) -> str:
        """Air pressure (hPa)"""
        return self._area

    @property
    def web(self) -> str:
        """Chance of thunder (Percent)"""
        return self._web

    @property
    def language(self) -> str:
        """Cloudiness (Percent)"""
        return self._language

    @property
    def event(self) -> str:
        """wind speed (m/s)"""
        return self._event

    @property
    def sender_name(self) -> str:
        """wind direction (degrees)"""
        return self._sender_name

    @property
    def push(self) -> str:
        """wind direction (degrees)"""
        return self._push

    @property
    def body_links(self) -> str:
        """Mean Precipitation (mm/h)"""
        return self._body_links

    @property
    def source_id(self) -> int:
        """Mean Precipitation (mm/h)"""
        return self._source_id


# pylint: disable=R0903


class KrisinformationAPIBase:
    """
    Baseclass to use as dependecy incjection pattern for easier
    automatic testing
    """

    @abc.abstractmethod
    def get_news_api(self, longitude: str, latitude: str):
        """Override this"""
        raise NotImplementedError("users must define get_news to use this base class")

    @abc.abstractmethod
    async def async_get_news_api(self, longitude: str, latitude: str):
        """Override this"""
        raise NotImplementedError("users must define get_news to use this base class")


# pylint: disable=R0903


class KrisinformationAPI(KrisinformationAPIBase):
    """Default implementation for Krisinformation api"""

    def __init__(self) -> None:
        """Init the API with or without session"""
        self.session = None

    def get_news_api(self, longitude: str, latitude: str):
        """gets data from API"""
        api_url = APIURL

        response = urlopen(api_url)
        data = response.read().decode("utf-8")
        json_data = json.loads(data)

        return json_data

    async def async_get_news_api(self, longitude: str, latitude: str):
        """gets data from API asyncronious"""
        api_url = APIURL

        is_new_session = False
        if self.session is None:
            self.session = aiohttp.ClientSession()
            is_new_session = True

        async with self.session.get(api_url) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()
                raise KrisinformationException(
                    "Failed to access Krisinformation API with status code {}".format(
                        response.status
                    )
                )
            data = await response.text()
            if is_new_session:
                await self.session.close()

            return json.loads(data)


class Krisinformation:
    """
    Class that use the Krisinformation open API
    """

    def __init__(
        self,
        longitude: str,
        latitude: str,
        session: aiohttp.ClientSession = None,
        api: KrisinformationAPIBase = KrisinformationAPI(),
    ) -> None:
        self._longitude = str(round(float(longitude), 6))
        self._latitude = str(round(float(latitude), 6))
        self._api = api

        if session:
            self._api.session = session

    def get_news(self) -> List[KrisinformationNews]:
        """
        Returns a list of news.
        """
        json_data = self._api.get_news_api(self._longitude, self._latitude)
        return _get_news(json_data)

    async def async_get_news(self) -> List[KrisinformationNews]:
        """
        Returns a list of forecasts. The first in list are the current one
        """
        json_data = await self._api.async_get_news_api(self._longitude, self._latitude)
        return _get_news(json_data)


# pylint: disable=R0914, R0912, W0212, R0915
def _get_news(api_result: dict) -> List[KrisinformationNews]:
    """Converts results from API to KrisinformationNews list"""
    news = _get_all_news_from_api(api_result)
    return news


# pylint: disable=R0914, R0912, W0212, R0915


def _get_all_news_from_api(api_result: dict) -> List[KrisinformationNews]:
    """Converts results from API to KrisinformationNews list"""
    newsList = []
    # Get the parameters
    for news in api_result:
        identifier = str(news["Identifier"])
        push_message = str(news["PushMessage"])
        updated = news["Updated"]
        published = news["Published"]
        headline = str(news["Headline"])
        preamble = str(news["Preamble"])
        body_text = str(news["BodyText"])
        image_link = str(news["ImageLink"])
        links = str(news["Links"])
        area = str(news["Area"])
        web = str(news["Web"])
        language = str(news["Language"])
        event = str(news["Event"])
        sender_name = str(news["SenderName"])
        push = str(news["Push"])
        body_links = str(news["BodyLinks"])
        source_id = str(news["SourceID"])

        news = KrisinformationNews(
            identifier,
            push_message,
            updated,
            published,
            headline,
            preamble,
            body_text,
            image_link,
            links,
            area,
            web,
            language,
            event,
            sender_name,
            push,
            body_links,
            source_id,
        )
        newsList.append(news)
    return newsList
