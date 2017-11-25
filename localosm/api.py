from flask import request, jsonify
import json
from . import nominatim, lists

def lookup():
    args = {}
    for key in 'q', 'lat', 'lon', 'osm_type', 'osm_id', 'error':
        value = request.args.get(key)
        if value:
            value = value.strip()
            if value:
                args[key] = value
    if 'error' in args:
        return jsonify(**args)

    q = args['q'] if 'q' in args else None

    if q and ('lat' in args or 'lon' in args):
        return jsonify(error='either q or lat/lon, not both',
                       **args)

    if ('lat' in args) != ('lon' in args):
        return jsonify(error='half of lat/lon missing', **args)

    if ('osm_type' in args) != ('osm_id' in args):
        return jsonify(error='half of osm_type/osm_id missing', **args)

    if q and not ('lat' in args and 'lon' in args):
        coords = nominatim.parse_coords(q)
        if coords:
            args['lat'], args['lon'] = coords

    if 'osm_type' in args and 'osm_id' in args:
        osm_type = args['osm_type']
        osm_id = args['osm_id']
        errors = []
        if osm_type[0].upper() not in {'N', 'W', 'R'}:
            errors.append('osm_type must be one of N, W or R')
        if osm_id.isdigit():
            args['osm_id'] = int(args['osm_id'])
        else:
            errors.append('osm_id must be an integer')
        if errors:
            return jsonify(error=', '.join(errors), **args)

        r = nominatim.reverse_osm(osm_type[0].upper(), osm_id)
        try:
            result = nominatim.parse_json(r)
        except json.decoder.JSONDecodeError:
            return jsonify(error=r.text, **args)
    elif 'lat' in args and 'lon' in args:
        errors = []
        try:
            lat = float(args['lat'])
            args['lat'] = lat
        except ValueError:
            errors.append('lat invalid')
        else:
            if not (90 > lat > -90):
                errors.append('lat out of range')

        try:
            lon = float(args['lon'])
            args['lon'] = lon
        except ValueError:
            errors.append('lon invalid')
        else:
            if not (180 > lon > -180):
                errors.append('lon out of range')

        if errors:
            return jsonify(error=', '.join(errors), **args)

        r = nominatim.reverse_latlon(lat, lon)

        try:
            result = nominatim.parse_json(r)
        except json.decoder.JSONDecodeError:
            return jsonify(error=r.text, **args)
    else:
        r = nominatim.lookup(q)
        result_list = nominatim.parse_json(r)
        result = result_list[0] if result_list else {}
        if 'lat' in result and 'lon' in result:
            args['lat'] = result['lat']
            args['lon'] = result['lon']

    address = result.get('address')
    ml = lists.lookup(address)

    return jsonify(local_match=bool(ml), list=(ml or 'talk'), **args)
