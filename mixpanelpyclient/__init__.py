"""
Event tracking, currently uses Mixpanel: https://mixpanel.com
"""
TRACK_BASE_URL = "http://api.mixpanel.com/track/?data=%s"
ARCHIVE_BASE_URL = "http://api.mixpanel.com/import/?data=%s&api_key=%s"

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import json
import base64
import time

class EventTracker(object):
  """Simple Event Tracker
  Designed to be generic, but currently uses Mixpanel
  to actually handle the tracking of the events
  """
  def __init__(self, token, api_key=None):
    """Create a new event tracker
    :param token: The auth token to use to validate each request
    :type token: str
    """
    self.token = token
    self.api_key = api_key

  def track(self, event, properties=None, callback=None):
    """Track a single event
    :param event: The name of the event to track
    :type event: str
    :param properties: An optional dict of properties to describe the event
    :type properties: dict
    :param callback: An optional callback to execute when
      the event has been tracked.
      The callback function should accept two arguments, the event
      and properties, just as they are provided to this function 
      This is mostly used for handling Async operations
    :type callback: function
    """
    if properties is None:
      properties = {}
    if 'token' not in properties:
      properties['token'] = self.token
    if 'time' not in properties:
      properties['time'] = int(time.time())

    assert('distinct_id' in properties), "Must specify a distinct ID"

    params = {"event": event, "properties": properties}
    data = base64.b64encode(json.dumps(params).encode('ascii'))
    if self.api_key:
      resp = urlopen(ARCHIVE_BASE_URL % (data.decode('ascii'), self.api_key))
    else:
      resp = urlopen(TRACK_BASE_URL % data.decode('ascii'))
    resp.read()

    if callback is not None:
      callback(event, properties)

  def track_async(self, event, properties=None, callback=None):
    """Track an event asyncrhonously, essentially this runs the track
    event in a new thread
    :param event: The name of the event to track
    :type event: str
    :param properties: An optional dict of properties to describe the event
    :type properties: dict
    :param callback: An optional callback to execute when the event has been
      tracked. The callback function should accept two arguments, the event
      and properties, just as they are provided to this function
    :type callback: function

    :return: Thread object that will process this request
    :rtype: :class:`threading.Thread`
    """
    from threading import Thread
    t = Thread(target=self.track, kwargs={
      'event': event, 
      'properties': properties, 
      'callback': callback
    })
    t.start()
    return t

tracker = EventTracker('723a07346e7ddadcca1e556886b4a403')
tracker.track_async("My Event", {
   "distinct_id": "123", 
   "mp_tag_name": "My User Name",
   "my_property": "some value",
   "some_int_value": 0,
})
