from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # 장르 목록을 자동으로 업데이트
        from accounts.models import Genre
        Genre.update_genres_from_tmdb()