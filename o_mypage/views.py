from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import MypageUpdate
# from .forms import MypageForm
# from .forms import TagForm
from bcuser.models import Bcuser
from django.core.paginator import Paginator
# from p_tag.models import Tag
from .models import Mypage
from django.http import JsonResponse


def mypage_main(request):
    # 가장 최근에 작성한 글 한 개만 가져오기
    user = Bcuser.objects.get(email=request.session.get('user'))
    latest_mypage = Mypage.objects.filter(writer=user).order_by('-id').first()
    return render(request, 'mypage_main.html', {'latest_mypage': latest_mypage})



def mypage_write(request):
    if not request.session.get('user'):
        return redirect('/login/')
    
    if request.method == 'POST':
        # form = MypageUpdate(request.POST)
        form = MypageUpdate(request.POST)
        if form.is_valid():
            mypage = Mypage()
            mypage.age = form.cleaned_data['age']
            mypage.gender = form.cleaned_data['gender']
            mypage.voice = form.cleaned_data['voice']
            mypage.introduction = form.cleaned_data['introduction']
            # mypage.image = form.cleaned_data['image']
            mypage.writer = Bcuser.objects.get(email=request.session.get('user')) # 로그인한 id 데이터베이스에 저
            # mypage.writer = Bcuser.objects.get(email=request.user.email)
            mypage.save()

            return redirect('/mypage/main/')
    else:
        form = MypageUpdate()

    return render(request, 'mypage_write.html', {'form': form})


def mypage_detail(request, writer_id):
    latest_mypage = Mypage.objects.filter(writer_id=writer_id).order_by('-id').first()
    return render(request, 'mypage_detail.html', {'latest_mypage': latest_mypage})