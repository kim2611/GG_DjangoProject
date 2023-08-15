from django.shortcuts import render
from django.views import View
# from l_info.models import /예시로 Info 사용/ 게임정보 게시판에서 찜 누르면, 그게 마이페이지로 넘어와야하니
# l_info에서 models 만들고 받아오기.

class MypageGame(View):
    pass
    # def get(self, request, *args, **kwargs):
        # games = Info.objects.all() # Info 만들고 주석 제거
        # return render(request, 'game_list.html', {'games': games})



class MypageWrite(View):
    pass

class MypageUpdate(View):
    pass
