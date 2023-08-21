from django import forms
from .models import buyProduct, j_Comment

CATEGORY_CHOICES = [
    ('본체', '본체'),
    ('타이틀', '타이틀'),
    ('주변기기', '주변기기'),
    ('기타', '기타'),
]

class buyRegisterForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select
    )

    class Meta:
        model = buyProduct
        fields = ['name', 'price', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].widget.attrs['value'] = self.instance.name
            self.fields['price'].widget.attrs['value'] = self.instance.price
            self.fields['category'].widget.attrs['value'] = self.instance.category
            self.fields['description'].widget.attrs['value'] = self.instance.description

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')
        description = cleaned_data.get('description')

        if not (name or price or description or category):
            self.add_error('name', '이름을 적어주세요')
            self.add_error('price', '희망가격을 적어주세요')
            self.add_error('category', '카테고리를 골라주세요')
            self.add_error('description', '내용을 적어주세요')
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = j_Comment
        fields = ['comment']

class ChatSearchForm(forms.Form):
    search_query = forms.CharField(label='검색어', max_length=100, required=False)