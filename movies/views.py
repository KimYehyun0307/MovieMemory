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
from accounts.models import Genre


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

def profile(request, user_name):
    user = get_object_or_404(User, username=user_name)

    has_kakao_account = SocialAccount.objects.filter(user=user, provider='kakao').exists()
    kakao_profile_image = (
        SocialAccount.objects.get(user=user, provider='kakao').get_avatar_url()
        if has_kakao_account else None
    )

    user_reviews = Review.objects.filter(user=user).order_by('-created_at')

    # 프로필 공개 범위 확인
    is_self = request.user == user  # 자신이 프로필을 보고 있는지 확인
    show_nickname = is_self or request.user.is_superuser or user.is_nickname_public
    show_birthdate = is_self or request.user.is_superuser or user.is_birthdate_public
    show_genre = is_self or request.user.is_superuser or user.is_genre_public

    # 리뷰 공개 범위 확인
    show_reviews = is_self or request.user.is_superuser or user.is_reviews_public

    # 리뷰 공개 범위가 비공개인 경우, 주인과 슈퍼유저만 볼 수 있도록 설정
    if not show_reviews:
        user_reviews = []  # 비공개이면 리뷰는 빈 리스트로 설정

    context = {
        'user': user,
        'has_kakao_account': has_kakao_account,
        'kakao_profile_image': kakao_profile_image,
        'user_reviews': user_reviews,
        'show_nickname': show_nickname,
        'show_birthdate': show_birthdate,
        'show_genre': show_genre,
        'show_reviews': show_reviews,  # 리뷰 공개 여부를 템플릿에서 사용할 수 있도록 추가
    }
    return render(request, 'movies/profile.html', context)




@login_required
def profile_edit(request, user_name):
    user = get_object_or_404(User, username=user_name)
    if request.user != user:
        return redirect('movies:index')

    is_kakao_user = user.username.startswith('kakao_')

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        user.nickname = nickname

        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
            if user.profile_image:
                user.profile_image.delete()
            user.profile_image = profile_image

        # 생년월일 최초 설정
        if not user.birthdate:
            birthdate = request.POST.get('birthdate')
            if birthdate:
                user.birthdate = birthdate

        # 좋아하는 장르 설정
        genre_1 = request.POST.get('genre_1')
        genre_2 = request.POST.get('genre_2')
        genre_3 = request.POST.get('genre_3')

        if genre_1:
            user.genre_1 = Genre.objects.get(id=genre_1)
        if genre_2:
            user.genre_2 = Genre.objects.get(id=genre_2)
        if genre_3:
            user.genre_3 = Genre.objects.get(id=genre_3)

        # 비밀번호 변경
        if not is_kakao_user:
            password = request.POST.get('password')
            if password:
                user.set_password(password)

        # 프로필 공개 범위 업데이트
        user.is_nickname_public = 'nickname_visible' in request.POST
        user.is_birthdate_public = 'birthdate_visible' in request.POST
        user.is_genre_public = 'genres_visible' in request.POST
        user.is_reviews_public = 'reviews_visible' in request.POST

        user.save()
        return redirect('movies:profile', user_name=user.username)

    context = {
        'user': user,
        'is_kakao_user': is_kakao_user,
        'genres': Genre.objects.all(),
    }
    return render(request, 'movies/profile_edit.html', context)

