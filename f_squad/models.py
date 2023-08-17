from django.db import models
from django.utils import timezone
from bcuser.models import Bcuser

class f_Squad(models.Model):
    f_writer = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='작성자')
    f_category = models.CharField(max_length=64, default='news', verbose_name='카테고리',
            choices=(
            ('PC', 'PC'),
            ('닌텐도', '닌텐도'),
            ('플스', '플스'),
            ('엑스박스', '엑스박스'),
            ('기타', '기타')
            ))
    f_title = models.CharField(max_length=128, verbose_name='제목')
    f_contents = models.TextField(verbose_name='내용')
    f_register_date=models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
    f_click = models.PositiveIntegerField(default=0)
    f_votes = models.PositiveIntegerField(default=0)  # 추천수 필드 추가
    f_voters = models.ManyToManyField(Bcuser, related_name='upvoted_squads', blank=True)  # 추천한 사용자 목록 필드 추가
    f_need = models.IntegerField(verbose_name='정원')
    
    def __str__(self):
        return self.f_title
    
    class Meta:
        db_table='f_squad'
        verbose_name='3-4인모집'
        verbose_name_plural='3-4인모집글들'

class f_Comment(models.Model):
    post= models.ForeignKey(f_Squad, on_delete=models.CASCADE, verbose_name='게시글')
    author = models.ForeignKey(Bcuser, on_delete=models.CASCADE, verbose_name='작성자')
    comment= models.CharField(max_length=256, verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    def __str__(self):
        return f'원래 글 : {self.post.f_title} ///// 댓글 내용 : {self.name}'
    
    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글들'