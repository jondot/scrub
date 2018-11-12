from datetime import datetime
import base64
import re
from os import getenv
from toolz.curried import itemmap, reduce


def scrub_headers(headermap):
    return itemmap(lambda h: (h[0], headermap.get(h[0], h[1])))


def scrub_body(datamap):
    return lambda body: reduce(
        lambda body_ongoing, p: re.sub(p[0], p[1], body_ongoing),
        datamap.items(),
        (body or b"").decode("utf-8"),
    ).encode("utf-8")


def scrub_request(headerscrubber, datascrubber):
    def req_scrubber(req):
        req.headers = headerscrubber(req.headers)
        req.body = datascrubber(req.body)
        return req

    return req_scrubber
