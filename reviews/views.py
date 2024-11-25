from django.shortcuts import render
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from movies.models import Movie  # Movie 모델이 있다고 가정
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import Comment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Review, Comment
from django.contrib.auth.decorators import login_required
import json

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

def create_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST' and request.is_ajax():
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                review=review,
                user=request.user,
                content=content
            )
            return JsonResponse({'content': comment.content, 'username': comment.user.username, 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')}, status=200)
    return JsonResponse({'error': '댓글 작성 실패'}, status=400)


@login_required
def add_comment(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)
        
        # JSON 데이터에서 content 값을 가져옵니다.
        data = json.loads(request.body)
        content = data.get('content')  # JSON에서 'content'를 가져옵니다.

        if not content:
            return JsonResponse({'error': '댓글 내용을 입력하세요.'}, status=400)

        # 댓글 생성
        comment = Comment.objects.create(
            review=review,
            user=request.user,  # 현재 로그인한 사용자
            content=content,
        )
        
        return JsonResponse({
            'comment': {
                'id': comment.id,
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            }
        })

    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:  # 본인 댓글인지 확인
        comment.delete()
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'}, status=403)




