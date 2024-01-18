[![Build Python distribution and Release](https://github.com/cloudcover-cc/cc-taxii2-client/actions/workflows/python-publish.yml/badge.svg)](https://github.com/cloudcover-cc/cc-taxii2-client/actions/workflows/python-publish.yml)
[![Python 3.9](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

# cc-taxii2-client
## Minimal CloudCover TAXII2.1 Python client library.

### Installation
To install from PyPI run:
```
pip install cc-taxii2-client
```

To install from source, run the following commands:
```
git clone https://github.com/cloudcover-cc/cc-taxii2-client
cd cc-taxii2-client
pip install .
```

### Basic usage examples:

```python
from itertools import chain
from cc_taxii2_client import (CCTaxiiClient, count_indicators, ip_search,
                              description_search)

# Create a CloudCover TAXII2.1 server connection client object:
connection = CCTaxiiClient("testaccount", "XxXxXx")
# RETURNS:
# CCTaxiiClient(account='testaccount',
#               url='https://taxii2.cloudcover.net',
#               headers={
#                   'Accept': 'application/taxii+json;version=2.1',
#                   'Content-Type': 'application/taxii+json;version=2.1',
#                   'Authorization': 'Basic dGVzdF9hY2NvdW50Olh4WHhYeA=='
#               })

# Get collection IDs for the public (/api/) root silo
connection.get_collections()
# RETURNS:
# ['decb0efc-6a36-4dd7-a4dd-7f955f42b977']

# Get collection IDS for private (/account/) root silo
connection.get_collections("testaccount")
# RETURNS:
# ['c774c554-038c-46a6-8339-9ddfae4cd871']

# Create a generator object that yields all indicators in the public root
#   silo default collection, grouped in pages of 1000 (default) indicators:
generate_indicators = connection.get_cc_indicators_generator(follow_pages=True)

# Count total number of indicators yielded from the generator:
count_indicators(generate_indicators)
# RETURNS:
# 711

# Create a generator object that yields all indicators in the private root
#   silo default collection, grouped in pages of 2 indicators, added only
#   after 2023-11-03T19:07:51.812746Z:
generate_indicators = connection.get_cc_indicators_generator(
    private=True,
    limit=2,
    added_after="2023-11-03T19:07:51.812746Z",
    follow_pages=True)

# Yield the pages of indicators:
next(generate_indicators)
# YIELDS:
# [
#     CCIndicator(created='2023-11-03T19:07:51.812746Z',
#                 description='#Recon# ICMP PING',
#                 id='indicator--5c46d792-93a9-435c-a04f-b843de740fe6',
#                 modified='2023-11-03T19:07:51.812746Z',
#                 name='CloudCover Detected IOC',
#                 pattern="[ipv4-addr:value = '13.127.11.123']",
#                 pattern_type='stix',
#                 pattern_version='2.1',
#                 spec_version='2.1',
#                 type='indicator',
#                 valid_from='2023-11-03T19:07:51.812746Z'),
#     CCIndicator(created='2023-11-03T19:07:51.816509Z',
#                 description='#Recon# ICMP PING',
#                 id='indicator--3d217760-a17a-41b4-af5f-5b5bf72ff396',
#                 modified='2023-11-03T19:07:51.816509Z',
#                 name='CloudCover Detected IOC',
#                 pattern="[ipv4-addr:value = '34.219.199.125']",
#                 pattern_type='stix',
#                 pattern_version='2.1',
#                 spec_version='2.1',
#                 type='indicator',
#                 valid_from='2023-11-03T19:07:51.816509Z')
# ]

# Search generator results for indicators containing a specific IP address:
generate_indicators = connection.get_cc_indicators_generator(private=True,
                                                             follow_pages=True)
ip_search("13.127.11.123", generate_indicators)
# RETURNS:
# [
#     CCIndicator(created='2023-11-03T19:07:51.812746Z',
#                 description='#Recon# ICMP PING',
#                 id='indicator--5c46d792-93a9-435c-a04f-b843de740fe6',
#                 modified='2023-11-03T19:07:51.812746Z',
#                 name='CloudCover Detected IOC',
#                 pattern="[ipv4-addr:value = '13.127.11.123']",
#                 pattern_type='stix',
#                 pattern_version='2.1',
#                 spec_version='2.1',
#                 type='indicator',
#                 valid_from='2023-11-03T19:07:51.812746Z')
# ]

# Search generator results for indicators containing "Recon" in the description
#   field, then get the total number found:
generate_indicators = connection.get_cc_indicators_generator(private=True,
                                                             follow_pages=True)
indicators = description_search("Recon", generate_indicators)
len(indicators)
# RETURNS:
# 264

# Create a generator object that yields all indicators in the private root
#   silo default collection, grouped in pages of 1000 (default) indicators,
#   of type "indicator" that match the two indicator IDs given. Then combine
#   all found indicator objects into a single list:
generate_indicators = connection.get_cc_indicators_generator(
    private=True,
    follow_pages=True,
    matches={
        "type":
        "indicator",
        "id": ("indicator--5c46d792-93a9-435c-a04f-b843de740fe6,"
               "indicator--6b405c16-ac9b-4446-8d13-1cc17a4cf867")
    })
list(chain(*generate_indicators))
# RETURNS:
# [
#     CCIndicator(created='2023-11-03T19:07:51.812746Z',
#                 description='#Recon# ICMP PING',
#                 id='indicator--5c46d792-93a9-435c-a04f-b843de740fe6',
#                 modified='2023-11-03T19:07:51.812746Z',
#                 name='CloudCover Detected IOC',
#                 pattern="[ipv4-addr:value = '13.127.11.123']",
#                 pattern_type='stix',
#                 pattern_version='2.1',
#                 spec_version='2.1',
#                 type='indicator',
#                 valid_from='2023-11-03T19:07:51.812746Z'),
#     CCIndicator(created='2023-11-03T19:07:51.817258Z',
#                 description='#Recon# ICMP PING',
#                 id='indicator--6b405c16-ac9b-4446-8d13-1cc17a4cf867',
#                 modified='2023-11-03T19:07:51.817258Z',
#                 name='CloudCover Detected IOC',
#                 pattern="[ipv4-addr:value = '34.218.245.10']",
#                 pattern_type='stix',
#                 pattern_version='2.1',
#                 spec_version='2.1',
#                 type='indicator',
#                 valid_from='2023-11-03T19:07:51.817258Z')
# ]
```
