from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from bcuser.models import Bcuser
from django.core.paginator import Paginator
from django.db import models
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from bcuser.decorators import *
from django.views import View

def board_list(request):
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search_query')

    all_notices = c_Notice.objects.all().order_by("-c_register_date")
    try : 
        user = Bcuser.objects.get(email=request.session.get('user'))
    except:
        user = ''
    
    if category_filter and category_filter != '전체':
        all_notices = all_notices.filter(c_category=category_filter)

    if search_query:
        all_notices = all_notices.filter(c_title__icontains=search_query)
    
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_notices, 5)
    notices = paginator.get_page(page)

    form = ChatSearchForm(request.GET)
    
    context = {
        'notices': notices,
        'form': form,
        'user' : user,
    }

    return render(request, 'c_notice_list.html', context)

###############################################################################

class BoardDeleteView(View):
    @method_decorator(admin_required)
    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        notice = get_object_or_404(c_Notice, pk=pk)
        
        if Bcuser.objects.get(email=request.session.get('user')) == notice.c_writer:
            notice.delete()
            return redirect('/notice_board/')
        else:
            raise Http404('권한이 없습니다')


###############################################################################
def comment_delete(request,pk):
    if not request.session.get('user'):
        return redirect('/login/')
    comment = get_object_or_404(c_Comment, pk=pk)
    if comment.author == Bcuser.objects.get(email=request.session.get('user')):
        notice_pk = comment.post.pk  # 코멘트가 속한 게시글의 pk 가져오기
        comment.delete()
        return redirect('notice_board_detail', pk=notice_pk)  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
    

def board_vote(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    notice = c_Notice.objects.get(pk=pk)
    user = Bcuser.objects.get(email=request.session.get('user')) # 현재 로그인한 사용자
    
        # 중복 추천 확인
    if user in notice.c_voters.all():
        notice.c_votes -= 1  # 추천수 감소
        notice.c_voters.remove(user)  # 사용자를 추천한 사용자 목록에서 제거
        is_upvoted = False # 추천 취소됨
    else:
        notice.c_votes += 1  # 추천수 증가
        notice.c_voters.add(user)  # 해당 사용자를 추천한 사용자 목록에 추가
        is_upvoted = True  # 추천됨
        
    notice.save()
    return redirect('notice_board_detail', pk=notice.pk)


class Board_detail(FormView):
    template_name = 'c_notice_detail.html'


    def get(self, request, pk):
        try:
            notice = c_Notice.objects.get(pk=pk)
        except c_Notice.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        notice.c_click += 1
        notice.save()
        
        is_upvoted = False  # 기본값으로 초기화
        
        try:
            user = Bcuser.objects.get(email=request.session.get('user'))
            is_upvoted = user in notice.c_voters.all()
        except Bcuser.DoesNotExist:
            user = ""

        comments = c_Comment.objects.filter(post=notice)
        comment_form = CommentForm()
        
        context = {
            'notice': notice,
            'comment_form': comment_form,
            'comments': comments,
            'is_upvoted': is_upvoted,
            'voters' : notice.c_voters.all(),
            'user' : user
        }
        
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        notice = c_Notice.objects.get(pk=pk)
        
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = notice
                new_comment.author = Bcuser.objects.get(email=request.session.get('user'))
                new_comment.save()
                return redirect('notice_board_detail', pk=notice.pk)
        else:
            comment_form = CommentForm()

        context = {
            'notice': notice,
            'comment_form': comment_form,
        }
        
        return render(request, self.template_name, context)


####################################################################################################

class BoardUpdateView(View):
    template_name = 'c_notice_update.html'
    @method_decorator(admin_required)
    def get(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        try:
            notice = c_Notice.objects.get(pk=pk)
        except c_Notice.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        if Bcuser.objects.get(email=request.session.get('user')) == notice.c_writer:
            form = c_NoticeForm(initial={'title': notice.c_title, 'contents': notice.c_contents, 'category': notice.c_category})
            context = {'form': form}
            return render(request, self.template_name, context)
        else:
            raise Http404('권한이 없습니다')
    
    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        notice = c_Notice.objects.get(pk=pk)
        
        if Bcuser.objects.get(email=request.session.get('user')) == notice.c_writer:
            form = c_NoticeForm(request.POST)
            if form.is_valid():
                notice.c_category = form.cleaned_data['category']
                notice.c_title = form.cleaned_data['title']
                notice.c_contents = form.cleaned_data['contents']
                notice.save()
                return redirect('/notice_board/')
            else:
                context = {'form': form}
                return render(request, self.template_name, context)
        else:
            raise Http404('권한이 없습니다')


####################################################################################################
class BoardWriteView(View):
    template_name = 'c_notice_write.html'

    @method_decorator(admin_required)
    def get(self, request):
        if not request.session.get('user'):
            return redirect('/login/')
        
        form = c_NoticeForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    def post(self, request):
        if not request.session.get('user'):
            return redirect('/login/')
        
        form = c_NoticeForm(request.POST)
        if form.is_valid():
            notice = c_Notice()
            notice.c_category = form.cleaned_data['category']
            notice.c_title = form.cleaned_data['title']
            notice.c_contents = form.cleaned_data['contents']
            notice.c_writer = Bcuser.objects.get(email=request.session.get('user'))
            notice.save()
            return redirect('/notice_board/')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)
