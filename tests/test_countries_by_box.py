import json
import unittest

import azure.functions as func

from countries_by_box.api import main


def test_countries_by_point():
    req = func.HttpRequest(
        method="POST",
        url="/api/countries/by-box",
        params=None,
        body=b'{"box": [8.36, 43.22, 11.93, 51.15]}'
    )

    result = json.loads(main(req).get_body())
    assert len(result) == 4
    
    conv_result = [(country["name"], country["continent"]) for country in result]
    assert(("Germany", "Europe") in conv_result)
    assert(("Switzerland", "Europe") in conv_result)
    assert(("Austria", "Europe") in conv_result)
    assert(("Italy", "Europe") in conv_result)