from django.shortcuts import render, redirect
from .models import c_Board
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .forms import c_BoardForm
# Create your views here.
from django.utils.decorators import method_decorator
from bcuser.decorators import admin_required
from bcuser.models import *

# from .serializers import ProductSerializer
from rest_framework import mixins, generics
# ListView : ListView를 사용하면 데이터 베이스에서 목록을 가져와서 
# 템플릿에 어떤 데이터 타입이든 쉽게 전달하는 작업을 수행해줌

class c_BoradList(ListView):
    model = c_Board
    template_name = 'c_board_list.html'
    context_object_name='c_board_list'
    paginate_by=10 # 한페이지에 최대 10개의 표시
    
# @method_decorator(admin_required, name='dispatch')
# class c_BoardCreate(FormView):
#     template_name='c_board_write.html'
#     form_class=RegisterForm
#     success_url='/notice_board/'
#     def form_valid(self, form):
#         board = c_Board(
#             title = form.data.get('title'),
#             contents = form.data.get('contents'),
#             # writer = form.data.get('writer'),
#             # tags = form.data.get('tags'),
#         )
#         board.save()
#         return super().form_valid(form)

def c_board_write(request):
# 세션영역에 id가 존재하지 않으면 로그인 하고 오도록 login.html페이지로 넘긴
    if not request.session.get("user"):
        return redirect("/login/")
    
    if request.method == "POST":
        form = c_BoardForm(request.POST)
        if form.is_valid(): # 폼의 데이터가 유효한 정보인지 여부
            user_id = request.session.get("user") # 세션에서 로그인한 아이디 확보
            bcuser = Bcuser.objects.get(pk=user_id) # 실제 데이터 베이스에서 로그인한 id 가져오기

            # tags = form.cleaned_data["tags"].split(",")

            board = c_Board() # 게시판의 객체 생성 : 유효성 검사가 통과된 데이터를 저장하기 위함
            board.title = form.cleaned_data["title"]
            board.contents = form.cleaned_data["contents"]
            board.writer = bcuser # 로그인한 id 데이터베이스에 저장
            board.save()

        # for tag in tags:
        #     if not tag: # 태그가 없을면 통과
        #         continue
        # # _tag, _ : 등록되어 있는 태그와 새로 생성한 태그 저장
        #     _tag, _ = Tag.objects.get_or_create(name=tag)
        #     board.tags.add(_tag) # 태그에 저장

            return redirect("/notice_board/")
    else:
        form = c_BoardForm() # 접속은 했으나 유효성 검사를 안했으므로 다시 유효성 검사부터 진행
    # 실패시 처음으로 돌아가 => 다시 해봐
    return render(request, "c_board_write.html", {"form": form})
        
class c_BoardDetail(DetailView):
    queryset = c_Board.objects.all()
    context_object_name = 'board'
    template_name = 'c_board_detail.html'
    

# GenericAPIView : RestFulAPI의 기본 동작을 제공
# ListModelMixin : views에서 필요로하는 메서드를 제공(여기에서는 list)
# class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin) :
#     serializer_class = ProductSerializer 
#     # RestFulAPI 타입으로 Product데이터베이스 변환
#     # serializer_class : Product데이터를 JSON 형태로 반환
    
#     def get_queryset(self):
#         # select * from Product where id=1;
#         # Product의 모든 데이터를 id로 정렬하여 반환하라
#         return Product.objects.all().order_by('id')
    
#     def get(self, request, *args, **kwargs) :
#         # list() : ListModelMixin에서 제공
#         return self.list(request, *args, **kwargs)
    
# # RetrieveModelMixin의 retrive() : DRF를 사용하여 특정데이터의 상세정보를 제공하는 API Views
# # RetrieveModelMixin
# class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
#     serializer_class = ProductSerializer 

#     def get_queryset(self):
#         return Product.objects.all().order_by('id')

#     def get(self, request, *args, **kwargs) :
#         # retrieve() : RetrieveModelMixin의 retrive() 
#         return self.retrieve(request, *args, **kwargs)