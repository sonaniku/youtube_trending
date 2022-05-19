"""Module consists of necessary configurations."""
import os
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

API_KEY = os.getenv("API_KEY", "AIzaSyAsxGJC3H7c8yrFKBTI5pTCEDx0T_Ul2Ig")
URL = os.getenv("URL", "https://www.googleapis.com/youtube/v3/videos")
DATADIR = os.getenv("DATADIR", "/youtube/youtube_trending/home/data")
CATEGORYDIR = os.getenv("CATEGORYDIR", "/youtube_trending/home/category_list")
print(f"{ LOG_LEVEL =  }")
print(f"{ API_KEY =  }")
print(f"{ URL =  }")
print(f"{ DATADIR =  }")
