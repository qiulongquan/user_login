from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    # 模型类中设置:blank=True,表示代码中创建数据库记录时该字段可传空白(空串,空字符串)
    org = models.CharField('Organization',
                           max_length=128,
                           blank=True,)
    telephone = models.CharField('Telephone',
                                 max_length=50,
                                 blank=True,)
    mod_data = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User profile'

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.user.__str__())
