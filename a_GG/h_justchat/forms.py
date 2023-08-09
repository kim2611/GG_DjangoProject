from django import forms
from .models import h_Chat

class h_ChatForm(forms.Form):
    # 유효성 검사 : 값을 입력하지 않았을때 기본적으로 얻은 메세지가 출력됨
    # 사용자가 원하는 메세지를 구현하여 출력할 수 있음
    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요'
        },
        max_length=128, label="제목")
    contents = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요'
        },
        widget=forms.Textarea, label='내용')

