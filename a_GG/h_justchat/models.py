from django.db import models
from django.utils import timezone

class h_Chat(models.Model):
    h_writer = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='작성자')
    h_category = models.CharField(max_length=64, default='news', verbose_name='카테고리',
            choices=(
            ('news', '소식'),
            ('friendship', '친목'),
            ('etc', '기타')
            ))
    h_title = models.CharField(max_length=128, verbose_name='제목')
    h_contents = models.TextField(verbose_name='내용')
    h_register_date=models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
    #h_register_date=models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
    
    def __str__(self):
        return self.h_title
    
    class Meta:
        db_table='h_chat'
        verbose_name='잡담'
        verbose_name_plural='잡담들'

