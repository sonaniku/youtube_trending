"""Worker to extract  Trending YouTube Video Statistics."""
import logging
from datetime import datetime
from pathlib import Path
from time import time
import os
import pandas as pd
import pytz

from . import config

# from . import common
# from ytid_trends import common

from .utils import save_to_csv
# from common.utils import save_to_csv
from .youtube import YouTube
from .logger import setup_logging


_LOGGER = logging.getLogger(__name__)


def get_trending_videos():
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
    _LOGGER.info("Start retrieving indonesia youtube trending videos")
    now = datetime.now(tz=pytz.utc)
    dataset_version = datetime.now(tz=pytz.timezone("UTC"))
    dataset_version = dataset_version.strftime("%Y%m%d.%H%M")

    youtube = YouTube(
        url=config.URL,
        api_key=config.API_KEY
    )
    print(f"{youtube.url = } - {youtube.api_key = }")
    for region in region_list:
        start = time()
        videos = youtube.get_trendings(region_code=region[0])
        end = time()
        _LOGGER.debug("Done retrieving raw video data in %.3fs", (end - start))
        
        # Add column trending_time = now 
        df_videos = pd.DataFrame([
            video.to_dict(trending_time=now)
            for video in videos
        ])
        _LOGGER.info("Got total %d trending videos", df_videos.shape[0])
        
        filename = Path(__file__).parent / f"data/{region[0]}_trending_{dataset_version}.csv"
        print(f"{filename = }")
        save_to_csv(df_videos, filename.as_posix())
        df_saved = pd.read_csv(filename)
        _LOGGER.info("Done saving %d trending videos (%s). Total videos: %d",
                    df_videos.shape[0], filename, df_saved.shape[0])


if __name__ == "__main__":
    setup_logging(config.LOG_LEVEL)
    get_trending_videos()
