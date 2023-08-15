from django import forms
from .models import h_Chat, h_Comment

class h_ChatForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
        ('소식', '소식'),
        ('친목', '친목'),
        ('기타', '기타')
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
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = h_Comment
        fields = ['comment']