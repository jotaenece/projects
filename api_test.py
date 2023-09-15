#!/usr/bin/env python3
# python3 ./api_test.py -v


import numpy as np
import pandas as pd
import requests as rq

# enter api credentials

# get data from api
url = 'https://api.census.gov/data/2019/pep/population?get=POP,GEONAME&for=state:*&DATE_CODE=12'
response = rq.get(url)
data = rq.json()

print(data)