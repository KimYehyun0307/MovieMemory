# communities/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class CommunitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communities'

    def ready(self):
        # 신호 연결을 ready() 메서드 내에서 직접 하지 않고, 앱이 완전히 로드된 후에 연결
        from django.db.models import signals
        signals.post_migrate.connect(self.update_screening_schedule)

    def update_screening_schedule(self, sender, **kwargs):
        from .utils import fetch_and_save_upcoming_movies
        fetch_and_save_upcoming_movies()
