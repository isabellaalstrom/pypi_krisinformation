"""
    Automatic tests for the krisinformation_lib
"""
# pylint: disable=C0302,W0621,R0903, W0212

from typing import List

import aiohttp
import pytest
from krisinformation.krisinformation_lib import (
    Krisinformation,
    KrisinformationNews,
    KrisinformationAPIBase,
    KrisinformationAPI,
    KrisinformationException,
)
from krisinformation import krisinformation_lib

import logging


@pytest.fixture
def krisinformation() -> Krisinformation:
    """Returns the krisinformation object."""
    return Krisinformation("17.041", "62.34198", api=FakeKrisinformationApi())


@pytest.fixture
def krisinformation_real() -> Krisinformation:
    """Returns the krisinformation object."""
    return Krisinformation("17.03078", "62.3398599")


@pytest.fixture
def krisinformation_news(krisinformation) -> List[KrisinformationNews]:
    """Returns the krisinformation object."""
    return krisinformation.get_news()


@pytest.fixture
def first_krisinformation_news(krisinformation) -> KrisinformationNews:
    """Returns the krisinformation object."""
    return krisinformation.get_news()


@pytest.fixture
def first_krisinformation_news2(krisinformation) -> KrisinformationNews:
    """Returns the krisinformation object."""
    return krisinformation.get_news()


@pytest.mark.asyncio
async def test_provide_session_constructor() -> None:
    """Test the constructor that provides session."""
    session = aiohttp.ClientSession()
    api = Krisinformation(
        "1.1234567", "1.9876543", session=session, api=FakeKrisinformationApi()
    )

    await session.close()
    assert api._api.session


def test_use_abstract_base_class():
    """test the not implemented stuff"""
    with pytest.raises(NotImplementedError):
        test = KrisinformationAPIBase()
        test.get_news_api("17.00", "62.1")


def test_krisinformation_integration_test():
    """Only test that uses the actual service. Make sure service is up if fails"""
    api = KrisinformationAPI()
    news = api.get_news_api("17.00", "62.1")
    assert news is not None


@pytest.mark.asyncio
async def test_krisinformation_async_integration_test():
    """Only test that uses the actual service. Make sure service is up if fails"""
    api = KrisinformationAPI()
    news = await api.async_get_news_api("17.00", "62.1")
    assert news is not None


@pytest.mark.asyncio
async def test_krisinformation_async_integration_test_use_session():
    """Only test that uses the actual service. Make sure service is up if fails"""
    api = KrisinformationAPI()
    api.session = aiohttp.ClientSession()
    news = await api.async_get_news_api("17.041326", "62.339859")
    assert news is not None
    await api.session.close()


@pytest.mark.asyncio
async def test_krisinformation_async_get_news_integration(krisinformation):
    """test the async stuff"""
    news = await krisinformation.async_get_news()
    assert news[0] is not None
    assert news is not None


@pytest.mark.asyncio
async def test_krisinformation_async_get_news_integration2(krisinformation_real) -> {}:
    """test the async stuff"""
    news = await krisinformation_real.async_get_news()
    print(news)
    assert news[0] is not None
    assert news is not None
    print(news[0].identifier)


@pytest.mark.asyncio
async def test_krisinformation_async_get_news_integration_use_session(krisinformation):
    """test the async stuff"""
    krisinformation.session = aiohttp.ClientSession()
    news = await krisinformation.async_get_news()

    assert news[0] is not None
    assert news is not None

    await krisinformation.session.close()


@pytest.mark.asyncio
async def test_async_use_abstract_base_class():
    """test the not implemented stuff"""
    with pytest.raises(NotImplementedError):
        test = KrisinformationAPIBase()
        await test.async_get_news_api("17.00", "62.1")


@pytest.mark.asyncio
async def test_async_error_from_api():
    """test the async stuff"""
    api = KrisinformationAPI()
    # Faulty template
    krisinformation_lib.APIURL = "http://api.krisinformation.se/v3/new"

    krisinformation_error = Krisinformation("17.00", "62.1", api=api)
    with pytest.raises(KrisinformationException):
        await krisinformation_error.async_get_news()


