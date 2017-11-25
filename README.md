# localosm

Tool/API to find local OSM mailing lists by location.

https://local.openstreetmap.directory/

The web interface handles searching by place name or lat/lon, the API can
be queried by place name, lat/lon and OSM object.

This is a proof of concept, I threw it together to see if it useful.

## Use cases

Systems for organising remote mapathons, like missing maps, could use the API
to look up the local mailing list and remind the organiser to contact the
local community to let them know about the mapathon.

An assisted editing tool like MapRoulette might show details of the local
mailing list so mappers know how to contact if they're making a complex edit
and they want to check with the local community that the edit is correct.

## Examples

Here are some example queries and the result:

    Cuba:          Talk-cu
    Rome:          Talk-it-lazio
    Burkina Faso:  Talk-bf
    Oxford:        Talk-gb-oxoncotswolds
    Timbuktu:      Talk-ml
    47.6,-122.3:   Talk-us-pugetsound

## How it works

The heavy lifting is done via the Nominatim API. For every lookup it issues a
query to Nominatim and uses the address information to determine the local
mailing list.

The algorithm for finding mailing lists is in localosm/lists.py
