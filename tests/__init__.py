import unittest

import sys
sys.path.insert(0, '..')
from os import environ

from mixpanelpyclient import EventTracker


class TestMixpanel(unittest.TestCase):

    def test_successful_upload(self):
        tracker = EventTracker(environ['TOKEN'])
        tracker.track_async("My Event", {
            "distinct_id": "123",
	    "mp_tag_name": "My User Name",
            "my_property": "some value",
            "some_int_value": 0,
        })
