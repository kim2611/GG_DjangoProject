from django.db import models
from django.utils import timezone

# Create your models here.
class c_Board(models.Model) :
    title = models.CharField(max_length=256, verbose_name='글제목')
    contents = models.TextField(verbose_name= '본문')
    writer = models.ForeignKey(
    'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='작성자')
    category = models.CharField(max_length=128, verbose_name='카테고리',
                                default='steam',
            choices=(
                ('스팀', '스팀'),
                ('닌텐도', '닌텐도')
            ))
    # tags = models.ManyToManyField('c_Tag', verbose_name='태그')
    # register_date = models.DateTimeField(default=timezone.now, verbose_name='등록날짜') #auto_now_add=True,
        
    def __str__(self) :
        return self.title
    
    class Meta :
        db_table = 'bootcampus_product'
        verbose_name = '공지'
        verbose_name_plural = '공지들'
# title, contents, writer, 현재시간
