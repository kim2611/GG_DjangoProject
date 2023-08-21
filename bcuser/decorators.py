from django.shortcuts import redirect
from .models import Bcuser
from django.http import HttpResponse
def login_required(function) :
    def wrap(request, *args, **kwargs) :
        user = request.session.get('user')
        if user is None or not user : # 로그인을 하지 않은 상태
            return redirect('/login')
        # 로그인 상태라면 원래의 함수를 호출하고 결과값 반환
        return function(request, *args, **kwargs)
    return wrap # @login_required함수는 wrap를 반환 ->@login_required


def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:  # 로그인을 하지 않은 상태
            return redirect('/login')
        user = Bcuser.objects.get(email=user)
        if user.level != 'admin':
            response = HttpResponse()
            response.status_code = 403  # Forbidden
            response.content = '''
                <p>권한이 없습니다. 5초 후 이전 페이지로 이동합니다.</p>
                <script>
                    setTimeout(function() {
                        history.back();
                    }, 5000);
                </script>
            '''
            return response
        # 로그인 상태라면 원래의 함수를 호출하고 결과값 반환
        return function(request, *args, **kwargs)
    return wrap  # @login_required함수는 wrap를 반환 ->@login_required
# def admin_required(function) :
#     def wrap(request, *args, **kwargs) :
#         user = request.session.get('user')
#         if user is None or not user : # 로그인을 하지 않은 상태
#             return redirect('/login')
#         user = Bcuser.objects.get(email=user)
#         if user.level != 'admin' :
#             return redirect('/')
#         # 로그인 상태라면 원래의 함수를 호출하고 결과값 반환
#         return function(request, *args, **kwargs)
#     return wrap # @login_required 함수는 wrap를 반환 ->@login_required