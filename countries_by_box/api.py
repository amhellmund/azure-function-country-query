import logging
import json
import azure.functions as func

from common.countries import CountryDatabase
from common.parse_input import parse_box, ParseException

from shapely.geometry import box as Box


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        bounding_box = parse_box(req)
        db = CountryDatabase.load()
        result = ({
            "name": country["name"],
            "continent": country["continent"]
        } for country in db.query_by_box(bounding_box) if country["shape"].intersects(Box(*bounding_box)))
        return func.HttpResponse(json.dumps(list(result)))
    except ParseException as e:
        return func.HttpResponse(e.message, status_code=400)