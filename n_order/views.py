from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import RegisterForm, OrderForm #order의 RegisterForm
from j_buyboard.models import Product
from bcuser.models import Bcuser
from .models import Order
from bcuser.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import F
from django.urls import reverse_lazy


########################################################
class OrderCreate(FormView):
    form_class = OrderForm
    template_name = 'order.html'
    success_url = reverse_lazy('buyboard')  # 구매 성공 시 이동할 URL

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.cleaned_data['product'])
            quantity = int(form.cleaned_data['quantity'])
            
            print("Before stock decrease:", prod.stock)  # 디버깅 메시지 추가
            prod.stock -= quantity
            print("After stock decrease:", prod.stock)   # 디버깅 메시지 추가

            if prod.stock >= 0:  # 재고가 음수가 되지 않도록 처리
                order = Order(
                    quantity=quantity,
                    product=prod,
                    bcuser=Bcuser.objects.get(email=self.request.session.get('user')),
                )
                order.save()
                if prod.stock <= 0:
                    prod.stock = 0
                    prod.sold_out = True
                prod.save()
            else:
                print("Not enough stock!")

        return super().form_valid(form)
    
    def form_invalid(self, form):
        product_id = form.cleaned_data.get('product')
        if product_id:
            return redirect('/buyboard/product/' + str(product_id))
        else:
            return redirect('buyboard')  # 예외 처리: product_id가 없을 경우 buyboard로 이동
    
    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw['request'] = self.request
        return kw


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    order_list = Order.objects.filter(product=product)

    context = {
        'product': product,
        'order_list': order_list,
    }

    return render(request, 'j_buy_detail.html', context)


