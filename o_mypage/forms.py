from django import forms
from .models import Bcuser

class MypageUpdate(forms.Form):
    age = forms.ChoiceField(
        choices=[
        ('10대', '10대'),
        ('20대', '20대'),
        ('30대', '30대'),
        ('40대', '40대'),
        ('50대 이상', '50대 이상')
],
        error_messages={
            'required': '연령대를 선택해주세요'
        },
        label="연령대", required=True
    )

    gender = forms.ChoiceField(
        choices=[
        ('남자', '남자'),
        ('여자', '여자'),
],
        error_messages={
            'required': '성별을 선택해주세요'
        },
        label="성별", required=True
    )
    voice = forms.ChoiceField(
        choices=[
        ('가능', '가능'),
        ('불가능', '불가능'),
],
        error_messages={
            'required': '음성채팅 참여 여부를 선택해주세요'
        },
        label="음성채팅 참여 여부", required=True
    )
    introduction = forms.CharField(
        label="자기소개",
        required=False,
        max_length=80,
        widget=forms.Textarea(attrs={
            'rows': 3,  # 텍스트 영역의 높이를 설정
            'style': 'max-height: 100px; overflow: auto; white-space: normal; word-wrap: break-word;'
            }),  # 텍스트 영역의 높이를 설정
        initial=""
    )