from django.shortcuts import render
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from movies.models import Movie  # Movie 모델이 있다고 가정
from django.conf import settings

def create_review(request, movie_id):
    # Movie 객체 가져오기 (없으면 생성)
    movie, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults=get_movie_data_from_tmdb(movie_id)
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_id=movie_id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'form': form, 'movie': movie})


def get_movie_data_from_tmdb(movie_id):
    """TMDB API에서 영화 데이터를 가져와 Movie 생성에 필요한 기본값 반환"""
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}&language=ko'
    response = requests.get(url)
    if response.status_code == 200:
        movie_data = response.json()
        return {
            'title': movie_data.get('title', '제목 없음'),
            'overview': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', None),
            'poster_path': movie_data.get('poster_path', ''),
        }
    else:
        raise Exception(f"TMDB에서 영화 데이터를 가져오는 데 실패했습니다. (ID: {movie_id})")


def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)  # 리뷰 가져오기
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            # 리뷰가 속한 영화의 상세 페이지로 리다이렉트
            return redirect('movies:detail', movie_id=review.movie.tmdb_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/update_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    movie_tmdb_id = review.movie.tmdb_id  # tmdb_id를 가져옴
    review.delete()
    return redirect('movies:detail', movie_id=movie_tmdb_id)

