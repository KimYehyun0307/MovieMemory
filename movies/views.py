import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from reviews.models import Review
from accounts.forms import UserCreationForm  
from accounts.models import User
from django.core.files.storage import default_storage

from .models import Movie
from reviews.models import Review


def get_genres(genre_id):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}&language=ko'
    response = requests.get(url)
    return response.json().get('results', [])[:20]  # top 20 영화만 가져오기

def index(request):
    # 인기 영화 목록 (전체 top 20)
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=ko'
    response = requests.get(url)
    movies = response.json().get('results', [])
    
    # 인기 영화 순위 내림차순 정렬
    movies_sorted = sorted(movies, key=lambda x: x['popularity'], reverse=True)
    
    # 1위부터 20위까지 영화만 가져오기
    top_20_movies = movies_sorted[:20]
    
    # 순위를 매기기 위해 영화에 인덱스를 추가
    for idx, movie in enumerate(top_20_movies):
        movie['rank'] = idx + 1  # 순위 1위부터 시작

    # 5개씩 묶어서 처리
    grouped_movies = [top_20_movies[i:i + 5] for i in range(0, len(top_20_movies), 5)]

    # 장르별로 인기 영화 리스트 가져오기
    genre_urls = {
        '액션': 28,  # 액션
        '코미디': 35,  # 코미디
        '모험': 12,  # 모험
        '애니메이션': 16,  # 애니메이션
        '로맨스': 10749,  # 로맨스
        '공포': 27,  # 공포
        '드라마': 18,  # 드라마
        # 필요한 다른 장르 추가
    }
    
    genre_movies = {}
    for genre_name, genre_id in genre_urls.items():
        # get_genre 함수 호출하여 장르별 영화 리스트 가져오기
        genre_movies[genre_name] = get_genres(genre_id)

        # 장르별 영화에 순위를 매기기
        for idx, movie in enumerate(genre_movies[genre_name]):
            movie['rank'] = idx + 1  # 순위 1위부터 시작

        # 5개씩 묶어서 처리
        genre_movies[genre_name] = [genre_movies[genre_name][i:i + 5] for i in range(0, len(genre_movies[genre_name]), 5)]  # 장르별로 5개씩 묶음
    
    return render(request, 'movies/index.html', {
        'grouped_movies': grouped_movies,
        'genre_movies': genre_movies
    })


def genre(request, genre_name):

    # TMDB API에서 장르 ID와 해당 장르에 대한 영화 데이터를 가져오기
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={settings.TMDB_API_KEY}&language=ko"
    genre_response = requests.get(genre_url)
    genre_data = genre_response.json()

    genre_mapping = {genre['name']: genre['id'] for genre in genre_data['genres']}
    genre_id = genre_mapping.get(genre_name)

    if not genre_id:
        return render(request, 'movies/genre.html', {'error_message': f"'{genre_name}' 장르를 찾을 수 없습니다."})

    movies = get_genres(genre_id)

    sorted_movies = {
        '인기순': sorted(movies, key=lambda x: x['popularity'], reverse=True),
        '평점순': sorted(movies, key=lambda x: x['vote_average'], reverse=True),
        '최근 출시순': sorted(movies, key=lambda x: x['release_date'], reverse=True),
    }

    grouped_movies = {
        key: [sorted_movies[key][i:i + 5] for i in range(0, len(sorted_movies[key]), 5)]
        for key in sorted_movies
    }

    return render(request, 'movies/genre.html', {
        'genre_name': genre_name,
        'grouped_movies': grouped_movies,
        'genres': genre_data['genres'],  # 장르 데이터를 전달
    })


