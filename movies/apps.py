from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        # 마이그레이션 완료 후 fixtures.json 자동 로드
        post_migrate.connect(load_fixtures, sender=self)


def load_fixtures(sender, **kwargs):
    """
    fixtures.json 데이터를 로드합니다.
    """
    try:
        call_command('loaddata', 'movies/fixtures/movies/movies_data.json')  
        print("Genres fixtures loaded successfully.")
    except Exception as e:
        print(f"Error loading fixtures: {e}")
