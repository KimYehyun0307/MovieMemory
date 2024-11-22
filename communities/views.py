from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Movie, MovieReview, BambooPost, Event
from .forms import MovieReviewForm, CommentForm, BambooPostForm, EventParticipationForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
from movies.models import Movie
from .models import ScreeningSchedule, Event, MovieReview, BambooPost
from collections import defaultdict
from django.db.models import Count
from datetime import datetime
import calendar
from django.core.paginator import Paginator

def main_community(request):
    # 현재 날짜 가져오기
    today = datetime.today()
    current_year = today.year  # 현재 연도
    current_month = today.month  # 현재 월
    current_day = today.day  # 현재 일

    # 상영 예정 영화 데이터를 날짜별로 가져오기 (이미 DB에 저장된 데이터 사용)
    upcoming_schedules = ScreeningSchedule.objects.all().order_by('screening_date')

    grouped_schedules = defaultdict(set)  # 중복 제거를 위해 set 사용
    for schedule in upcoming_schedules:
        formatted_date = schedule.screening_date.strftime('%Y-%m-%d')
        grouped_schedules[formatted_date].add(schedule.movie_title)

    # set을 다시 list로 변환 (템플릿에서 반복 가능하도록)
    grouped_schedules = {date: list(titles) for date, titles in grouped_schedules.items()}

    # 주별로 나누어진 날짜 생성 (달력 데이터)
    calendar_instance = calendar.Calendar()
    weeks_in_month = list(calendar_instance.monthdatescalendar(current_year, current_month))

    # 각 날짜에 해당하는 "몇 주차"인지 계산
    week_info = {}  # 날짜별 몇 주차 정보를 저장
    for week_index, week in enumerate(weeks_in_month, start=1):  # 주차는 1부터 시작
        for day in week:
            if day.month == current_month:  # 현재 월의 날짜만 저장
                formatted_day = day.strftime('%Y-%m-%d')
                week_info[formatted_day] = week_index

    # 진행 중인 이벤트 가져오기
    active_events = Event.objects.filter(is_active=True)

    # 인기 영화 리뷰
    popular_reviews = MovieReview.objects.annotate(like_count=Count('like_set')).order_by('-like_count')[:5]

    # 인기 대나무숲 게시물
    popular_bamboo_posts = BambooPost.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]

    # Context에 데이터 추가
    context = {
        'grouped_schedules': grouped_schedules,  # 날짜별 영화 목록
        'week_info': week_info,  # 날짜별 몇 주차 정보
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day,
        'weeks_in_month': weeks_in_month,  # 주별로 나누어진 날짜들
        'active_events': active_events,
        'popular_reviews': popular_reviews,
        'popular_bamboo_posts': popular_bamboo_posts,
    }

    return render(request, 'communities/main_community.html', context)


# 영화 게시판
def board(request, movie_title):
    movie = get_object_or_404(Movie, title=movie_title)
    # 인기 글 5개 (좋아요 많은 순으로)
    popular_reviews = MovieReview.objects.filter(movie=movie).order_by('-likes')[:5]

    # 영화 후기 15개씩 페이지네이션
    reviews = MovieReview.objects.filter(movie=movie).order_by('-created_at')
    paginator = Paginator(reviews, 15)
    page_number = request.GET.get('page')
    reviews_page = paginator.get_page(page_number)

    context = {
        'movie': movie,
        'popular_reviews': popular_reviews,
        'reviews': reviews_page
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
def post_edit(request, movie_title, post_num=None):
    # post_num이 None이면 새 게시물 작성, 아니면 기존 게시물 수정
    if post_num:
        review = get_object_or_404(MovieReview, pk=post_num)
        # 수정 권한 체크 (작성자 본인만 수정 가능)
        if review.user != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("권한이 없습니다.")
    else:
        review = None  # 새 게시물 작성

    if request.method == "POST":
        form = MovieReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            # 새 게시물인 경우
            if not review:
                new_review = form.save(commit=False)
                new_review.user = request.user  # 새 게시물 작성자 설정
                new_review.movie_title = movie_title  # 영화 제목 설정
                new_review.save()
            else:
                form.save()  # 기존 게시물 수정

            return redirect('communities:movieboard', movie_title=movie_title)
    else:
        form = MovieReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'movie_title': movie_title,
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
    return redirect('communities:movieboard', movie_title=movie_title)

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
