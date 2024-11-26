import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
import urllib.parse
from django.conf import settings
from reviews.models import Review
from accounts.forms import UserCreationForm  
from accounts.models import User
from communities.models import MovieReview, Comment, CommentReply
from django.core.files.storage import default_storage
from .models import Movie, Scrap
from .models import Genres
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
    genre_movies = {}  # 기본값
    show_genre_message = False  # 선호 장르 메시지를 표시할지 여부
    if request.user.is_authenticated:
        # 로그인한 사용자의 선호 장르 가져오기
        user = request.user
        favorite_genres = [user.genre_1, user.genre_2, user.genre_3]
        # 선호 장르가 하나도 설정되지 않은 경우 메시지 표시
        if not any(favorite_genres):  # 모든 장르가 None인 경우
            show_genre_message = True
        else:
            # 선호 장르별 인기 영화 리스트 가져오기
            for genre in favorite_genres:
                if genre:  # 장르가 설정된 경우에만 처리
                    genre_name = genre.name
                    genre_movies[genre_name] = get_genres(genre.id)
                    # 5개씩 묶어서 처리
                    genre_movies[genre_name] = [
                        genre_movies[genre_name][i:i + 5] 
                        for i in range(0, len(genre_movies[genre_name]), 5)
                    ]
    genres = Genres.objects.all()  # 모든 장르 데이터 로드
    return render(request, 'movies/index.html', {
        'grouped_movies': grouped_movies,
        'genre_movies': genre_movies,
        'genres': genres,
        'show_genre_message': show_genre_message,  # 메시지 여부 전달
    })

from datetime import datetime

# 각 API를 별도로 호출하는 함수
def get_popular_movies(genre_id):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc&language=ko'
    response = requests.get(url)
    return response.json().get('results', [])[:20]  # 인기순 20개 영화 반환

def get_top_rated_movies(genre_id):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}&sort_by=vote_average.desc&vote_count.gte=200&language=ko'
    response = requests.get(url)
    return response.json().get('results', [])[:20]  # 평점순 20개 영화 반환

def get_upcoming_movies(genre_id):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}&sort_by=release_date.desc&vote_count.gte=5&language=ko&release_date.lte=2024-11-25'
    response = requests.get(url)
    return response.json().get('results', [])[:20]


