from django.shortcuts import render, redirect, get_object_or_404
from j_buyboard.models import Product
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from django.core.paginator import Paginator
from .models import Product
from n_order.forms import RegisterForm
from n_order.models import Order
from django.http import Http404
from .forms import *
from bcuser.models import Bcuser
from django.db.models import F
from django.shortcuts import render
from .models import Product
from n_order.models import Order




# Create your views here.
class ProductList(ListView):
    model=Product
    template_name='j_buyboard.html'
    context_object_name='product_list'
    paginate_by=10
# ##### 실패작인듯?!
    # def chat_list(request):
    #     all_Products = Product.objects.all().order_by("-id")
    #     page = int(request.GET.get('p', 1))  # 초기에 페이지는 1로 시작
    #     paginator = Paginator(all_Products, 10)  # 전체 글을 가져와서 4개씩 나누어 보여줌
    #     product_list = paginator.get_page(page)
    #     return render(request, 'h_chat_list.html', {'product_list': product_list})


class ProductCreate(FormView):
    template_name='j_register_buy.html'
    form_class=RegisterForm
    success_url='/buyboard/'
    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'), 
            price=form.data.get('price'), 
            description=form.data.get('description'), 
            stock=form.data.get('stock')
            )
        product.save()
        return super().form_valid(form)
# ######################################################################
# class ProductDetail(DetailView):
#     queryset = Product.objects.all()
#     context_object_name='product'
#     template_name='j_buy_detail.html'
#     def get_context_data(self, **kwargs):
#         #기본적인 Product의 데이터 가져오기
#         context=super().get_context_data(**kwargs)
#         # Order의 OrderForm에서 받아온 데이터 추가
#         # context['form']=OrderForm(self.request)
#         return context
#########################################################################
class ProductDetail(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'j_buy_detail.html'

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if 'buy_button' in request.POST:
            if product.stock > 0:
                product.stock -= 1
                if product.stock == 0:
                    product.sold_out = True
                product.save()
        return redirect('product_detail', pk=product.pk)
    #######################################################################
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             product = order.product
#             product.stock = F('stock') - order.quantity
#             if product.stock <= 0:
#                 product.stock = 0
#                 product.sold_out = True
#             product.save()
#             context = {
#                 'order': order,
#                 'product': product,
#             }
#             return render(request, 'order_success.html', context)
#     else:
#         form = OrderForm()
#     context = {'form': form}
#     return render(request, 'order/create.html', context)
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    order_list = Order.objects.filter(product=product)
    context = {
        'product': product,
        'order_list': order_list,
    }
    return render(request, 'j_buy_detail.html', context)
    
########################## 아직 실패 ################
# def board_delete(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     # 로그인한 사용자와 채팅 메시지 작성자가 같은지 확인
#     if Bcuser.objects.get(email=request.session.get('user')) == product.email:
#         product.delete()
#         return redirect('/buyboard/')  # 채팅 목록 페이지로 리다이렉트
#     else:
#         raise Http404('권한이 없습니다')
# # def board_update(request, pk):
# #     if not request.session.get('user'):
#         return redirect('/login/')
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:  # 게시글이 없을때 다음 메시지를 띄움
#         raise Http404('게시글을 찾을 수 없습니다.')
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():  # 폼이 유효한지
#             user_id = request.session.get('user') # 세션에서 로그인한 아이디 확보
#             # product.h_category = form.cleaned_data['category']
#             product.name = form.cleaned_data['title']
#             product.price = form.cleaned_data['price']
#             product.h_writer = Bcuser.objects.get(email=request.session.get('user'))
#             product.save()
#             return redirect('/boyboard/')
#     else:
#         form = RegisterForm(initial={'title':product.h_title, 'contents':product.h_contents})
#     return render(request, 'j_update.html', {'form': form})