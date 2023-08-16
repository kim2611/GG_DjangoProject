from django.shortcuts import render, redirect, get_object_or_404
from j_buyboard.models import Product
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from django.core.paginator import Paginator
from .models import Product
from n_order.forms import RegisterForm as OrderForm
from n_order.models import Order
from django.http import Http404
from .forms import *
from django.db.models import F
from django.shortcuts import render
from .models import Product
from n_order.models import Order




# Create your views here.
class ProductList(ListView):
    model=Product
    template_name='k_sell_board.html'
    context_object_name='product_list'
    paginate_by=10


class ProductCreate(FormView):
    template_name='k_register_sell.html'
    form_class=RegisterForm
    success_url='/sellboard/'
    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'), 
            price=form.data.get('price'), 
            description=form.data.get('description'), 
            stock=form.data.get('stock')
            )
        product.save()
        return super().form_valid(form)

class ProductDetail(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'k_sell_detail.html'

    def get_context_data(self, **kwargs):
        # 기본적인 Product의 데이터 가져오기
        context=super().get_context_data(**kwargs)
        # Order의 OrderForm에서 받아온 데이터 추가
        context['form']=OrderForm(self.request)
        return context
