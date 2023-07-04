from django.db import models


class SysUser(models.Model):
    ORG_ID = models.IntegerField()
    CLIENT_ID = models.IntegerField()
    UserName = models.CharField(max_length=50, verbose_name='用户名')
    Password = models.CharField(max_length=50, null=True, blank=True, verbose_name='密码')
    REAL_NAME = models.CharField(max_length=50, null=True, blank=True)
    SEX = models.CharField(max_length=20, null=True, blank=True)
    EMAIL = models.CharField(max_length=50, null=True, blank=True)
    PHONE = models.CharField(max_length=50, null=True, blank=True)
    MOBILE = models.CharField(max_length=50, null=True, blank=True)
    DESCRIPTION = models.CharField(max_length=200, null=True, blank=True)
    ISACTIVE = models.CharField(max_length=10, null=True, blank=True)
    CREATED = models.DateTimeField(null=True, blank=True)
    CREATEBY = models.IntegerField(null=True, blank=True)
    UPDATED = models.DateTimeField(null=True, blank=True)
    UPDATEBY = models.IntegerField(null=True, blank=True)
    REMOVE = models.CharField(max_length=1, null=True, blank=True)
    DATAFILTER = models.CharField(max_length=200, null=True, blank=True)
    theme = models.CharField(max_length=45, null=True, blank=True)
    defaultpage = models.CharField(max_length=45, null=True, blank=True, verbose_name='登录成功页面')
    logoimage = models.CharField(max_length=45, null=True, blank=True, verbose_name='显示不同logo')
    qqopenid = models.CharField(max_length=100, null=True, blank=True, verbose_name='第三方登录的凭证')
    appversion = models.CharField(max_length=10, null=True, blank=True, verbose_name='检测app的版本号')
    jsonauth = models.CharField(max_length=1000, null=True, blank=True, verbose_name='app权限控制')

    class Meta:
        db_table = 'sys_user'

    def __str__(self):
        return f"User ID: {self.ID}"
