from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import h_Chat
from .forms import h_ChatForm
from bcuser.models import Bcuser
from django.core.paginator import Paginator
# Create your views here.


def chat_list(request):
    all_chats = h_Chat.objects.all().order_by("-id")
    page = int(request.GET.get('p', 1))  # 초기에 페이지는 1로 시작
    paginator = Paginator(all_chats, 10)  # 전체 글을 가져와서 4개씩 나누어 보여줌

    chats = paginator.get_page(page)
    return render(request, 'h_chat_list.html', {'chats': chats})


def board_write(request):
    # 세션영역에 id가 존재하지 않으면 로그인 하고 오도록 login.html페이지로 넘김(ok)
    if not request.session.get('user'):
        return redirect('/login/')

    if request.method == 'POST':
        form = h_ChatForm(request.POST)
        print(request.POST) 
        if form.is_valid():  # 폼이 유효한지(ok 빈값일때 에러메시지 확인)
            #user_id = request.session.get('user')  # 세션에서 로그인한 아이디 확보
            # 실제 데이터 베이스에서 로그인한 id 가져오기
            #bcuser = form.data.get('email')

            chat = h_Chat()  # 게시판의 객체 생성 : 유효성 검사가 통과된 데이터를 저장하기 위함
            chat.h_title = form.cleaned_data['title']
            chat.h_contents = form.cleaned_data['contents']
            chat.h_writer = Bcuser.objects.get(email=request.session.get('user')) # 로그인한 id 데이터베이스에 저장
            chat.save()

            return redirect('/')
    else:
        form = h_ChatForm()  # 접속은 했으나 유효성 검사를 안했으므로 다시 유효성 검사부터 진행
    # 실패시 처음으로 돌아가서 다시해봐
    return render(request, 'h_chat_write.html', {'form': form})


def board_detail(request, pk):
    try:
        chat = h_Chat.objects.get(pk=pk)
    except h_Chat.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
        raise Http404('게시글을 찾을 수 없습니다.')

    return render(request, 'h_chat_detail.html', {'chat': chat})

# def board_update(request, pk):
#     if not request.session.get('user'):
#         return redirect('/bcuser/login/')
    
#     try:
#         board = Board.objects.get(pk=pk)
#     except Board.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
#         raise Http404('게시글을 찾을 수 없습니다.')
    
#     if request.method == 'POST':
#         form = BoardForm(request.POST)
#         if form.is_valid():  # 폼이 유효한지
#             user_id = request.session.get('user')  # 세션에서 로그인한 아이디 확보
#             bcuser = Bcuser.objects.get(pk=user_id)

#             board.title = form.cleaned_data['title']
#             board.contents = form.cleaned_data['contents']
#             board.writer = bcuser  # 글 작성자
#             board.save()

#             return redirect('/board/list/')
#     else:
#         form = BoardForm(initial={'title':board.title, 'contents':board.contents})  
#     return render(request, 'board_update.html', {'form': form})

# def board_delete(request, pk):
#     user_id = request.session.get('user')
    
#     if not request.session.get('user'):
#         return redirect('/bcuser/login/')
    
#     board = Board.objects.get(pk=pk)
#     if Bcuser.objects.get(pk=user_id) == board.writer:
#         board.delete()
#     else:
#         raise Http404('권한이 없습니다')
#     return redirect('board_list')
