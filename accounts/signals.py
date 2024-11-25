from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, KakaoUser
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.signals import user_logged_in
# from django.utils.timezone import now

@receiver(post_save, sender=User)
def create_kakao_user(sender, instance, created, **kwargs):
    """
    유저가 생성될 때마다 카카오 유저 정보가 없다면 KakaoUser 모델에 기본 정보 저장
    """
    if created:
        try:
            # 카카오 유저와 관련된 정보가 이미 존재하는지 확인
            kakao_user = KakaoUser.objects.get(user=instance)
        except ObjectDoesNotExist:
            # 카카오 유저가 없다면 새로 생성
            KakaoUser.objects.create(
                user=instance,
                profile_nickname=instance.username,  # 기본적으로 카카오 유저의 닉네임을 username으로 설정
                profile_image='default_image_url',  # 기본 이미지 URL 또는 빈값 설정
                birthdate=None,  # 생년월일은 프로젝트 내에서 받으므로 초기값은 None
                genre_1=None,  # 장르는 프로젝트에서 선택하므로 초기값은 None
                genre_2=None,
                genre_3=None
            )
        # 카카오 유저가 이미 존재하면 추가로 정보를 업데이트하거나 추가 작업을 수행할 수 있음
        # 예: 카카오 유저 정보를 업데이트 (profile_nickname, profile_image 등)

@receiver(post_save, sender=KakaoUser)
def update_kakao_user_info(sender, instance, created, **kwargs):
    """
    카카오 유저 정보가 변경되었을 때(예: 닉네임, 이미지 변경 등), 해당 유저 정보를 업데이트.
    """
    if not created:
        # 카카오 유저의 정보가 변경되었을 때 처리
        instance.profile_nickname = instance.user.username  # 예시로, 닉네임을 사용자의 username으로 변경
        instance.save()

# @receiver(user_logged_in)
# def update_last_visited_at(sender, request, user, **kwargs):
#     user.visited_at = now()
#     user.save()

