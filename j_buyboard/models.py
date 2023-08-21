from django.db import models
from bcuser.models import Bcuser

class buyProduct(models.Model):
    name=models.CharField(max_length=256, verbose_name='상품명')
    price=models.IntegerField(verbose_name='희망가격')
    description=models.TextField(verbose_name='상품설명')
    register_date=models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
    writer = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE,null=True,default='', verbose_name='작성자')
    category = models.CharField(max_length=64, default='news', verbose_name='카테고리',
            choices=(
            ('본체', '본체'),
            ('타이틀', '타이틀'),
            ('주변기기', '주변기기'),
            ('기타', '기타')
            ))




    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'bootcampus_buyproduct'
        verbose_name = '상품'
        verbose_name_plural = '상품들'




class j_Comment(models.Model):
    post=models.ForeignKey(buyProduct,on_delete=models.CASCADE, verbose_name='게시글')
    author = models.ForeignKey(Bcuser, on_delete=models.CASCADE, verbose_name='작성자')
    comment= models.CharField(max_length=256, verbose_name='댓글 내용')
    created_at=models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    def __str__(self):
        return f'원래 글 : {self.post.name} ///// 댓글 내용 : {self.name}'

    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글들'