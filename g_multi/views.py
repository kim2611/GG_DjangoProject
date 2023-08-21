from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import g_Multi, g_Comment
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

    all_multis = g_Multi.objects.all().order_by("-g_register_date")
    
    if category_filter and category_filter != '전체':
        all_multis = all_multis.filter(g_category=category_filter)

    if search_query:
        all_multis = all_multis.filter(g_title__icontains=search_query)
    
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_multis, 10)
    multis = paginator.get_page(page)

    form = ChatSearchForm(request.GET)
    
    context = {
        'multis': multis,
        'form': form,
    }

    return render(request, 'g_multi_list.html', context)

def board_write(request):
    # 세션영역에 id가 존재하지 않으면 로그인 하고 오도록 login.html페이지로 넘김(ok)
    if not request.session.get('user'):
        return redirect('/login/')

    if request.method == 'POST':
        form = g_MultiForm(request.POST)
        print(request.POST) 
        if form.is_valid():  # 폼이 유효한지(ok 빈값일때 에러메시지 확인)
            #user_id = request.session.get('user')  # 세션에서 로그인한 아이디 확보
            # 실제 데이터 베이스에서 로그인한 id 가져오기
            #bcuser = form.data.get('email')

            multi = g_Multi()  # 게시판의 객체 생성 : 유효성 검사가 통과된 데이터를 저장하기 위함
            multi.g_category = form.cleaned_data['category']
            multi.g_title = form.cleaned_data['title']
            multi.g_contents = form.cleaned_data['contents']
            multi.g_writer = Bcuser.objects.get(email=request.session.get('user')) # 로그인한 id 데이터베이스에 저장
            multi.g_need = form.cleaned_data['need']
            multi.save()

            return redirect('/multi_board/')
    else:
        form = g_MultiForm()  # 접속은 했으나 유효성 검사를 안했으므로 다시 유효성 검사부터 진행
    # 실패시 처음으로 돌아가서 다시해봐
    return render(request, 'g_multi_write.html', {'form': form})


def board_delete(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    multi = get_object_or_404(g_Multi, pk=pk)

    # 로그인한 사용자와 채팅 메시지 작성자가 같은지 확인
    if Bcuser.objects.get(email=request.session.get('user')) == multi.g_writer:
        multi.delete()
        return redirect('/multi_board/')  # 채팅 목록 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
    
#######################
def comment_delete(request,pk):
    if not request.session.get('user'):
        return redirect('/login/')
    comment = get_object_or_404(g_Comment, pk=pk)
    if comment.author == Bcuser.objects.get(email=request.session.get('user')):
        multi_pk = comment.post.pk  # 코멘트가 속한 게시글의 pk 가져오기
        comment.delete()
        return redirect('multi_board_detail', pk=multi_pk)  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
    

def board_vote(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    multi = g_Multi.objects.get(pk=pk)
    user = Bcuser.objects.get(email=request.session.get('user')) # 현재 로그인한 사용자
    
        # 중복 추천 확인
    if user in multi.g_voters.all():
        multi.g_votes -= 1  # 추천수 감소
        multi.g_voters.remove(user)  # 사용자를 추천한 사용자 목록에서 제거
        is_upvoted = False # 추천 취소됨
    else:
        multi.g_votes += 1  # 추천수 증가
        multi.g_voters.add(user)  # 해당 사용자를 추천한 사용자 목록에 추가
        is_upvoted = True  # 추천됨
        
    multi.save()
    return redirect('multi_board_detail', pk=multi.pk)

class Board_detail(FormView):
    template_name = 'g_multi_detail.html'
    
    def get(self, request, pk):
        try:
            multi = g_Multi.objects.get(pk=pk)
        except g_Multi.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        multi.g_click += 1
        multi.save()
        
        is_upvoted = False  # 기본값으로 초기화
        
        try:
            user = Bcuser.objects.get(email=request.session.get('user'))
            is_upvoted = user in multi.g_voters.all()
        except Bcuser.DoesNotExist:
            user = ""

            
        comments = g_Comment.objects.filter(post=multi)
        comment_form = CommentForm()
        
        context = {
            'multi': multi,
            'comment_form': comment_form,
            'comments': comments,
            'is_upvoted': is_upvoted,
            'voters': multi.g_voters.all(),
            'user' : user
        }
            
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        multi = g_Multi.objects.get(pk=pk)
        
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = multi
                new_comment.author = Bcuser.objects.get(email=request.session.get('user'))
                new_comment.save()
                return redirect('multi_board_detail', pk=multi.pk)
        else:
            comment_form = CommentForm()

        context = {
            'multi': multi,
            'comment_form': comment_form,
        }
        
        return render(request, self.template_name, context)

def board_update(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')

    try:
        multi = g_Multi.objects.get(pk=pk)
    except g_Multi.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
        raise Http404('게시글을 찾을 수 없습니다.')

    if Bcuser.objects.get(email=request.session.get('user')) == multi.g_writer:
        if request.method == 'POST':
            form = g_MultiForm(request.POST)
            if form.is_valid():  # 폼이 유효한지
                multi.g_category = form.cleaned_data['category']
                multi.g_title = form.cleaned_data['title']
                multi.g_contents = form.cleaned_data['contents']
                multi.g_writer = Bcuser.objects.get(email=request.session.get('user'))
                multi.g_need = form.cleaned_data['need']
                
                multi.save()
                return redirect('/multi_board/')
        else:
            form = g_MultiForm(initial={'title':multi.g_title, 'contents':multi.g_contents, 'category':multi.g_category, 'need':multi.g_need})
        return render(request, 'g_multi_update.html', {'form': form})
    else:
        raise Http404('권한이 없습니다')

