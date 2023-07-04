from django.db import models


class EmployeeInfo(models.Model):
    ORG_ID = models.IntegerField(null=True)
    CLIENT_ID = models.IntegerField(null=True)
    username = models.CharField(max_length=50, null=True, verbose_name='用户名')
    gender = models.CharField(max_length=5, null=True, verbose_name='性别')
    phone = models.CharField(max_length=50, null=True)
    id_card = models.CharField(max_length=50, null=True)
    birthday = models.DateTimeField(null=True)
    hire_date = models.DateTimeField(null=True)
    resign_date = models.DateTimeField(null=True)
    imgset_dir = models.CharField(max_length=200, null=True)
    profile_photo = models.CharField(max_length=200, null=True)
    DESCRIPTION = models.CharField(max_length=200, null=True)
    ISACTIVE = models.CharField(max_length=10, null=True)
    CREATED = models.DateTimeField(null=True)
    CREATEBY = models.IntegerField(null=True)
    UPDATED = models.DateTimeField(null=True)
    UPDATEBY = models.IntegerField(null=True)
    REMOVE = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'employee_info'
