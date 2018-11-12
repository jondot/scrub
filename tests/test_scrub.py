from scrub import scrub_body, scrub_headers, scrub_request
import base64
from requests import Request, Session


sensitive_headers = {
    "x-api-key": "--key--",
    "x-date": "--filtered--",
    "Set-Cookie": "--filtered--",
}

sensitive_data = {
    "<Secret>.*</Secret>": "<Secret>{}</Secret>".format(
        base64.b64encode(b"--filtered--").decode()
    ),
    "{.*}": "{}",
}


def test_body(snapshot):
    scrubber = scrub_body(sensitive_data)
    snapshot.assert_match(scrubber(b'{"secret":"foobar"}'))
    snapshot.assert_match(scrubber(b"<xml><Secret>shazam!</Secret></xml>"))


def test_headers(snapshot):
    scrubber = scrub_headers(sensitive_headers)
    snapshot.assert_match(
        scrubber(
            {
                "x-api-key": "3faf",
                "x-date": "Oct 18 2001",
                "Set-Cookie": "secret=3faf00",
                "Accept": "application/json",
            }
        )
    )


def test_request(snapshot):
    r = Request(
        "POST",
        "http://localhost",
        data=b'{"secret":"foobar"}',
        headers={
            "x-api-key": "3faf",
            "x-date": "Oct 18 2001",
            "Set-Cookie": "secret=3faf00",
        },
    )
    req = r.prepare()
    nil_scrubber = scrub_request(lambda x: x, lambda x: x)
    nil_scrubber(req)
    snapshot.assert_match({"body": req.body, "headers": dict(req.headers)})

    scrubber = scrub_request(
        scrub_headers(sensitive_headers), scrub_body(sensitive_data)
    )
    scrubber(req)
    snapshot.assert_match({"body": req.body, "headers": req.headers})