def detail(request, movie_id):
    # 특정 영화의 세부 정보 가져오기
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}&language=ko'
    response = requests.get(url)
    movie_data = response.json()

    # 트레일러 정보 가져오기
    trailer_url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={settings.TMDB_API_KEY}&language=ko'
    trailer_response = requests.get(trailer_url)
    trailers = trailer_response.json().get('results', [])

    # 가장 첫 번째 트레일러를 선택 (있을 경우)
    trailer = trailers[0] if trailers else None

    # DB에 저장된 해당 영화 정보를 가져옴 (영화 정보 없으면 생성 가능)
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': movie_data.get('title', ''),
            'overview': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', None),
            'poster_path': movie_data.get('poster_path', ''),
        }
    )

    # 영화에 대한 리뷰 가져오기
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')

    # 영화 세부 정보와 리뷰를 전달
    return render(request, 'movies/detail.html', {'movie': movie_data, 'reviews': reviews, 'trailer': trailer})


def search(request):
    query = request.GET.get('query', '').strip()  # 검색어 받기
    print(f"입력된 검색어: {query}")  # query 값 확인용

    if not query:
        # 검색어가 없을 때 메시지나 빈 리스트를 전달
        return render(request, 'movies/search.html', {'movies': [], 'message': '검색어를 입력해주세요.'})

    movies = []

    # 검색어가 있을 경우만 API 요청
    api_url = f'https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}&language=ko-KR'
    response = requests.get(api_url)

    data = response.json()

    movies = data.get('results', [])

    return render(request, 'movies/search.html', {'movies': movies})

@login_required
def profile(request, user_name):
    # user_name을 기준으로 해당 사용자 정보 가져오기
    user = get_object_or_404(User, username=user_name)  # user_name을 통해 해당 사용자 찾기

    # 카카오 계정 여부 확인
    has_kakao_account = SocialAccount.objects.filter(user=user, provider='kakao').exists()

    # 카카오 프로필 이미지 가져오기
    kakao_profile_image = None
    if has_kakao_account:
        social_account = SocialAccount.objects.get(user=user, provider='kakao')
        kakao_profile_image = social_account.get_avatar_url()  # 카카오 프로필 이미지 URL

    # 사용자가 작성한 리뷰 가져오기 (최근 작성한 순서대로)
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')

    # POST 요청 시 닉네임 및 프로필 이미지 수정
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        user.nickname = nickname

        # 프로필 이미지 수정
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            if user.profile_image:  # 기존 이미지가 있으면 삭제
                user.profile_image.delete()
            user.profile_image = profile_image  # 새 이미지 저장

        user.save()  # 변경 사항 저장
        return redirect('movies:profile', user_name=user.username)  # 수정 후 해당 사용자의 프로필 페이지로 리디렉션

    context = {
        'user': user,
        'has_kakao_account': has_kakao_account,
        'kakao_profile_image': kakao_profile_image,
        'user_reviews': user_reviews,  # 댓글 단 글 목록 전달
    }
    return render(request, 'movies/profile.html', context)


@login_required
def profile_edit(request, user_name):
    user = get_object_or_404(User, username=user_name)  # user_name을 통해 해당 사용자 찾기
    
    # 현재 로그인한 사용자가 아니라면 수정 불가
    if request.user != user:
        return redirect('movies:index')  # 접근을 제한하려면 다른 페이지로 리디렉션
    
    # kakao_로 시작하는 경우 비밀번호 수정 옵션을 사용하지 않도록 설정
    is_kakao_user = user.username.startswith('kakao_')

    if request.method == 'POST':
        # 닉네임 수정
        nickname = request.POST.get('nickname')
        user.nickname = nickname

        # 프로필 이미지 수정
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            if user.profile_image:  # 기존 이미지가 있으면 삭제
                user.profile_image.delete()
            user.profile_image = profile_image  # 새 이미지 저장

        # 비밀번호 수정
        if not is_kakao_user:
            password = request.POST.get('password')
            if password:
                user.set_password(password)

        user.save()  # 변경 사항 저장
        return redirect('movies:profile', user_name=user.username)  # 수정 후 해당 사용자의 프로필 페이지로 리디렉션

    context = {'user': user, 'is_kakao_user': is_kakao_user}
    return render(request, 'movies/profile_edit.html', context)

