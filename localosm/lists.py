#!/usr/bin/python3
import re

re_talk = re.compile('^[Tt]alk-(..)$')

central_america = ['bz', 'cr', 'gt', 'hn', 'ni', 'pa', 'sv']
south_america = ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'fk', 'gf', 'gy', 'gy',
                 'py', 'pe', 'sr', 'uy', 've']

africa = ['dz', 'ao', 'sh', 'bj', 'bw', 'bf', 'bi', 'cm', 'cv', 'cf', 'td',
          'km', 'cg', 'cd', 'dj', 'eg', 'gq', 'er', 'et', 'ga', 'gm', 'gh', 'gn',
          'gw', 'ci', 'ke', 'ls', 'lr', 'ly', 'mg', 'mw', 'ml', 'mr', 'mu', 'yt',
          'ma', 'mz', 'na', 'ne', 'ng', 'st', 're', 'rw', 'st', 'sn', 'sc', 'sl',
          'so', 'za', 'ss', 'sh', 'sd', 'sz', 'tz', 'tg', 'tn', 'ug', 'cd', 'zm',
          'tz', 'zw']

caribbean = ['ai', 'ag', 'aw', 'bs', 'bb', 'ky', 'cu', 'dm', 'do', 'gd', 'gp',
             'ht', 'jm', 'mq', 'ms', 'an', 'pr', 'kn', 'lc', 'vc', 'tt', 'tc',
             'vg', 'vi']

mailing_lists = {
    'af': 'Talk-af', 'al': 'Talk-al', 'ar': 'Talk-ar', 'at': 'Talk-at',
    'au': 'Talk-au', 'ba': 'Talk-ba', 'bd': 'Talk-bd', 'be': 'Talk-be',
    'bf': 'Talk-bf', 'bi': 'Talk-bi', 'bj': 'Talk-bj', 'bo': 'Talk-bo',
    'br': 'Talk-br', 'ca': 'Talk-ca', 'cd': 'Talk-cd', 'cf': 'Talk-cf',
    'ci': 'Talk-CI', 'cl': 'Talk-cl', 'cm': 'Talk-cm', 'cn': 'Talk-cn',
    'co': 'Talk-co', 'cr': 'Talk-cr', 'cu': 'Talk-cu', 'cz': 'Talk-cz',
    'de': 'Talk-de', 'dk': 'Talk-dk', 'do': 'Talk-do', 'es': 'Talk-es',
    'et': 'Talk-ET', 'fi': 'talk-fi', 'fr': 'Talk-fr', 'gb': 'Talk-GB',
    'ge': 'talk-ge', 'gh': 'Talk-gh', 'gr': 'Talk-gr', 'hn': 'Talk-hn',
    'hr': 'Talk-hr', 'ht': 'Talk-ht', 'id': 'Talk-id', 'ie': 'Talk-ie',
    'il': 'Talk-il', 'in': 'Talk-in', 'iq': 'Talk-iq', 'ir': 'Talk-ir',
    'is': 'Talk-is', 'it': 'Talk-it', 'ja': 'Talk-ja', 'ke': 'Talk-ke',
    'kg': 'Talk-kg', 'ko': 'Talk-ko', 'lb': 'Talk-lb', 'lk': 'Talk-lk',
    'lt': 'Talk-lt', 'lu': 'talk-lu', 'lv': 'Talk-lv', 'ma': 'Talk-ma',
    'mg': 'Talk-mg', 'ml': 'Talk-ml', 'mm': 'Talk-mm', 'mn': 'Talk-mn',
    'mw': 'Talk-mw', 'mx': 'Talk-mx', 'my': 'Talk-my', 'nc': 'Talk-nc',
    'ne': 'Talk-ne', 'ng': 'Talk-ng', 'ni': 'Talk-ni', 'nl': 'Talk-nl',
    'np': 'Talk-np', 'pe': 'Talk-pe', 'ph': 'talk-ph', 'pl': 'Talk-pl',
    'pr': 'talk-pr', 'ps': 'Talk-ps', 'pt': 'Talk-pt', 'py': 'Talk-py',
    'ro': 'Talk-ro', 'rs': 'Talk-rs', 'ru': 'Talk-ru', 'sc': 'Talk-sc',
    'se': 'Talk-se', 'si': 'Talk-si', 'sn': 'Talk-sn', 'sy': 'Talk-sy',
    'td': 'Talk-td', 'tg': 'Talk-tg', 'tn': 'Talk-tn', 'tr': 'Talk-tr',
    'tw': 'Talk-TW', 'tz': 'Talk-tz', 'ug': 'Talk-ug', 'us': 'Talk-us',
    'uy': 'Talk-uy', 've': 'Talk-ve', 'vi': 'Talk-vi', 'xk': 'Talk-kosovo',
    'za': 'Talk-ZA', 'zm': 'Talk-zm', 'zw': 'Talk-ZW'

}

