from django import forms

# forms.Form: 유효성 검사를 진행하는 클래스로 상속받아서 사용함
# class BoardForm(forms.Form):
#     # 유효성 검사 : 값을 입력하지 않았을때 기본적으로 영문 메세지가 출력됨
#     # 사용자가 원하는 메세지를 구현하여 출력할 수 있음
#     title=forms.CharField(
#         error_messages={
#             'required':'제목을 입력해주세요'
#         },
#         max_length=128, label="제목")
    
#     contents=forms.CharField(
#         error_messages={
#         'required':'내용을 입력해주세요'
#         },
#         widget=forms.Textarea, label="내용")
    
#     tags = forms.CharField(
#         required=False, label='태그')