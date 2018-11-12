# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_headers 1'] = {
    'Accept': 'application/json',
    'Set-Cookie': '--filtered--',
    'x-api-key': '--key--',
    'x-date': '--filtered--'
}

snapshots['test_body 1'] = b'{}'

snapshots['test_body 2'] = b'<xml><Secret>LS1maWx0ZXJlZC0t</Secret></xml>'

snapshots['test_request 1'] = {
    'body': b'{"secret":"foobar"}',
    'headers': {
        'Content-Length': '19',
        'Set-Cookie': 'secret=3faf00',
        'x-api-key': '3faf',
        'x-date': 'Oct 18 2001'
    }
}

snapshots['test_request 2'] = {
    'body': b'{}',
    'headers': {
        'Content-Length': '19',
        'Set-Cookie': '--filtered--',
        'x-api-key': '--key--',
        'x-date': '--filtered--'
    }
}
