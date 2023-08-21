from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import f_Squad, f_Comment
from .forms import *
from bcuser.models import Bcuser
from django.core.paginator import Paginator
from django.db import models
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from bcuser.decorators import login_required

def board_list(request):
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search_query')

    all_squads = f_Squad.objects.all().order_by("-f_register_date")
    
    if category_filter and category_filter != '전체':
        all_squads = all_squads.filter(f_category=category_filter)

    if search_query:
        all_squads = all_squads.filter(f_title__icontains=search_query)
    
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_squads, 10)
    squads = paginator.get_page(page)

    form = ChatSearchForm(request.GET)
    
    context = {
        'squads': squads,
        'form': form,
    }

    return render(request, 'f_squad_list.html', context)

def board_write(request):
    # 세션영역에 id가 존재하지 않으면 로그인 하고 오도록 login.html페이지로 넘김(ok)
    if not request.session.get('user'):
        return redirect('/login/')

    if request.method == 'POST':
        form = f_SquadForm(request.POST)
        print(request.POST) 
        if form.is_valid():  # 폼이 유효한지(ok 빈값일때 에러메시지 확인)
            #user_id = request.session.get('user')  # 세션에서 로그인한 아이디 확보
            # 실제 데이터 베이스에서 로그인한 id 가져오기
            #bcuser = form.data.get('email')

            squad = f_Squad()  # 게시판의 객체 생성 : 유효성 검사가 통과된 데이터를 저장하기 위함
            squad.f_category = form.cleaned_data['category']
            squad.f_title = form.cleaned_data['title']
            squad.f_contents = form.cleaned_data['contents']
            squad.f_writer = Bcuser.objects.get(email=request.session.get('user')) # 로그인한 id 데이터베이스에 저장
            squad.f_need = form.cleaned_data['need']
            squad.save()

            return redirect('/squad_board/')
    else:
        form = f_SquadForm()  # 접속은 했으나 유효성 검사를 안했으므로 다시 유효성 검사부터 진행
    # 실패시 처음으로 돌아가서 다시해봐
    return render(request, 'f_squad_write.html', {'form': form})


def board_delete(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    squad = get_object_or_404(f_Squad, pk=pk)

    # 로그인한 사용자와 채팅 메시지 작성자가 같은지 확인
    if Bcuser.objects.get(email=request.session.get('user')) == squad.f_writer:
        squad.delete()
        return redirect('/squad_board/')  # 채팅 목록 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
    
#######################
def comment_delete(request,pk):
    if not request.session.get('user'):
        return redirect('/login/')
    comment = get_object_or_404(f_Comment, pk=pk)
    if comment.author == Bcuser.objects.get(email=request.session.get('user')):
        squad_pk = comment.post.pk  # 코멘트가 속한 게시글의 pk 가져오기
        comment.delete()
        return redirect('squad_board_detail', pk=squad_pk)  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
    

def board_vote(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    squad = f_Squad.objects.get(pk=pk)
    user = Bcuser.objects.get(email=request.session.get('user')) # 현재 로그인한 사용자
    
        # 중복 추천 확인
    if user in squad.f_voters.all():
        squad.f_votes -= 1  # 추천수 감소
        squad.f_voters.remove(user)  # 사용자를 추천한 사용자 목록에서 제거
        is_upvoted = False # 추천 취소됨
    else:
        squad.f_votes += 1  # 추천수 증가
        squad.f_voters.add(user)  # 해당 사용자를 추천한 사용자 목록에 추가
        is_upvoted = True  # 추천됨
        
    squad.save()
    return redirect('squad_board_detail', pk=squad.pk)

class Board_detail(FormView):
    template_name = 'f_squad_detail.html'
    
    def get(self, request, pk):
        try:
            squad = f_Squad.objects.get(pk=pk)
        except f_Squad.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        squad.f_click += 1
        squad.save()
        
        is_upvoted = False  # 기본값으로 초기화
        
        try:
            user = Bcuser.objects.get(email=request.session.get('user'))
            is_upvoted = user in squad.f_voters.all()
        except Bcuser.DoesNotExist:
            user = ""

            
        comments = f_Comment.objects.filter(post=squad)
        comment_form = CommentForm()
        
        
        context = {
            'squad': squad,
            'comment_form': comment_form,
            'comments': comments,
            'is_upvoted': is_upvoted,
            'voters': squad.f_voters.all(),
            'user' : user
        }
            
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        squad = f_Squad.objects.get(pk=pk)
        
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = squad
                new_comment.author = Bcuser.objects.get(email=request.session.get('user'))
                new_comment.save()
                return redirect('squad_board_detail', pk=squad.pk)
        else:
            comment_form = CommentForm()

        context = {
            'squad': squad,
            'comment_form': comment_form,
        }
        
        return render(request, self.template_name, context)

def board_update(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')

    try:
        squad = f_Squad.objects.get(pk=pk)
    except f_Squad.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
        raise Http404('게시글을 찾을 수 없습니다.')

    if Bcuser.objects.get(email=request.session.get('user')) == squad.f_writer:
        if request.method == 'POST':
            form = f_SquadForm(request.POST)
            if form.is_valid():  # 폼이 유효한지
                squad.f_category = form.cleaned_data['category']
                squad.f_title = form.cleaned_data['title']
                squad.f_contents = form.cleaned_data['contents']
                squad.f_writer = Bcuser.objects.get(email=request.session.get('user'))
                squad.f_need = form.cleaned_data['need']
                
                squad.save()
                return redirect('/squad_board/')
        else:
            form = f_SquadForm(initial={'title':squad.f_title, 'contents':squad.f_contents, 'category':squad.f_category, 'need':squad.f_need})
        return render(request, 'f_squad_update.html', {'form': form})
    else:
        raise Http404('권한이 없습니다')

