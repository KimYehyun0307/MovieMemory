from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # 마이그레이션 완료 후 fixtures.json 자동 로드
        post_migrate.connect(load_fixtures, sender=self)


def load_fixtures(sender, **kwargs):
    """
    fixtures.json 데이터를 로드합니다.
    """
    try:
        call_command('loaddata', 'accounts/fixtures/accounts/genre.json')
        call_command('loaddata', 'accounts/fixtures/accounts/users.json')
        print("Genres fixtures and Users samples loaded successfully.")
# 데이터를 로드한 후 비밀번호 해시 처리
        hash_user_passwords()

    except Exception as e:
        print(f"Error loading fixtures: {e}")


def hash_user_passwords():
    """
    로드된 유저 데이터의 비밀번호를 해시 처리합니다.
    """
    User = get_user_model()
    users = User.objects.all()

    with transaction.atomic():  # 트랜잭션을 사용하여 여러 사용자 비밀번호를 안전하게 처리
        for user in users:
            if user.password and not user.password.startswith(('pbkdf2_sha256$', 'bcrypt')):
                print(f"Hashing password for user: {user.username}")
                user.set_password(user.password)  # 비밀번호 해시 처리
                user.save()