class FakeKrisinformationApi(KrisinformationAPIBase):
    """Implements fake class to return API data"""

    async def async_get_news_api(self, longitude: str, latitude: str):
        """Real data from the version code works from"""
        return self.get_news_api(longitude, latitude)

    def get_news_api(self, longitude: str, latitude: str):
        """Real data from the version code works from"""
        return [
            {
                "Identifier": "18478",
                "PushMessage": "🔶 SMHI har utfärdat en orange varning för vind och snöfall i norra Götaland, östra Svealand samt i norra Skåne. Ovädret kan bland annat&nbsp; leda till trafikstörningar och elavbrott.",
                "Updated": "2023-03-07T12:55:43+01:00",
                "Published": "2023-03-06T12:04:12+01:00",
                "Headline": "Orange varning för vind och snöfall",
                "Preamble": "🔶 SMHI har utfärdat en orange varning för vind och snöfall i norra Götaland, östra Svealand samt i norra Skåne. Ovädret kan bland annat&nbsp; leda till trafikstörningar och elavbrott.",
                "BodyText": "<p>Under tisdagen och onsdagen väntas kraftigt snöfall i kombination med blåsigt väder. Det kan komma&nbsp;10-20 cm snö i norra Skåne och 15-25 cm snö i nordöstra och nordvästra Götaland samt östra Svealand.</p>\n<ul>\n<li>Varningen för nordöstra Götaland och östra Svealand gäller från den 7 mars kl. 06.00 till den 8 mars kl. 12.00.&nbsp;</li>\n<li>Varningen för nordvästra Götaland&nbsp;gäller från den 7 mars kl. 06.00 till kl. 23.00.&nbsp;</li>\n<li>Varningen för norra Skåne gäller från den 7 mars kl. 09.00&nbsp; till kl. 23.00.</li>\n</ul>\n<h2>Hur kan det påverka mig?</h2>\n<ul>\n<li>Mycket begränsad framkomlighet på vägar, särskilt i öppna landskap, som till exempel inte hunnit snöröjas eller på grund av trafikolyckor.</li>\n<li>Förseningar inom buss-, tåg- och flygtrafiken samt inställda avgångar.</li>\n<li>Sannolikt elbortfall i områden med luftburna elledningar, vilket även påverkar mobila nät för telekommunikationer.</li>\n</ul>",
                "ImageLink": "",
                "Links": [
                    {
                        "Text": "Följ varningsläget hos SMHI",
                        "Url": "https://www.smhi.se/vader/varningar-och-brandrisk/varningar-och-meddelanden/varningar#ws=wpt-a,proxy=wpt-a,district=none,page=wpt-warning-alla",
                    },
                    {
                        "Text": "Följ trafikläget hos Trafikverket",
                        "Url": "https://www.trafikverket.se/resa-och-trafik/trafikinformation/",
                    },
                ],
                "Area": [
                    {
                        "Type": "Country",
                        "Description": "Sverige",
                        "Coordinate": "16.596265846848,62.8114849680804 0",
                        "CoordinateObject": {
                            "Latitude": "62.8114849680804",
                            "Longitude": "16.596265846848",
                            "Altitude": "0",
                        },
                        "GeometryInformation": None,
                    }
                ],
                "Web": "https://www.krisinformation.se/nyheter/2023/mars/orange-varning-for-vind-och-snofall/",
                "Language": "sv",
                "Event": "News",
                "SenderName": "SMHI",
                "Push": True,
                "BodyLinks": [],
                "SourceID": 0,
            },
            {
                "Identifier": "18435",
                "PushMessage": "🔶 SMHI har utfärdat en orange varning för vind och snöfall i delar av Härjedals- och Jämtlandsfjällen. Personer avråds starkt från att ge sig ut på fjället. Varningen gäller från fredag morgon till fredag kväll.",
                "Updated": "2023-03-02T13:36:17+01:00",
                "Published": "2023-03-02T13:36:00+01:00",
                "Headline": "Orange vind- och snövarning i Härjedals- och Jämtlandsfjällen",
                "Preamble": "🔶 SMHI har utfärdat en orange varning för vind och snöfall i delar av Härjedals- och Jämtlandsfjällen. Personer avråds starkt från att ge sig ut på fjället. Varningen gäller från fredag morgon till fredag kväll.",
                "BodyText": "<p>Under fredag morgon väntas ökande vind som på kalfjället kan bli mycket hård och under eftermiddagen nå18-23 meter per sekund. Samtidigt väntas snöfall eller täta snöbyar. Vinden avtar under fredag kväll samtidigt som intensiteten på snöbyarna minskar något. Varningen gäller 3 mars kl. 05.00&nbsp;– 20.00.&nbsp;</p>\n<h2>Hur kan det påverka mig?</h2>\n<ul>\n<li>Personer avråds starkt från att ge sig ut på fjället.</li>\n<li>Räddningsinsatser i fjällmiljö kan bli riskabla och ta lång tid.</li>\n<li>Mycket svårt att förflytta sig samt att resa och förankra tält.</li>\n<li>Mycket svårt att orientera sig på grund av kraftigt nedsatt sikt.</li>\n<li>Stor risk för förfrysning.</li>\n</ul>",
                "ImageLink": "",
                "Links": [
                    {
                        "Text": "SMHI:s vädervarningar",
                        "Url": "https://www.smhi.se/vader/varningar-och-brandrisk/varningar-och-meddelanden/varningar",
                    }
                ],
                "Area": [
                    {
                        "Type": "Country",
                        "Description": "Sverige",
                        "Coordinate": "16.596265846848,62.8114849680804 0",
                        "CoordinateObject": {
                            "Latitude": "62.8114849680804",
                            "Longitude": "16.596265846848",
                            "Altitude": "0",
                        },
                        "GeometryInformation": None,
                    },
                    {
                        "Type": "County",
                        "Description": "Jämtlands län",
                        "Coordinate": "14.3120756370727,63.2577271060803 0",
                        "CoordinateObject": {
                            "Latitude": "63.2577271060803",
                            "Longitude": "14.3120756370727",
                            "Altitude": "0",
                        },
                        "GeometryInformation": None,
                    },
                ],
                "Web": "https://www.krisinformation.se/nyheter/2023/mars/orange-vind--och-snovarning-i-harjedals--och-jamtlandsfjallen/",
                "Language": "sv",
                "Event": "News",
                "SenderName": "SMHI",
                "Push": True,
                "BodyLinks": [],
                "SourceID": 0,
            },
            {
                "Identifier": "18434",
                "PushMessage": "Uppdatering 2/3 kl. 09.30: Faran är över. Meddelandet gäller inte längre.\n\n",
                "Updated": "2023-03-02T06:15:17+01:00",
                "Published": "2023-03-02T06:15:00+01:00",
                "Headline": "Viktigt meddelande till allmänheten i Åhus, Skåne län. ",
                "Preamble": "Uppdatering 2/3 kl. 09.30: Faran är över. Meddelandet gäller inte längre.\n\n",
                "BodyText": "<p>Ursprungligt meddelande: ⚠ Viktigt meddelande till allmänheten i Åhus i Kristianstads kommun. Det brinner i en byggnad med giftig rökutveckling till följd. Räddningsledaren uppmanar alla i området omkring Äspet att gå inomhus och stänga dörrar, fönster och, om möjligt, ventilation.</p>\n<p>{0}.</p>",
                "ImageLink": "",
                "Links": [
                    {
                        "Text": "Polisen om händelsen",
                        "Url": "https://polisen.se/aktuellt/handelser/2023/mars/2/02-mars-0544-brand-kristianstad/",
                    }
                ],
                "Area": [
                    {
                        "Type": "Country",
                        "Description": "Sverige",
                        "Coordinate": "16.596265846848,62.8114849680804 0",
                        "CoordinateObject": {
                            "Latitude": "62.8114849680804",
                            "Longitude": "16.596265846848",
                            "Altitude": "0",
                        },
                        "GeometryInformation": None,
                    },
                    {
                        "Type": "County",
                        "Description": "Skåne län",
                        "Coordinate": "13.5339954630322,55.8614466949293 0",
                        "CoordinateObject": {
                            "Latitude": "55.8614466949293",
                            "Longitude": "13.5339954630322",
                            "Altitude": "0",
                        },
                        "GeometryInformation": None,
                    },
                    {
                        "Type": "PoI",
                        "Description": "Åhus",
                        "Coordinate": "14.30884,55.92231",
                        "CoordinateObject": {
                            "Latitude": "55.92231",
                            "Longitude": "14.30884",
                            "Altitude": None,
                        },
                        "GeometryInformation": None,
                    },
                ],
                "Web": "https://www.krisinformation.se/nyheter/2023/mars/vma-ahus/",
                "Language": "sv",
                "Event": "News",
                "SenderName": "",
                "Push": True,
                "BodyLinks": [
                    {
                        "Text": "För mer information lyssna på Sveriges Radio P4 Kristianstad",
                        "Url": "https://sverigesradio.se/kristianstad",
                    }
                ],
                "SourceID": 0,
            },
        ]
