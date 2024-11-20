from allauth.socialaccount.models import SocialAccount

def user_info(request):
    user = request.user
    kakao_account = None

    # 로그인된 사용자이고 카카오 로그인인 경우
    if user.is_authenticated:
        kakao_account = user.socialaccount_set.filter(provider='kakao').first()

    return {
        'kakao_account': kakao_account,  # 카카오 계정 정보
        'user': user,  # 사용자 정보
    }
