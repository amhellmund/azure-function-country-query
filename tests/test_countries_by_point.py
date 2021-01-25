import json
import unittest

import azure.functions as func

from countries_by_point.api import main


def test_countries_by_point():
    req = func.HttpRequest(
        method="POST",
        url="/api/countries/by-point",
        params=None,
        body=b'{"point": {"longitude": 8.5, "latitude": 51.2}}'
    )

    result = json.loads(main(req).get_body())
    assert len(result) == 1
    assert result[0]["name"] == "Germany"
    assert result[0]["continent"] == "Europe"