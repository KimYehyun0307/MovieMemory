from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # 마이그레이션 완료 후 장르 목록 업데이트
        post_migrate.connect(self.update_genres, sender=self)

    def update_genres(self, sender, **kwargs):
        from accounts.models import Genre
        Genre.update_genres_from_tmdb()