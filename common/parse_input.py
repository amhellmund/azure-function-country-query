from shapely.geometry import LineString, Point


class ParseException(Exception):
    def __init__(self, message):
        self.message = message


def parse_point(req):
    body = _parse_json(req)
    if _is_valid_point_input(body):
        return body["point"]["longitude"], body["point"]["latitude"]
    raise ParseException("Invalid body specified for <Point> input data: {'point': {'longitude': <long>, 'latitude': <lat> } }")


def parse_box(req):
    body = _parse_json(req)
    if _is_valid_box_input(body):
        return body["box"]
    raise ParseException("Invalid body specified for <Box> input data: {'box': [<x-min>, <y-min>, <x-max>, <y-max>] }")


def parse_trace(req):
    body = _parse_json(req)
    if _is_valid_trace_input(body):
        return LineString([Point(p[0], p[1]) for p in body["trace"]])
    raise ParseException("Invalid body specified for <Trace> input data: {'trace': [ [<x-1>, <y-1>], ..., [<x-N>, <y-N>] ] }")
    

def _parse_json(req):
    try:
        return req.get_json()
    except ValueError:
        raise ParseException("Unable to parse JSON document in body")


def _is_valid_point_input(body):
    return "point" in body and "longitude" in body["point"] and "latitude" in body["point"]


def _is_valid_box_input(body):
    return "box" in body and len(body["box"]) == 4 and body["box"][0] <= body["box"][2] and body["box"][1] <= body["box"][3]


def _is_valid_trace_input(body):
    return "trace" in body and len(body["trace"]) > 1 and all(len(p) == 2 for p in body["trace"])