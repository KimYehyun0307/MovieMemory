from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Movie, MovieReview, BambooPost, Event
from .forms import MovieReviewForm, CommentForm, BambooPostForm, EventParticipationForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
from movies.models import Movie
from django.shortcuts import render
from .models import ScreeningSchedule, Event, MovieReview, BambooPost
from django.db.models import Count

# 커뮤니티 메인 페이지
def main_community(request):
    screening_schedules = ScreeningSchedule.objects.all()

    # 진행 중인 이벤트 가져오기
    active_events = Event.objects.filter(is_active=True)

    # 인기 영화 리뷰
    popular_reviews = MovieReview.objects.annotate(like_count=Count('like_set')).order_by('-like_count')[:5]

    # 인기 대나무숲 게시물
    popular_bamboo_posts = BambooPost.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]

    context = {
        'screening_schedules': screening_schedules,
        'active_events': active_events,
        'popular_reviews': popular_reviews,
        'popular_bamboo_posts': popular_bamboo_posts,
    }

    return render(request, 'communities/main_community.html', context)


# 영화 게시판
def board(request, movie_title):
    movie = get_object_or_404(Movie, title=movie_title)
    reviews = MovieReview.objects.filter(movie=movie)

    context = {
      'movie': movie, 
      'reviews': reviews,
    }

    return render(request, 'communities/board.html', context)

# 영화 게시물 보기
def post(request, movie_title, post_num):
    review = get_object_or_404(MovieReview, pk=post_num)
    # 댓글 작성 폼
    comment_form = CommentForm()
    comments = review.comments.all()  # 해당 리뷰의 댓글

    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, 'communities/post.html', context)

# 영화 게시물 수정
@login_required
def post_edit(request, movie_title, post_num):
    review = get_object_or_404(MovieReview, pk=post_num)
    # 수정 권한 체크 (작성자 본인만 수정 가능)
    if review.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("권한이 없습니다.")
    
    if request.method == "POST":
        form = MovieReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('communities:board', movie_title=movie_title)
    else:
        form = MovieReviewForm(instance=review)

    context = {
        'form': form, 
        'review': review
    }
    return render(request, 'communities/post_edit.html', context)

# 영화 게시물 삭제
@login_required
def post_delete(request, movie_title, post_num):
    review = get_object_or_404(MovieReview, pk=post_num)
    # 삭제 권한 체크 (작성자 본인 또는 슈퍼유저만 삭제 가능)
    if review.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("권한이 없습니다.")
    
    review.delete()
    return redirect('communities:board', movie_title=movie_title)

# 대나무숲 게시판
def bamboo(request):
    bamboo_posts = BambooPost.objects.all()
    context = {
        'bamboo_posts': bamboo_posts,
    }
    return render(request, 'communities/bamboo.html', context)

# 대나무숲 게시물 보기
def bamboo_post(request, post_num):
    bamboo_post = get_object_or_404(BambooPost, pk=post_num)

    context = {
        'bamboo_post': bamboo_post,
    }
    return render(request, 'communities/bamboo_post.html', context)

# 대나무숲 게시물 수정
@login_required
def bamboo_post_edit(request, post_num):
    bamboo_post = get_object_or_404(BambooPost, pk=post_num)
    # 수정 권한 체크 (작성자 본인만 수정 가능)
    if bamboo_post.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("권한이 없습니다.")
    
    if request.method == "POST":
        form = BambooPostForm(request.POST, request.FILES, instance=bamboo_post)
        if form.is_valid():
            form.save()
            return redirect('communities:bamboo')
    else:
        form = BambooPostForm(instance=bamboo_post)

    context = {
        'form': form, 
        'bamboo_post': bamboo_post
    }
    return render(request, 'communities/bamboo_post_edit.html', context)

# 대나무숲 게시물 삭제
@login_required
def bamboo_post_delete(request, post_num):
    bamboo_post = get_object_or_404(BambooPost, pk=post_num)
    # 삭제 권한 체크 (작성자 본인 또는 슈퍼유저만 삭제 가능)
    if bamboo_post.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("권한이 없습니다.")
    
    bamboo_post.delete()
    return redirect('communities:bamboo')

# 이벤트 페이지
def event(request):
    events = Event.objects.filter(is_active=True)
    context = {
        'events': events,
    }
    return render(request, 'communities/event.html', context)

# 이벤트 섹션 페이지
def event_section(request, eventname):
    event = get_object_or_404(Event, name=eventname)
    # 이벤트 참여 폼
    participation_form = EventParticipationForm()
    context = {
        'event': event,
        'participation_form': participation_form
    }
    return render(request, 'communities/event_section.html', context)

# 이벤트 참여 처리
@login_required
def event_participation(request, eventname):
    event = get_object_or_404(Event, name=eventname)
    if request.method == 'POST':
        form = EventParticipationForm(request.POST)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.event = event
            participation.user = request.user  # 로그인한 사용자로 설정
            participation.save()
            return redirect('communities:event_section', eventname=event.name)
    else:
        form = EventParticipationForm()
    context = {
        'event': event,
        'participation_form': form,
    }
    return render(request, 'communities/event_section.html', context)
