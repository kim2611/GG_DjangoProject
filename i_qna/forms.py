from django import forms
from .models import i_Qna, i_Comment

class i_QnaForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
        ('일반질문', '일반질문'),
        ('게임질문', '게임질문'),
        ('시세정보', '시세정보')
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

class BoardSearchForm(forms.Form):
    search_query = forms.CharField(label='검색어', max_length=100, required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = i_Comment
        fields = ['comment']