from django.db import models
from django.utils import timezone
from bcuser.models import Bcuser

class h_Chat(models.Model):
    h_writer = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='작성자')
    h_category = models.CharField(max_length=64, default='news', verbose_name='카테고리',
            choices=(
            ('소식', '소식'),
            ('친목', '친목'),
            ('기타', '기타')
            ))
    h_title = models.CharField(max_length=128, verbose_name='제목')
    h_contents = models.TextField(verbose_name='내용')
    h_register_date=models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
    h_click = models.PositiveIntegerField(default=0)
    h_votes = models.PositiveIntegerField(default=0)  # 추천수 필드 추가
    h_voters = models.ManyToManyField(Bcuser, related_name='upvoted_chats', blank=True)  # 추천한 사용자 목록 필드 추가
    
    def __str__(self):
        return self.h_title
    
    class Meta:
        db_table='h_chat'
        verbose_name='잡담'
        verbose_name_plural='잡담들'

class h_Comment(models.Model):
    post= models.ForeignKey(h_Chat, on_delete=models.CASCADE, verbose_name='게시글')
    author = models.ForeignKey(Bcuser, on_delete=models.CASCADE, verbose_name='작성자')
    comment= models.CharField(max_length=256, verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    def __str__(self):
        return f'원래 글 : {self.post.h_title} ///// 댓글 내용 : {self.name}'
    
    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글들'