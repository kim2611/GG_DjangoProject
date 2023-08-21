from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from bcuser.models import Bcuser
# Create your models here.
class c_Notice(models.Model):
    c_writer = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='작성자')
    c_category = models.CharField(max_length=64, default='news', verbose_name='카테고리',
        choices=(
        ('공지', '공지'),
        ('이벤트', '이벤트'),
        ('기타', '기타')
        ))
    c_title = models.CharField(max_length=128, verbose_name='제목')
    c_contents = models.TextField(verbose_name='내용')
    c_register_date=models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
    c_click = models.PositiveIntegerField(default=0)
    c_votes = models.PositiveIntegerField(default=0)  # 추천수 필드 추가
    c_voters = models.ManyToManyField(Bcuser, related_name='upvoted_notices', blank=True)  # 추천한 사용자 목록 필드 추가
    def __str__(self):
        return self.c_title
    
    class Meta:
        verbose_name='게임정보글'
        verbose_name_plural='게임정보 게시판'
        
        
class c_Comment(models.Model):
    post= models.ForeignKey(c_Notice, on_delete=models.CASCADE, verbose_name='게시글')
    author = models.ForeignKey(Bcuser, on_delete=models.CASCADE, verbose_name='작성자')
    comment= models.CharField(max_length=256, verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    def __str__(self):
        return f'원래 글 : {self.post.c_title} ///// 댓글 내용 : {self.author}'
    
    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글들'