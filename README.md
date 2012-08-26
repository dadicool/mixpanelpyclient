Mixpanel Analytics API python client
====================================

Overview:
---------
This library enables any python process to upload events to the Mixpanel analytics service
It's compatible with python 2.6/2.7 and python 3.2

This implementation is inspired from this blog [post](http://blog.coredumped.org/2012/05/using-mixpanel-with-python.html)

Usage :
-------
- drop mixpanelpyclient into your project

Example :
---------

        TOKEN = XYZ // Mixpanel Token
        tracker = EventTracker(TOKEN)
        tracker.track_async("My Event", {
            "distinct_id": "123",
	    "mp_tag_name": "My User Name",
            "my_property": "some value",
            "some_int_value": 0,
        })

Tests :
-------
`python test.py`
