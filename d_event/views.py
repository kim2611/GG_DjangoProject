from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
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

    all_infos = l_Info.objects.all().order_by("-l_register_date")
    try : 
        user = Bcuser.objects.get(email=request.session.get('user'))
    except:
        user = ''
    
    if category_filter and category_filter != '전체':
        all_infos = all_infos.filter(l_category=category_filter)

    if search_query:
        all_infos = all_infos.filter(l_title__icontains=search_query)
    
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_infos, 5)
    infos = paginator.get_page(page)

    form = ChatSearchForm(request.GET)
    
    context = {
        'infos': infos,
        'form': form,
        'user' : user,
    }

    return render(request, 'l_info_list.html', context)

###############################################################################

class BoardDeleteView(View):
    @method_decorator(admin_required)
    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        info = get_object_or_404(l_Info, pk=pk)
        
        if Bcuser.objects.get(email=request.session.get('user')) == info.l_writer:
            info.delete()
            return redirect('/info_board/')
        else:
            raise Http404('권한이 없습니다')


###############################################################################
def comment_delete(request,pk):
    if not request.session.get('user'):
        return redirect('/login/')
    comment = get_object_or_404(l_Comment, pk=pk)
    if comment.l_author == Bcuser.objects.get(email=request.session.get('user')):
        info_pk = comment.post.pk  # 코멘트가 속한 게시글의 pk 가져오기
        comment.delete()
        return redirect('info_board_detail', pk=info_pk)  # 게시글 상세 페이지로 리다이렉트
    else:
        raise Http404('권한이 없습니다')
    

def board_vote(request, pk):
    if not request.session.get('user'):
        return redirect('/login/')
    info = l_Info.objects.get(pk=pk)
    user = Bcuser.objects.get(email=request.session.get('user')) # 현재 로그인한 사용자
    
        # 중복 추천 확인
    if user in info.l_voters.all():
        info.l_votes -= 1  # 추천수 감소
        info.l_voters.remove(user)  # 사용자를 추천한 사용자 목록에서 제거
        is_upvoted = False # 추천 취소됨
    else:
        info.l_votes += 1  # 추천수 증가
        info.l_voters.add(user)  # 해당 사용자를 추천한 사용자 목록에 추가
        is_upvoted = True  # 추천됨
        
    info.save()
    return redirect('info_board_detail', pk=info.pk)


class Board_detail(FormView):
    template_name = 'l_info_detail.html'


    def get(self, request, pk):
        try:
            info = l_Info.objects.get(pk=pk)
        except l_Info.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        info.l_click += 1
        info.save()
        
        is_upvoted = False  # 기본값으로 초기화
        
        try:
            user = Bcuser.objects.get(email=request.session.get('user'))
            is_upvoted = user in info.l_voters.all()
        except Bcuser.DoesNotExist:
            user = ""

        comments = l_Comment.objects.filter(post=info)
        comment_form = CommentForm()
        
        context = {
            'info': info,
            'comment_form': comment_form,
            'comments': comments,
            'is_upvoted': is_upvoted,
            'voters' : info.l_voters.all(),
            'user' : user
        }
        
        return render(request, self.template_name, context)

    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        info = l_Info.objects.get(pk=pk)
        
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = info
                new_comment.author = Bcuser.objects.get(email=request.session.get('user'))
                new_comment.save()
                return redirect('info_board_detail', pk=info.pk)
        else:
            comment_form = CommentForm()

        context = {
            'info': info,
            'comment_form': comment_form,
        }
        
        return render(request, self.template_name, context)


####################################################################################################
# def board_update(request, pk):
#     if not request.session.get('user'):
#         return redirect('/login/')

#     try:
#         info = l_Info.objects.get(pk=pk)
#     except l_Info.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
#         raise Http404('게시글을 찾을 수 없습니다.')
#     if Bcuser.objects.get(email=request.session.get('user')) == info.l_writer:
#         if request.method == 'POST':
#             form = l_InfoForm(request.POST)
#             if form.is_valid():  # 폼이 유효한지
#                 user_id = request.session.get('user') # 세션에서 로그인한 아이디 확보
#                 info.l_category = form.cleaned_data['category']
#                 info.l_title = form.cleaned_data['title']
#                 info.l_contents = form.cleaned_data['contents']
#                 info.l_writer = Bcuser.objects.get(email=request.session.get('user'))
#                 info.l_nickname = Bcuser.objects.get(nickname=request.session.get('user'))
#                 info.save()
#                 return redirect('/info_board/')
#         else:
#             form = l_InfoForm(initial={'title':info.l_title, 'contents':info.l_contents, 'category':info.l_category})
#     else:
#         raise Http404('권한이 없습니다')
#     return render(request, 'l_info_update.html', {'form': form})

class BoardUpdateView(View):
    template_name = 'l_info_update.html'
    @method_decorator(admin_required)
    def get(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        try:
            info = l_Info.objects.get(pk=pk)
        except l_Info.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다.')
        
        if Bcuser.objects.get(email=request.session.get('user')) == info.l_writer:
            form = l_InfoForm(initial={'title': info.l_title, 'contents': info.l_contents, 'category': info.l_category})
            context = {'form': form}
            return render(request, self.template_name, context)
        else:
            raise Http404('권한이 없습니다')
    
    def post(self, request, pk):
        if not request.session.get('user'):
            return redirect('/login/')
        info = l_Info.objects.get(pk=pk)
        
        if Bcuser.objects.get(email=request.session.get('user')) == info.l_writer:
            form = l_InfoForm(request.POST)
            if form.is_valid():
                info.l_category = form.cleaned_data['category']
                info.l_title = form.cleaned_data['title']
                info.l_contents = form.cleaned_data['contents']
                info.save()
                return redirect('/info_board/')
            else:
                context = {'form': form}
                return render(request, self.template_name, context)
        else:
            raise Http404('권한이 없습니다')


####################################################################################################
class BoardWriteView(View):
    template_name = 'l_info_write.html'
    @method_decorator(admin_required)
    def get(self, request):
        if not request.session.get('user'):
            return redirect('/login/')
        
        form = l_InfoForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    @method_decorator(admin_required)
    def post(self, request):
        if not request.session.get('user'):
            return redirect('/login/')
        
        form = l_InfoForm(request.POST)
        if form.is_valid():
            info = l_Info()
            info.l_category = form.cleaned_data['category']
            info.l_title = form.cleaned_data['title']
            info.l_contents = form.cleaned_data['contents']
            info.l_writer = Bcuser.objects.get(email=request.session.get('user'))
            info.save()
            return redirect('/info_board/')
        else:
            context = {'form': form}
            return render(request, self.template_name, context)
