from datetime import datetime
from pathlib import Path
from time import time

import pandas as pd
import pytz

from utils import save_to_csv
import config
from youtube import YouTube
from logger import setup_logging
import requests
from requests.exceptions import RequestException

import logging
from typing import Any, Dict, List
from config import API_KEY
import json

_LOGGER = logging.getLogger(__name__)


region_list = [
        ('VN', 'Vietnam'),
        ('GB', 'United Kingdom'),
        ('CA', 'Canada'),
        ('DE', 'Germany'),
        ('KR', 'South Korea'),
        ('RU', 'Russia'),
        ('UA', 'Ukraine'),
        ('JP', 'Japan'),
        ('US', 'United States'),
        ('HK', 'Hong Kong'),
]

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

api_key = API_KEY
url = "https://www.googleapis.com/youtube/v3/videoCategories"

def _get(payload: Dict[str, Any]):
    try:
        res = requests.get(url, params=payload)
        res.raise_for_status()
    except RequestException:
       
        print("Error while retrieving based on payload: {}".format(payload))
        
    else:
        return res.json()

for region in region_list:
    payload = {
        "key": api_key,
        "part": "snippet",
        "regionCode": region[0]
    }

    response = _get(payload=payload)
    category_list = response.get("items")
    _LOGGER.warning("Got %d category from youtube %s", len(category_list), region[0])
    filename = Path(__file__).parent / f"category_list/{region[0]}_category_id.json"
    with open(filename, 'w') as f:
        json.dump(category_list, f)