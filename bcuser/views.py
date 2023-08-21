from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django. views.generic.edit import FormView
from django.views import View
from .forms import *
from .models import *
from itertools import chain

from c_notice.models import *
from e_duo.models import *
from f_squad.models import *
from g_multi.models import *
from h_justchat.models import *
from i_qna.models import *
# Create your views here.
# def home(request) :
#     return render(request, 'home.html', {'email':request.session.get('user')})


# FormView : GET 또는 POST 요청을 처리해주는 비즈니스 로직 라이브러리
class RegisterView(FormView):
    template_name = 'register.html' # 사용할 템플릿 이름
    form_class = RegisterForm # 참고할 forms.py에 있는 클레스 즉 폼 클래스
    success_url='/login/' # Registerform이 성공적으로 처리된 후 리다이렉트될 URL을 작성

    def form_valid(self, form):
        bcuser = Bcuser(
            email = form.data.get('email'),
            nickname = form.data.get('nickname'),
            password = make_password(form.data.get('password')),
            level = 'user',
        )
        if Bcuser.objects.filter(email=form.data.get('email')).exists(): #User의 email객체들 중 form에 입력한 email과 같은 대상이 존재하면,
            form.add_error('email', '이미 사용 중인 이메일입니다.') # form에 email에러필드에 에러를 추가하라
            return self.form_invalid(form)
        if Bcuser.objects.filter(nickname=form.data.get('nickname')).exists(): #User의 email객체들 중 form에 입력한 email과 같은 대상이 존재하면,
            form.add_error('nickname', '이미 사용 중인 닉네임입니다.') # form에 email에러필드에 에러를 추가하라
            return self.form_invalid(form)

        else:
            bcuser.save()
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url='/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)
    
def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')

class Hometable(View):
    template_name = 'home.html'
    
    def get(self, request):
        DataA.objects.all().delete()  
        DataB.objects.all().delete()  
        DataC.objects.all().delete()  
        DataD.objects.all().delete()  # 모든 데이터 삭제

##########DataA   공지
        notices = c_Notice.objects.all().order_by('-c_register_date')[:5]
        for entry in notices: # 공지 게시판
            dt_entry = DataA.objects.create(
                board = "c_notice",
                origin = entry.id,
                category =entry.c_category,
                title=entry.c_title,
                click = entry.c_click,
                date = entry.c_register_date)
##########DataB    자유
        chats = h_Chat.objects.all().order_by('-h_register_date')[:5]
        qnas = i_Qna.objects.all().order_by('-i_register_date')[:5]
        for entry in chats: # 잡담 게시판
            dt_entry = DataB.objects.create(
                board = "h_chat",
                origin = entry.id,
                category =entry.h_category,
                title=entry.h_title,
                click = entry.h_click,
                date = entry.h_register_date)
        for entry in qnas: # 질문 게시판
            dt_entry = DataB.objects.create(
                board = "i_qna",
                origin = entry.id,
                category =entry.i_category,
                title=entry.i_title,
                click = entry.i_click,
                date = entry.i_register_date)
##########DataC   유저모으기
        duo = e_Duo.objects.all().order_by('-e_register_date')[:5]
        squad = f_Squad.objects.all().order_by('-f_register_date')[:5]
        multi = g_Multi.objects.all().order_by('-g_register_date')[:5]
        for entry in duo: # 듀오 게시판
            dt_entry = DataC.objects.create(
                board = "e_duo",
                origin = entry.id,
                category =entry.e_category,
                title=entry.e_title,
                click = entry.e_click,
                date = entry.e_register_date)
        for entry in squad: # 스쿼드 게시판
            dt_entry = DataC.objects.create(
                board = "f_squad",
                origin = entry.id,
                category =entry.f_category,
                title=entry.f_title,
                click = entry.f_click,
                date = entry.f_register_date)
        for entry in multi: # 멀티 게시판
            dt_entry = DataC.objects.create(
                board = "g_multi",
                origin = entry.id,
                category =entry.g_category,
                title=entry.g_title,
                click = entry.g_click,
                date = entry.g_register_date)
            
############DataD 중고거래 게시판
        # buys = buyProduct.objects.all().order_by('-h_register_date')[:5]
        # sells = i_Qna.objects.all().order_by('-i_register_date')[:5]
        # for entry in chats: # 잡담 게시판
        #     dt_entry = DataC.objects.create(
        #         board = "c_chat",
        #         origin = entry.id,
        #         category =entry.h_category,
        #         title=entry.h_title,
        #         click = entry.h_click,
        #         date = entry.h_register_date)
        # for entry in qnas: # 질문 게시판
        #     dt_entry = DataB.objects.create(
        #         board = "i_qna",
        #         origin = entry.id,
        #         category =entry.i_category,
        #         title=entry.i_title,
        #         click = entry.i_click,
        #         date = entry.i_register_date)
        
        
        
        dta = DataA.objects.all().order_by('-date')[:5]
        dtb = DataB.objects.all().order_by('-date')[:5]
        dtc = DataC.objects.all().order_by('-date')[:5]
        dtd = DataD.objects.all().order_by('-date')[:5]
        context = {
            'dta'  : dta,
            'dtb'  : dtb,
            'dtc'  : dtc,
            'dtd'  : dtd,
        }
        
        return render(request, self.template_name, context)