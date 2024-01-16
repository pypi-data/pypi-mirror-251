from AcdhArcheAssets.uri_norm_rules import get_norm_id, get_normalized_uri
from wikidata.client import Client

WIKIDATA_URL = "https://www.wikidata.org/wiki/"
GEONAMES_URL = "https://sws.geonames.org/"
GND_URL = "https://d-nb.info/gnd/"


class NoWikiDataUrlException(Exception):
    pass


def check_url(wikidata_url):
    if "wikidata" not in wikidata_url:
        raise NoWikiDataUrlException(f"{wikidata_url} is no proper Wikidata URL")
    else:
        return get_normalized_uri(wikidata_url)


class WikiDataPlace:
    """Class to fetch and return often used data from WikiData Person entries"""

    def get_apis_entity(self):
        return {"name": self.label, "lat": self.lat, "lng": self.lng}

    def __init__(self, wikidata_url):
        self.wikidata_url = check_url(wikidata_url)
        self.wikidata_id = get_norm_id(self.wikidata_url)
        self.client = Client()
        self.entity = self.client.get(self.wikidata_id, load=True)
        self.label = str(self.entity.label)
        coordinates_prop = self.client.get("P625")
        gnd_uri_property = self.client.get("P227")
        geonames_uri_property = self.client.get("P1566")
        try:
            coordinates = self.entity[coordinates_prop]
        except KeyError:
            coordinates = False
        if coordinates:
            self.lat = coordinates.latitude
            self.lng = coordinates.longitude
        else:
            self.lat = None
            self.lng = None
        try:
            gnd_uri = self.entity[gnd_uri_property]
            self.gnd_uri = get_normalized_uri(f"{GND_URL}{gnd_uri}")
        except KeyError:
            self.gnd_uri = False
        try:
            geonames_uri = self.entity[geonames_uri_property]
            self.geonames_uri = get_normalized_uri(f"{GEONAMES_URL}{geonames_uri}")
        except KeyError:
            self.geonames_uri = False


class WikiDataPerson:
    """Class to fetch and return often used data from WikiData Person entries"""

    def get_apis_entity(self):
        return {
            "name": self.name,
            "first_name": self.first_name,
            "start_date_written": self.date_of_birth,
            "end_date_written": self.date_of_death,
            "gender": self.sex_or_gender,
        }

    def __init__(self, wikidata_url):
        self.wikidata_url = check_url(wikidata_url)
        self.wikidata_id = get_norm_id(self.wikidata_url)
        self.client = Client()
        self.entity = self.client.get(self.wikidata_id, load=True)
        self.label = str(self.entity.label)
        date_of_birth_prop = self.client.get("P569")
        date_of_death_prop = self.client.get("P570")
        place_of_birth_prop = self.client.get("P19")
        place_of_death_prop = self.client.get("P20")
        sex_or_gender_prop = self.client.get("P21")
        first_name_prop = self.client.get("P735")
        name_prop = self.client.get("P734")
        gnd_uri_property = self.client.get("P227")
        try:
            self.first_name = str(self.entity[first_name_prop].label)
        except KeyError:
            self.first_name = None
        try:
            self.name = str(self.entity[name_prop].label)
        except KeyError:
            self.name = self.label
        try:
            self.date_of_birth = str(self.entity[date_of_birth_prop])
        except (KeyError, ValueError):
            self.date_of_birth = None
        try:
            self.date_of_death = str(self.entity[date_of_death_prop])
        except (KeyError, ValueError):
            self.date_of_death = None
        try:
            self.sex_or_gender = str(self.entity[sex_or_gender_prop].label)
        except KeyError:
            self.sex_or_gender = None
        try:
            place_of_birth_id = str(self.entity[place_of_birth_prop].id)
            self.place_of_birth = get_normalized_uri(
                f"{WIKIDATA_URL}{place_of_birth_id}"
            )
        except KeyError:
            self.place_of_birth = None
        try:
            place_of_death_id = str(self.entity[place_of_death_prop].id)
            self.place_of_death = get_normalized_uri(
                f"{WIKIDATA_URL}{place_of_death_id}"
            )
        except KeyError:
            self.place_of_death = None
        try:
            gnd_uri = self.entity[gnd_uri_property]
            self.gnd_uri = get_normalized_uri(f"{GND_URL}{gnd_uri}")
        except KeyError:
            self.gnd_uri = False
