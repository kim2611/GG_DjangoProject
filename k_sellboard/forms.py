from django import forms
from .models import Product, Comment


CATEGORY_CHOICES = [
    ('본체', '본체'),
    ('타이틀', '타이틀'),
    ('주변기기', '주변기기'),
    ('기타', '기타'),
]
class RegisterForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select
    )

    class Meta:
        model = Product
        fields = ['name', 'price','category', 'stock','description' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].widget.attrs['value'] = self.instance.name
            self.fields['price'].widget.attrs['value'] = self.instance.price
            self.fields['category'].widget.attrs['value'] = self.instance.category
            self.fields['stock'].widget.attrs['value'] = self.instance.stock
            self.fields['description'].widget.attrs['value'] = self.instance.description

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')
        stock=cleaned_data.get('stock')
        description = cleaned_data.get('description')

        if not (name or price or description or stock or category):
            self.add_error('name', '이름을 적어주세요')
            self.add_error('price', '희망가격을 적어주세요')
            self.add_error('category', '카테고리를 골라주세요')
            self.add_error('description', '내용을 적어주세요')
            self.add_error('stock', '값이 없습니다')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class ChatSearchForm(forms.Form):
    search_query = forms.CharField(label='검색어', max_length=100, required=False)