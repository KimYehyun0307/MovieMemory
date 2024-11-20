from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import User, KakaoUser, Genre
from .forms import CustomUserCreationForm
from social_django.utils import psa
import requests
import os

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "로그인 성공!")
            return redirect('movies:index')  # 메인 페이지로 리다이렉트
        else:
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect('accounts:login')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # 기본 로그인 처리시 backend 명시
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # 기본 인증 백엔드
            messages.success(request, "회원가입 성공!")
            return redirect('movies:index')
        else:
            messages.error(request, "회원가입 중 오류가 발생했습니다.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, "회원탈퇴가 완료되었습니다.")
        return redirect('accounts:login')
    return render(request, 'accounts/delete_account.html')

def kakao_login(request):
    kakao_api_key = settings.KAKAO_REST_API_KEY
    redirect_uri = request.build_absolute_uri('/accounts/kakao/callback/')
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={kakao_api_key}&redirect_uri={redirect_uri}"
    return redirect(kakao_auth_url)

def kakao_callback(request):
    """카카오 로그인 후 콜백을 처리하는 뷰"""
    code = request.GET.get('code')
    kakao_api_key = settings.KAKAO_REST_API_KEY
    redirect_uri = request.build_absolute_uri('/accounts/kakao/callback/')
    token_url = f"https://kauth.kakao.com/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": kakao_api_key,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    # 카카오로부터 액세스 토큰을 받아오기
    try:
        token_response = requests.post(token_url, headers=headers, data=data).json()
        access_token = token_response.get('access_token')
        if not access_token:
            raise ValueError("Access token not found.")
    except Exception as e:
        messages.error(request, f"카카오 로그인 중 오류가 발생했습니다: {str(e)}")
        return redirect('movies:index')

    user_info_url = "https://kapi.kakao.com/v2/user/me"
    user_info_headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        # 카카오 사용자 정보 가져오기
        user_info_response = requests.get(user_info_url, headers=user_info_headers).json()
        kakao_account = user_info_response.get('kakao_account', {})
        profile = kakao_account.get('profile', {})
        username = f"kakao_{user_info_response.get('id')}"
        nickname = profile.get('nickname')
        profile_image = profile.get('profile_image_url')

        # 이미지 다운로드 및 저장 (media/profile에 저장)
        if profile_image:
            image_response = requests.get(profile_image)
            if image_response.status_code == 200:
                image_name = f"{username}_profile.jpg"  # 파일 이름을 사용자 이름 기반으로 설정
                image_path = os.path.join(settings.MEDIA_ROOT, 'profile', image_name)
                
                # 이미지 파일 저장
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_response.content)

                # 이미지 경로를 user 모델에 저장
                profile_image = f"profile/{image_name}"
            else:
                profile_image = None
        else:
            profile_image = None

        # 기존 사용자 확인 또는 새 사용자 생성
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.nickname = nickname[:20]  # 닉네임은 20자로 제한
            user.profile_image = profile_image
            user.save()

            # KakaoUser 생성
            KakaoUser.objects.create(
                user=user,
                profile_nickname=nickname,
                profile_image=profile_image,
                # 생년월일 및 장르 정보는 사용자가 따로 입력하도록 처리
                # 예: user.birthdate = 생년월일 입력값, user.genre_1 = 장르 입력값 등
            )
        else:
            # 기존 사용자 정보 갱신
            user.nickname = nickname[:20]  # 닉네임은 20자로 제한
            user.profile_image = profile_image
            user.save()

            # KakaoUser 정보 갱신
            kakao_user = user.kakao_user
            kakao_user.profile_nickname = nickname
            kakao_user.profile_image = profile_image
            kakao_user.save()

    except Exception as e:
        messages.error(request, f"카카오 사용자 정보 가져오기 실패: {str(e)}")
        return redirect('movies:index')

    # 사용자 로그인 처리 (backend 명시)
    login(request, user, backend='social_core.backends.kakao.KakaoOAuth2')
    messages.success(request, "카카오 로그인 성공!")
    return redirect('movies:index')
