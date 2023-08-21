from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from bcuser.models import Bcuser
# Create your models here.
class l_Info(models.Model):
    l_writer = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='작성자')
    l_category = models.CharField(max_length=64, default='news', verbose_name='카테고리',
        choices=(
        ('PC', 'PC'),
        ('닌텐도', '닌텐도'),
        ('플스', '플스'),
        ('엑스박스', '엑스박스'),
        ('기타', '기타')
        ))
    l_title = models.CharField(max_length=128, verbose_name='제목')
    l_contents = models.TextField(verbose_name='내용')
    l_register_date=models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
    l_click = models.PositiveIntegerField(default=0)
    l_votes = models.PositiveIntegerField(default=0)  # 추천수 필드 추가
    l_voters = models.ManyToManyField(Bcuser, related_name='upvoted_infos', blank=True)  # 추천한 사용자 목록 필드 추가
    def __str__(self):
        return self.l_title
    
    class Meta:
        verbose_name='게임정보글'
        verbose_name_plural='게임정보 게시판'
        
        
class l_Comment(models.Model):
    post= models.ForeignKey(l_Info, on_delete=models.CASCADE, verbose_name='게시글')
    author = models.ForeignKey(Bcuser, on_delete=models.CASCADE, verbose_name='작성자')
    comment= models.CharField(max_length=256, verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    def __str__(self):
        return f'원래 글 : {self.post.l_title} ///// 댓글 내용 : {self.author}'
    
    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글들'