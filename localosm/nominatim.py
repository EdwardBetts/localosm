from flask import current_app
from collections import OrderedDict
import json
import requests
import re

re_latlon = re.compile('^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*'
                       '[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$')

def parse_coords(q):
    m = re_latlon.match(q)
    if m:
        lat, _, lon = q.partition(',')
        return lat, lon

class SearchError(Exception):
    pass

def admin_email():
    return current_app.config['ADMIN_EMAIL']

def reverse(**kwargs):
    url = 'http://nominatim.openstreetmap.org/reverse'

    params = {
        'format': 'json',
        'addressdetails': 1,
        'namedetails': 1,
        'email': admin_email(),
        'accept-language': 'en',
    }

    params.update(**kwargs)

    r = requests.get(url, params=params)
    if r.status_code == 500:
        raise SearchError

    return r

def reverse_latlon(lat, lon):
    return reverse(lat=lat, lon=lon)

def reverse_osm(osm_type, osm_id):
    return reverse(osm_type=osm_type, osm_id=osm_id)

def lookup(q):
    url = 'http://nominatim.openstreetmap.org/search'

    params = {
        'format': 'jsonv2',
        'addressdetails': 1,
        'namedetails': 1,
        'email': admin_email(),
        'limit': 1,
        'polygon_geojson': 1,
        'accept-language': 'en',
    }

    params.update(q=q)

    r = requests.get(url, params=params)
    if r.status_code == 500:
        raise SearchError

    return r

def parse_json(r):
    return json.loads(r.text, object_pairs_hook=OrderedDict)
