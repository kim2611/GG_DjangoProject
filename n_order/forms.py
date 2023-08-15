from typing import Any, Dict
from django import forms
from .models import Order
from j_buyboard.models import Product
from bcuser.models import Bcuser

class RegisterForm(forms.Form):
    # request 라는 추가적인 인자를 받을 수 있도록 재정의
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=request

    quantity=forms.IntegerField(
        error_messages={
            'required':'수량을 입력하시오'
        }, label='수량'
    )

    product=forms.IntegerField(
        error_messages={
            'required':'상품 정보를 입력하시오'
        }, label='상품정보', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data=super().clean()
        quantity=cleaned_data.get('quantity')
        product=cleaned_data.get('product')
        if not(quantity and product):
            self.add_error('quantity','입력정보가 없다리옹?')
            self.add_error('product','값이 없다리옹?')



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'product']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super().__init__(*args, **kwargs)

        # 제품 선택 폼 필드를 확장하여 선택 가능한 제품 목록을 필터링합니다.
        if self.request:
            available_products = Product.objects.filter(stock__gt=0)
            self.fields['product'].queryset = available_products

    def save(self, commit=True):
        # 'product' 필드를 제대로 설정하기 위해 Order 객체를 생성할 때 사용합니다.
        order = super().save(commit=False)
        order.bcuser = Bcuser.objects.get(email=self.request.session.get('user'))
        order.product = self.cleaned_data.get('product')

        if commit:
            order.save()
            product = order.product
            product.stock -= order.quantity
            if product.stock <= 0:
                product.stock = 0
                product.sold_out = True
            product.save()

        return order