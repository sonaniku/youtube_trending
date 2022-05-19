"""Worker to extract  Trending YouTube Video Statistics."""
import logging
from datetime import datetime
from pathlib import Path
from time import time
import os
import isodate
import pandas as pd
import pytz
import json
from . import config
from dateutil import parser
import calendar
import psycopg2
from sqlalchemy import create_engine

# from . import common
# from ytid_trends import common

from .utils import save_to_csv
# from common.utils import save_to_csv
from .youtube import YouTube
from .logger import setup_logging


_LOGGER = logging.getLogger(__name__)


def load_category(region_id):
    category_list = []
    path_json = Path(__file__).parent / f"category_list/{region_id}_category_id.json"
    with open(path_json) as f:
        data = json.load(f)
        for i in data:
            print(f"id: {i['id']}")
            print(f"title: {i['snippet']['title']}")
            print(1)
            category_list.append({'id': i['id'], 'title': i['snippet']['title']})
            # print(2)
            # print(f"category_list[{count}]: {category_list[count]}")
            # print(f"id: {category_list[count]['id']}")
            # print(f"title: {category_list[count]['title']}")
            # print(3)
            # count = count + 1
            # print(4)
    return category_list


def TransformCategoryId(cateid, category_list):
    # print(category_list)
    c = 0
    r = []
    l = len(category_list)
    print(cateid)
    for i in cateid:
        print(f"\t- i: {i}")
        flag = False
        for j in range(l):
            if(int(i) == int(category_list[j]["id"])):
                #print(f"j: {j}")
                r.append(category_list[j]["title"])
                flag = True
        if(flag == False):
            r.append("unknown")
        print(f"r[{c}] = {r[c]}")
        c = c + 1
    return r

def TransformPublishDate_day_in_week(published_at: str):
    day_in_week_result = []
    for d in published_at:
        published_date = parser.parse(d)
        day_in_week = calendar.day_name[published_date.weekday()]
        day_in_week_result.append(day_in_week)
    return day_in_week_result
    pass

def TransformPublishDate_hour_in_day(published_at):
    hour_result = []
    for d in published_at:
        published_date = parser.parse(d)
        hour = published_date.hour
        hour_result.append(hour)
    return hour_result
    pass

def TransformDuration(duration_list):
    r = []
    for i in duration_list:
        r.append(isodate.parse_duration(i))
    return r
    pass

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
    _LOGGER.info("Start retrieving  youtube trending videos")
    now = datetime.now(tz=pytz.utc)
    dataset_version = datetime.now(tz=pytz.timezone("UTC"))
    dataset_version = dataset_version.strftime("%Y%m%d.%H%M")

    youtube = YouTube(
        url=config.URL,
        api_key=config.API_KEY
    )
    os.mkdir(Path(__file__).parent / f"archive/{dataset_version}")

    print(f"{youtube.url = } - {youtube.api_key = }")

    conn_string = 'postgresql://postgres:admin123456@youtube-trending.csnauvtnhw7m.us-east-1.rds.amazonaws.com/youtube_trending_videos'
    # conn = psycopg2.connect(
    #     host="youtube-trending.csnauvtnhw7m.us-east-1.rds.amazonaws.com",
    #     database="youtube_trending_videos",
    #     user="postgres",
    #     password="admin123456"
    # )
    db = create_engine(conn_string)
    try:
        conn = db.connect()
    except ConnectionError as e:
        print(e)
    ##########
    for region in region_list:
        category_list = load_category(region[0])

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

        ##### transform
        df_videos["category_name"] = TransformCategoryId(df_videos["category_id"], category_list)
        df_videos["region_id"] = region[0]
        df_videos["region_name"] = region[1]
        
        df_videos["hour_in_day"] = TransformPublishDate_hour_in_day(df_videos["publish_time"])
        df_videos["day_in_week"] = TransformPublishDate_day_in_week(df_videos["publish_time"])
        
        df_videos["dislike"] = 0
        df_videos["duration"] = TransformDuration(df_videos["duration"])
        ##### save archive
        filename_archive = Path(
            __file__).parent / f"archive/{dataset_version}/{region[0]}_trending_{dataset_version}.csv"
        print(f"{filename_archive = }")
        save_to_csv(df_videos, filename_archive.as_posix())
        df_saved = pd.read_csv(filename_archive)
        _LOGGER.info("Done saving %d trending videos (%s). Total videos: %d",
                     df_videos.shape[0], filename_archive, df_saved.shape[0])

        ##### save data
        filename_data = Path(__file__).parent / f"data/trendings.csv"
        save_to_csv(df_videos, filename_data.as_posix())
        df_saved_data = pd.read_csv(filename_data)
        _LOGGER.info("Done saving %d trending videos to data folder (%s). Total videos: %d",
                     df_videos.shape[0], filename_data, df_saved_data.shape[0])
        
        ##### insert to database
        df_videos.to_sql('trending_videos', con=conn, if_exists='append', index=False)
        conn = psycopg2.connect(conn_string
                        )
        conn.autocommit = True
    
    conn.close()


if __name__ == "__main__":
    setup_logging(config.LOG_LEVEL)
    get_trending_videos()
