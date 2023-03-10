"""
    Automatic tests for the krisinformation_lib
"""
# pylint: disable=C0302,W0621,R0903, W0212

from typing import List

import logging
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
    return krisinformation.get_all_news()


@pytest.fixture
def first_krisinformation_news(krisinformation) -> KrisinformationNews:
    """Returns the krisinformation object."""
    return krisinformation.get_all_news()


@pytest.fixture
def first_krisinformation_news2(krisinformation) -> KrisinformationNews:
    """Returns the krisinformation object."""
    return krisinformation.get_all_news()


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
        test.get_all_news_api("17.00", "62.1")


def test_krisinformation_integration_test():
    """Only test that uses the actual service. Make sure service is up if fails"""
    api = KrisinformationAPI()
    news = api.get_all_news_api("17.00", "62.1")
    assert news is not None


@pytest.mark.asyncio
async def test_krisinformation_async_integration_test():
    """Only test that uses the actual service. Make sure service is up if fails"""
    api = KrisinformationAPI()
    news = await api.async_get_all_news_api("17.00", "62.1")
    assert news is not None


@pytest.mark.asyncio
async def test_krisinformation_async_integration_test_use_session():
    """Only test that uses the actual service. Make sure service is up if fails"""
    api = KrisinformationAPI()
    api.session = aiohttp.ClientSession()
    news = await api.async_get_all_news_api("17.041326", "62.339859")
    assert news is not None
    await api.session.close()


@pytest.mark.asyncio
async def test_krisinformation_async_get_all_news_integration(krisinformation):
    """test the async stuff"""
    news = await krisinformation.async_get_all_news()
    assert news[0] is not None
    assert news is not None


@pytest.mark.asyncio
async def test_krisinformation_async_get_all_news_integration2(
    krisinformation_real,
) -> {}:
    """test the async stuff"""
    news = await krisinformation_real.async_get_all_news()
    print(news)
    assert news[0] is not None
    assert news is not None
    print(news[0].identifier)


@pytest.mark.asyncio
async def test_krisinformation_async_get_all_news_integration_use_session(
    krisinformation,
):
    """test the async stuff"""
    krisinformation.session = aiohttp.ClientSession()
    news = await krisinformation.async_get_all_news()

    assert news[0] is not None
    assert news is not None

    await krisinformation.session.close()


@pytest.mark.asyncio
async def test_async_use_abstract_base_class():
    """test the not implemented stuff"""
    with pytest.raises(NotImplementedError):
        test = KrisinformationAPIBase()
        await test.async_get_all_news_api("17.00", "62.1")


@pytest.mark.asyncio
async def test_async_error_from_api():
    """test the async stuff"""
    api = KrisinformationAPI()
    # Faulty template
    krisinformation_lib.BASEURL = "http://api.krisinformation.se/v3/"
    krisinformation_lib.NEWS_ENDPOINT = "new"

    krisinformation_error = Krisinformation("17.00", "62.1", api=api)
    with pytest.raises(KrisinformationException):
        await krisinformation_error.async_get_all_news()


