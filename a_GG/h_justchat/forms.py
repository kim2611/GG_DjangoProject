from django import forms
from .models import h_Chat

class h_ChatForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
        ('news', '소식'),
        ('friendship', '친목'),
        ('etc', '기타')
    ],
        error_messages={
            'required': '카테고리를 선택해주세요'
        },

        label="카테고리"
    )
    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요'
        },
        max_length=128, label="제목"
    )
    contents = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요'
        },
        widget=forms.Textarea, label='내용'
    )

class ChatSearchForm(forms.Form):
    search_query = forms.CharField(label='검색어', max_length=100, required=False)