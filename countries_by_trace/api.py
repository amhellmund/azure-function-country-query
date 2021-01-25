import logging
import json
import azure.functions as func

from common.countries import CountryDatabase
from common.parse_input import parse_trace, ParseException

from shapely.geometry import box as Box


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        trace = parse_trace(req)
        db = CountryDatabase.load()
        result = ({
            "name": country["name"],
            "continent": country["continent"]
        } for country in db.query_by_box(trace.bounds) if country["shape"].intersects(Box(*trace.bounds)))
        return func.HttpResponse(json.dumps(list(result)))
    except ParseException as e:
        return func.HttpResponse(e.message, status_code=400)