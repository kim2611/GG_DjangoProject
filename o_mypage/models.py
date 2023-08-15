from django.db import models

class Mypage(models.Model):
    name = models.ForeignKey(
        'bcuser.Bcuser', on_delete=models.CASCADE, verbose_name='사용자이름')
    # myschedule =models.DateTimeField(verbose_name='등록날짜')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table='h_chat'
        verbose_name='잡담'
        verbose_name_plural='잡담들'
