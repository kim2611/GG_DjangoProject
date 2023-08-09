from django import forms
from .models import c_Board

# forms.Form 유효성 검사를 진행하는 클래스



class c_BoardForm(forms.Form):
    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요.'
        },
        max_length=256, label='글제목'
    )
    contents=forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요'
        },
        widget=forms.Textarea, label='내용'
    )
    
    
    def clean(self):
        cleaned_data=super().clean()
        title = cleaned_data.get('title')
        contents = cleaned_data.get('contents')
        
        if not(title and contents):
            self.add_error('title','값이 없습니다')
            self.add_error('contents','값이 없습니다')