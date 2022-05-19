import sys
from django.apps import AppConfig
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .models import LatestUpdated
        from django.db.models import Max
        from .get_trending_videos import get_trending_videos
        from datetime import datetime, date
        print("Home ready")
        latest_updated_date = date.today()
        print(f"{latest_updated_date = }")
        temp = LatestUpdated.objects.filter(latest_updated_date=latest_updated_date)
        print(f"{temp = }")
        if not temp:
            print("True")
            flag = False
            try:
                get_trending_videos()
                flag = True
            except Exception as e: 
                print(f"Exception: {e}")
            if flag == True: 
                LatestUpdated.objects.create(latest_updated_date = date.today())
        else:
            print(f"{latest_updated_date = }")