def genre(request, genre_id):
    # TMDB API에서 장르 ID와 해당 장르에 대한 영화 데이터를 가져오기
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={settings.TMDB_API_KEY}&language=ko"
    genre_response = requests.get(genre_url)
    genre_data = genre_response.json()

    # 장르 ID를 확인하여 해당 장르 이름을 찾기
    genre_mapping = {genre['id']: genre['name'] for genre in genre_data['genres']}
    genre_name = genre_mapping.get(genre_id)

    if not genre_name:
        return render(request, 'movies/genre.html', {'error_message': f"ID '{genre_id}'에 해당하는 장르를 찾을 수 없습니다."})

    # 각 기준에 따른 영화 데이터 호출
    movies_popularity = get_popular_movies(genre_id)  # 인기순
    movies_vote_average = get_top_rated_movies(genre_id)  # 평점순
    movies_release_date = get_upcoming_movies(genre_id)  # 최근 출시순

    # 각 정렬된 영화들을 5개씩 그룹화
    sorted_movies = {
        '인기순': movies_popularity,
        '평점순': movies_vote_average,
        '최근 출시순': movies_release_date,
    }
    
    # 각 정렬된 영화들을 5개씩 그룹화
    grouped_movies = {}
    for sort_type, movie_list in sorted_movies.items():
        grouped_movies[sort_type] = [movie_list[i:i + 5] for i in range(0, len(movie_list), 5)]

    return render(request, 'movies/genre.html', {
        'genre_name': genre_name,  # 장르 이름 전달
        'grouped_movies': grouped_movies,  # 영화 데이터를 그룹화하여 전달
        'genres': genre_data['genres'],  # TMDB에서 가져온 모든 장르 데이터를 전달
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
    
    # 스크랩 상태를 movie_data에 추가
    movie_data['is_scrapped'] = movie.is_scrapped

    # movie 인스턴스에 연결된 장르들을 가져오기
    genres = movie.genres.all()  # ManyToMany 관계로 연결된 장르들 가져오기

    # 영화에 대한 리뷰 가져오기
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')

    # 영화 세부 정보와 리뷰를 전달
    return render(request, 'movies/detail.html', {'movie': movie_data, 'reviews': reviews, 'trailer': trailer, 'genres': genres})






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

import random

def get_recommendations(user):
    TMDB_API_KEY = settings.TMDB_API_KEY
    recommendations = {}  # 장르별 추천 영화 저장
    favorite_genres = [user.genre_1, user.genre_2, user.genre_3]

    if not user.birthdate:
        return recommendations  # 생년 정보가 없으면 빈 추천 목록 반환

    # 생년 기준 필터링 범위
    start_year = user.birthdate.year
    end_year = start_year + 19

    for genre in favorite_genres:
        if genre:  # 선호 장르가 설정된 경우에만 처리
            genre_id = genre.id
            genre_name = genre.name

            # TMDB API 호출 (해당 장르 및 연도 범위, 평점 8점 이상)
            url = (
                f"https://api.themoviedb.org/3/discover/movie?"
                f"api_key={TMDB_API_KEY}&language=ko"
                f"&sort_by=vote_average.desc&vote_count.gte=100"
                f"&primary_release_date.gte={start_year}-01-01"
                f"&primary_release_date.lte={end_year}-12-31"
                f"&vote_average.gte=7"
                f"&with_genres={genre_id}"
            )
            response = requests.get(url).json()
            movies = response.get('results', [])

            # 랜덤으로 20개 선택
            if movies:
                recommendations[genre_name] = random.sample(movies, min(len(movies), 20))

    return recommendations

@login_required
def memory(request):
    # Memory 추천 로직
    genre_recommendations = get_recommendations(request.user)

    # 슬라이드 형식으로 묶기 (5개씩)
    grouped_recommendations = {
        genre: [movies[i:i + 5] for i in range(0, len(movies), 5)]
        for genre, movies in genre_recommendations.items()
    }

    genres = Genres.objects.all()  # 모든 장르 데이터 로드

    return render(request, 'movies/memory.html', {
        'grouped_recommendations': grouped_recommendations,
        'genres': genres
    })

def profile(request, user_nickname):
    user_nickname = urllib.parse.unquote(user_nickname)
    user = get_object_or_404(User, nickname=user_nickname)
    scrapped_movies = Scrap.objects.filter(user=user)
    has_kakao_account = SocialAccount.objects.filter(user=user, provider='kakao').exists()
    kakao_profile_image = (
        SocialAccount.objects.get(user=user, provider='kakao').get_avatar_url()
        if has_kakao_account else None
    )
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')
    user_posts = MovieReview.objects.filter(user=user).order_by('-created_at')
    user_comments = Comment.objects.filter(user=user)

    is_self = request.user == user  # 자신이 프로필을 보고 있는지 확인
    show_id = is_self or request.user.is_superuser # 프로필을 보는 사람이 자기 자신이거나 관리자일때만 id 공개
    show_birthdate = is_self or request.user.is_superuser or user.is_birthdate_public
    show_genre = is_self or request.user.is_superuser or user.is_genre_public
    show_reviews = is_self or request.user.is_superuser or user.is_reviews_public
    show_posts = is_self or request.user.is_superuser or user.is_post_public
    show_comments = is_self or request.user.is_superuser or user.is_comments_public

    # 비공개일 경우, 해당 목록을 비우기
    if not show_reviews:
        user_reviews = []
    if not show_posts:
        user_posts = []
    if not show_comments:
        user_comments = []

    context = {
        'user': user,
        'has_kakao_account': has_kakao_account,
        'kakao_profile_image': kakao_profile_image,
        'user_reviews': user_reviews,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'scrapped_movies': scrapped_movies,
        'show_id': show_id, 
        'show_birthdate': show_birthdate,
        'show_genre': show_genre,
        'show_reviews': show_reviews,
        'show_posts': show_posts,
        'show_comments': show_comments,  # 댓글 공개 여부를 템플릿에서 사용할 수 있도록 추가
    }

    return render(request, 'movies/profile.html', context)

@login_required
def profile_edit(request, user_nickname):
    user = get_object_or_404(User, nickname=user_nickname)
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
        user.is_birthdate_public = 'birthdate_visible' in request.POST
        user.is_genre_public = 'genres_visible' in request.POST
        user.is_reviews_public = 'reviews_visible' in request.POST

        # 영화 게시판 글 목록 공개 여부 업데이트
        user.is_post_public = 'posts_visible' in request.POST

        # 댓글 및 대댓글 공개 여부 업데이트
        user.is_comments_public = 'comments_visible' in request.POST

        user.save()
        return redirect('movies:profile', user_nickname=user.nickname)

    context = {
        'user': user,
        'is_kakao_user': is_kakao_user,
        'genres': Genre.objects.all(),
    }
    return render(request, 'movies/profile_edit.html', context)

from django.http import JsonResponse


@login_required
def scrap_toggle(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    
    # 기존에 스크랩된 상태가 있으면 삭제, 없으면 추가
    scrap, created = Scrap.objects.get_or_create(user=user, movie=movie)
    if created:
        # 새로 스크랩 추가
        is_scrapped = True
    else:
        # 기존 스크랩 취소
        scrap.delete()
        is_scrapped = False
    
    # movie 객체의 is_scrapped 상태를 갱신
    movie.is_scrapped = is_scrapped
    movie.save()

    return JsonResponse({'is_scrapped': is_scrapped})


