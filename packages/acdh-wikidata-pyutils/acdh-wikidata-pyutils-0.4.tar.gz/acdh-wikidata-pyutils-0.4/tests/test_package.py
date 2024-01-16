import unittest

from acdh_wikidata_pyutils import NoWikiDataUrlException, WikiDataPerson, WikiDataPlace

ARTHUR_SCHNITZLER_URL = "https://www.wikidata.org/wiki/Q44331"
ARTHUR_SCHNITZLER_ID = "Q44331"
POOR_DATA_URL = "https://www.wikidata.org/wiki/Q122733648"
LINZ_URL = "https://www.wikidata.org/wiki/Q41329"
BROKEN = "https://www.wikidata.org/wiki/Q2390830"

ARTHUR_SCHNITZLER = WikiDataPerson(ARTHUR_SCHNITZLER_URL)
POOR_DATA_ITEM = WikiDataPerson(POOR_DATA_URL)
LINZ = WikiDataPlace(LINZ_URL)


class TestTestTest(unittest.TestCase):
    """Tests for `acdh-wikidata-pyutils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_testsetup(self):
        self.assertTrue(True)

    def test_002_valid_url(self):
        item = ARTHUR_SCHNITZLER
        self.assertEqual(item.wikidata_id, ARTHUR_SCHNITZLER_ID)

    def test_003_non_valid_url(self):
        with self.assertRaises(NoWikiDataUrlException):
            WikiDataPerson(ARTHUR_SCHNITZLER_URL.replace("wikidata", "hansi"))

    def test_004_label(self):
        item = ARTHUR_SCHNITZLER
        self.assertEqual(item.label, "Arthur Schnitzler")

    def test_005_poor_data(self):
        item = POOR_DATA_ITEM
        apis_person = item.get_apis_entity()
        self.assertTrue(apis_person["first_name"])

    def test_006_no_name(self):
        item = POOR_DATA_ITEM
        apis_person = item.get_apis_entity()
        self.assertEqual(apis_person["name"], "Andorfer")

    def test_007_coords(self):
        item = LINZ
        self.assertTrue("lat" in item.get_apis_entity().keys())

    def test_008_no_coords(self):
        item = WikiDataPlace("https://www.wikidata.org/wiki/Q16006181")
        self.assertFalse(item.lat)
        self.assertFalse(item.gnd_uri)
        self.assertFalse(item.geonames_uri)

    def test_008_no_ngd(self):
        item = WikiDataPerson("https://www.wikidata.org/wiki/Q16006181")
        self.assertFalse(item.gnd_uri)

    def test_009_broken_date(self):
        item = WikiDataPerson(BROKEN)
        self.assertFalse(item.date_of_birth)
