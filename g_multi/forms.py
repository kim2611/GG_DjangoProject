from django import forms
from .models import g_Multi,g_Comment

class g_MultiForm(forms.Form):
    category = forms.ChoiceField(
        choices=[
        ('PC', 'PC'),
        ('닌텐도', '닌텐도'),
        ('플스', '플스'),
        ('엑스박스', '엑스박스'),
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
    need = forms.IntegerField(
        error_messages={
            'required':'게시판에 맞는 인원 수를 입력해주세요. (5인 이상 게시판)'
        },
        label='참가인원'
    )
    def clean_need(self):
        need = self.cleaned_data['need']
        if need <= 0:
            raise forms.ValidationError("게시판에 맞는 인원 수를 입력해주세요. (5인 이상 게시판)")
        return need

class ChatSearchForm(forms.Form):
    search_query = forms.CharField(label='검색어', max_length=100, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = g_Comment
        fields = ['comment']