from django.shortcuts import render, redirect
from django.http import Http404
# from .models import Board
# from .forms import BoardForm
from bcuser.models import Bcuser
from django.core.paginator import Paginator
# from tag.models import Tag


# def board_list(request):
#     all_boards=Board.objects.all().order_by("-id")
#     page=int(request.GET.get('p',1)) # 초기에 페이지는 1로 시작
#     paginator=Paginator(all_boards,3) # 전체 글을 가져와서 5개씩 나누어 보여줌

#     boards=paginator.get_page(page)
#     return render(request, 'board_list.html',{'boards' : boards})



# from django.shortcuts import render
# from .forms import YourForm  # YourForm은 폼 클래스의 이름입니다

# def your_view_function(request):
#     if request.method == 'POST':
#         form = YourForm(request.POST)
#         if form.is_valid():
#             # 폼이 유효할 때 처리 로직
#             # form.cleaned_data를 사용하여 폼 데이터에 접근 가능
#             age = form.cleaned_data['age']
#             gender = form.cleaned_data['gender']
#             # 추가로 처리할 내용 작성

#     else:
#         form = YourForm()

#     return render(request, 'mypage_write.html', {'form': form})