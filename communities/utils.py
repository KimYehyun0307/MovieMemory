# communities/utils.py
import requests
from django.conf import settings
from .models import ScreeningSchedule
from datetime import datetime

def get_upcoming_movies_from_tmdb():
    # TMDB API로 상영 예정작 데이터를 요청
    url = f"https://api.themoviedb.org/3/movie/upcoming"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR',
        'region': 'KR',  # 한국 상영 예정작
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

def fetch_and_save_upcoming_movies():
    # TMDB에서 상영 예정작 데이터를 가져옵니다.
    upcoming_movies = get_upcoming_movies_from_tmdb()

    for movie_data in upcoming_movies:
        # 영화 제목, 상영 날짜, 상영 시간을 얻습니다.
        title = movie_data['title']
        release_date = movie_data['release_date']

        try:
            release_date_obj = datetime.strptime(release_date, "%Y-%m-%d").date()
        except ValueError:
            release_date_obj = None

        # ScreeningSchedule 객체 생성 및 저장
        if release_date_obj:
            ScreeningSchedule.objects.create(
                movie_title=title,  # 상영 예정 영화 제목
                screening_date=release_date_obj,  # 상영 날짜
            )
        else:
            print(f"Invalid date format for movie: {title}")
