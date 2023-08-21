from django.db import models
from bcuser.models import Bcuser

class Mypage(models.Model):
    writer = models.ForeignKey(
        Bcuser, on_delete=models.CASCADE, verbose_name='작성자')
    age = models.CharField(
        max_length=10,
        choices=[
        ('10대', '10대'),
        ('20대', '20대'),
        ('30대', '30대'),
        ('40대', '40대'),
        ('50대 이상', '50대 이상')
],
        default='20대',  # 기본값 설정
        verbose_name='연령대'
    )

    gender = models.CharField(
        max_length=10,
        choices=[
        ('남자', '남자'),
        ('여자', '여자'),
],
        default='남자',  # 기본값 설정
        verbose_name='성별'
    )

    voice = models.CharField(
        max_length=10,
        choices=[
        ('가능', '가능'),
        ('불가능', '불가능'),
],
        default='음성채팅 가능',  # 기본값 설정
        verbose_name='음성대화'
    )
    introduction = models.TextField(
        verbose_name='자기소개',  # 필요한 라벨 설정
        blank=True,  # 비어있어도 됨
        null=True,  # 데이터베이스에서 NULL 값 허용
    )

    def __str__(self):
        return self.age
    
    # Table Name
    class Meta:
        db_table='mypage'
        verbose_name="나의 프로필"
        verbose_name_plural='나의 프로필'
