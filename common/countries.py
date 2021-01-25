import json
import os
import rtree

from shapely import geometry

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
SHAPES_FILE = "shapes.json"
METADATA_FILE = "metadata.json"


cached_country_database = None


class CountryDatabase:
    @staticmethod
    def load(root_dir = DEFAULT_DATA_DIR):
        global cached_country_database
        if not cached_country_database:
            countries = _load_countries(root_dir)
            index = _create_index(countries)
            cached_country_database = CountryDatabase(countries, index)
        return cached_country_database
    
    def __init__(self, countries, index):
        self.countries = countries
        self.index = index

    def query_by_point(self, longitude, latitude):
        return self.query_by_box((longitude, latitude, longitude, latitude))

    def query_by_box(self, box):
        indices = self.index.intersection(box)
        return (self.countries[i] for i in indices)


def _load_countries(data_root):
    shapes = _load_json(os.path.join(data_root, SHAPES_FILE))
    metadata = _load_json(os.path.join(data_root, METADATA_FILE))

    return [{
        "name": country["properties"]["name"],
        "continent": _get_continent(country, metadata),
        "shape": geometry.shape(country["geometry"])
    } for country in shapes["features"]]


def _load_json(filepath):
    with open(os.path.join(filepath), "r") as file_stream:
        return json.load(file_stream)


def _get_continent(country, metadata):
    country_code = country["id"]
    for meta in metadata:
        if meta["alpha-3"] == country_code:
            return meta["region"]
    return None


def _create_index(countries):
    index = rtree.index.Index(interleaved=True)
    for id, country in enumerate(countries):
        index.insert(id, country["shape"].bounds)
    return index