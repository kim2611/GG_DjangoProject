from django.db import models

# Create your models here.

class Bcuser(models.Model) :
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    nickname = models.CharField(max_length=64, verbose_name='닉네임')
    # 사용자의 등급을 저장하는 데 사용 -> 선택 가능한 값은 'admin'과 'user'
    level = models.CharField(max_length=8, verbose_name='등급',
                choices=(
                    ('admin', 'admin'),
                    ('user', 'user')
                ))
    register = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
    
    def __str__(self) :
        return self.email
    
    class Meta :
        db_table = 'bootcampus_bcuser'
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'