class FakeKrisinformationApi(KrisinformationAPIBase):
    """Implements fake class to return API data"""

    async def async_get_all_news_api(self, longitude: str, latitude: str):
        """Real data from the version code works from"""
        return self.get_all_news_api(longitude, latitude)

    def get_all_news_api(self, longitude: str, latitude: str):
        """Real data from the version code works from"""
        return [
            {
                "Identifier": "18478",
                "PushMessage": "???? SMHI har utf??rdat en orange varning f??r vind och sn??fall i norra G??taland, ??stra Svealand samt i norra Sk??ne. Ov??dret kan bland annat&nbsp; leda till trafikst??rningar och elavbrott.",
                "Updated": "2023-03-07T12:55:43+01:00",
                "Published": "2023-03-06T12:04:12+01:00",
                "Headline": "Orange varning f??r vind och sn??fall",
                "Preamble": "???? SMHI har utf??rdat en orange varning f??r vind och sn??fall i norra G??taland, ??stra Svealand samt i norra Sk??ne. Ov??dret kan bland annat&nbsp; leda till trafikst??rningar och elavbrott.",
                "BodyText": "<p>Under tisdagen och onsdagen v??ntas kraftigt sn??fall i kombination med bl??sigt v??der. Det kan komma&nbsp;10-20 cm sn?? i norra Sk??ne och 15-25 cm sn?? i nord??stra och nordv??stra G??taland samt ??stra Svealand.</p>\n<ul>\n<li>Varningen f??r nord??stra G??taland och ??stra Svealand g??ller fr??n den 7 mars kl. 06.00 till den 8 mars kl. 12.00.&nbsp;</li>\n<li>Varningen f??r nordv??stra G??taland&nbsp;g??ller fr??n den 7 mars kl. 06.00 till kl. 23.00.&nbsp;</li>\n<li>Varningen f??r norra Sk??ne g??ller fr??n den 7 mars kl. 09.00&nbsp; till kl. 23.00.</li>\n</ul>\n<h2>Hur kan det p??verka mig?</h2>\n<ul>\n<li>Mycket begr??nsad framkomlighet p?? v??gar, s??rskilt i ??ppna landskap, som till exempel inte hunnit sn??r??jas eller p?? grund av trafikolyckor.</li>\n<li>F??rseningar inom buss-, t??g- och flygtrafiken samt inst??llda avg??ngar.</li>\n<li>Sannolikt elbortfall i omr??den med luftburna elledningar, vilket ??ven p??verkar mobila n??t f??r telekommunikationer.</li>\n</ul>",
                "ImageLink": "",
                "Links": [
                    {
                        "Text": "F??lj varningsl??get hos SMHI",
                        "Url": "https://www.smhi.se/vader/varningar-och-brandrisk/varningar-och-meddelanden/varningar#ws=wpt-a,proxy=wpt-a,district=none,page=wpt-warning-alla",
                    },
                    {
                        "Text": "F??lj trafikl??get hos Trafikverket",
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
                "PushMessage": "???? SMHI har utf??rdat en orange varning f??r vind och sn??fall i delar av H??rjedals- och J??mtlandsfj??llen. Personer avr??ds starkt fr??n att ge sig ut p?? fj??llet. Varningen g??ller fr??n fredag morgon till fredag kv??ll.",
                "Updated": "2023-03-02T13:36:17+01:00",
                "Published": "2023-03-02T13:36:00+01:00",
                "Headline": "Orange vind- och sn??varning i H??rjedals- och J??mtlandsfj??llen",
                "Preamble": "???? SMHI har utf??rdat en orange varning f??r vind och sn??fall i delar av H??rjedals- och J??mtlandsfj??llen. Personer avr??ds starkt fr??n att ge sig ut p?? fj??llet. Varningen g??ller fr??n fredag morgon till fredag kv??ll.",
                "BodyText": "<p>Under fredag morgon v??ntas ??kande vind som p?? kalfj??llet kan bli mycket h??rd och under eftermiddagen n??18-23 meter per sekund. Samtidigt v??ntas sn??fall eller t??ta sn??byar. Vinden avtar under fredag kv??ll samtidigt som intensiteten p?? sn??byarna minskar n??got. Varningen g??ller 3 mars kl. 05.00&nbsp;??? 20.00.&nbsp;</p>\n<h2>Hur kan det p??verka mig?</h2>\n<ul>\n<li>Personer avr??ds starkt fr??n att ge sig ut p?? fj??llet.</li>\n<li>R??ddningsinsatser i fj??llmilj?? kan bli riskabla och ta l??ng tid.</li>\n<li>Mycket sv??rt att f??rflytta sig samt att resa och f??rankra t??lt.</li>\n<li>Mycket sv??rt att orientera sig p?? grund av kraftigt nedsatt sikt.</li>\n<li>Stor risk f??r f??rfrysning.</li>\n</ul>",
                "ImageLink": "",
                "Links": [
                    {
                        "Text": "SMHI:s v??dervarningar",
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
                        "Description": "J??mtlands l??n",
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
                "PushMessage": "Uppdatering 2/3 kl. 09.30: Faran ??r ??ver. Meddelandet g??ller inte l??ngre.\n\n",
                "Updated": "2023-03-02T06:15:17+01:00",
                "Published": "2023-03-02T06:15:00+01:00",
                "Headline": "Viktigt meddelande till allm??nheten i ??hus, Sk??ne l??n. ",
                "Preamble": "Uppdatering 2/3 kl. 09.30: Faran ??r ??ver. Meddelandet g??ller inte l??ngre.\n\n",
                "BodyText": "<p>Ursprungligt meddelande: ??? Viktigt meddelande till allm??nheten i ??hus i Kristianstads kommun. Det brinner i en byggnad med giftig r??kutveckling till f??ljd. R??ddningsledaren uppmanar alla i omr??det omkring ??spet att g?? inomhus och st??nga d??rrar, f??nster och, om m??jligt, ventilation.</p>\n<p>{0}.</p>",
                "ImageLink": "",
                "Links": [
                    {
                        "Text": "Polisen om h??ndelsen",
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
                        "Description": "Sk??ne l??n",
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
                        "Description": "??hus",
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
                        "Text": "F??r mer information lyssna p?? Sveriges Radio P4 Kristianstad",
                        "Url": "https://sverigesradio.se/kristianstad",
                    }
                ],
                "SourceID": 0,
            },
        ]