def build_lookup_table():
    by_country_code = {}

    for code in central_america + south_america:
        by_country_code[code] = 'talk-latam'

    for code in africa:
        by_country_code[code] = 'Talk-africa'

    for code in caribbean:
        by_country_code[code] = 'Talk-carib'

    for country, ml in mailing_lists.items():
        by_country_code[country] = ml
    return by_country_code


by_country_code = build_lookup_table()

def lookup_fr(address):
    if address['state'] == 'Brittany':
        return 'Talk-fr-bzh'
    else:
        return 'Talk-fr'

def lookup_it(address):
    lc_state = address['state'].lower()
    if address['county'] == 'South Tyrol':
        return 'Talk-it-southtyrol'
    if address['county'] == "Territorio Val d'Adige":
        return 'Talk-it-trentino'

    if lc_state == 'piemont':
        return 'Talk-it-piemonte'
    if lc_state == 'mar':
        return 'Talk-it-marche'
    if lc_state == 'friuli venezia giulia':
        return 'Talk-it-fvg'
    if lc_state in ('basilicata', 'apulia'):
        return 'Talk-it-appulo-lucana'

    states = {'sardinia', 'sicilia', 'veneto', 'liguria', 'lazio'}

    if lc_state in states:
        return 'Talk-it-' + lc_state

    return 'Talk-it'

def lookup_gb(address):
    city = address.get('city')
    county = address.get('county')
    state_district = address.get('state_district')
    state = address.get('state')
    if 'London' in (city, county) or state_district == 'Greater London':
        return 'Talk-gb-london'
    if state == 'Scotland':
        return 'Talk-scotland'
    if state_district == 'West Midlands':
        return 'Talk-gb-westmidlands'
    if county in ('Gloucestershire', 'Oxfordshire'):
        # FIXME: not all of Gloucestershire is in the Cotswolds
        # should consider the Cotswolds AONB polygon
        return 'Talk-gb-oxoncotswolds'
    if county == 'Cambridgeshire':
        return 'Talk-gb-midanglia'
    the_north = ('North West England', 'North East England',
                 'Yorkshire and the Humber')
    if state_district in the_north:
        return 'Talk-gb-thenorth'

    return 'Talk-GB'

def lookup_us(address):
    state = address.get('state')
    county = address.get('county')
    if state == 'Massachusetts':
        return 'Talk-us-massachusetts'
    if state == 'New York':
        return 'Talk-us-newyork'

    sfbay = {'Alameda County', 'Contra Costa County', 'Marin County',
             'Napa County', 'San Francisco City and County', 'San Mateo County',
             'Santa Clara County', 'Solano County', 'Sonoma County',
             'San Benito County', 'San Joaquin County', 'Santa Cruz County'}

    if state == 'California' and county in sfbay:
        return 'Talk-us-sfbay'

    puget_sound = {'King County', 'Kitsap County', 'Thurston County',
                   'Snohomish County', 'Pierce County', 'Island County',
                   'Mason County', 'Skagit County', 'Jefferson County'}

    if state == 'Washington' and county in puget_sound:
        return 'Talk-us-pugetsound'

    return 'Talk-us'


extra_lookup = {
    'us': lookup_us,
    'gb': lookup_gb,
    'fr': lookup_fr,
    'it': lookup_it,
    'us': lookup_us,
}

def lookup(address):
    if not address:
        return
    c = address.get('country_code')
    if c in extra_lookup:
        return extra_lookup[c](address)
    else:
        return by_country_code.get(c)


done = {'Talk-transit', 'Talk-baltics', 'Talk-blr', 'Talk-kosovo',
        'Talk-fr-bzh', 'Talk-gb-london', 'Talk-scotland',
        'Talk-gb-westmidlands', 'Talk-gb-oxoncotswolds', 'Talk-gb-midanglia',
        'Talk-gb-thenorth', 'Talk-us-massachusetts', 'Talk-us-newyork',
        'Talk-us-sfbay', 'Talk-us-pugetsound', 'Talk-us-nps', 'Talk-cat',
        'talk-latam', 'Talk-africa', 'Talk-carib'}

def build_list():
    for line in open('lists'):
        line = line[:-1]
        ml, description = line.split('\t')
        if ml in done or ml.startswith('Talk-it-'):
            continue
        # print((ml, description))

        m = re_talk.match(ml)
        if m:
            by_country_code[m.group(1).lower()] = ml
        else:
            print('{:25s}  {}'.format(ml, description))
