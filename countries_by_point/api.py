import json
import azure.functions as func

from common.countries import CountryDatabase
from common.parse_input import parse_point, ParseException

from shapely.geometry import Point


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        longitude, latitude = parse_point(req)
        db = CountryDatabase.load()
        result = ({
            "name": country["name"],
            "continent": country["continent"]
        } for country in db.query_by_point(longitude, latitude) if country["shape"].contains(Point(longitude, latitude)))
        return func.HttpResponse(json.dumps(list(result)))
    except ParseException as e:
        return func.HttpResponse(e.message, status_code=400)