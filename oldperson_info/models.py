from django.db import models


class OldPersonInfo(models.Model):
    ID = models.IntegerField(primary_key=True)
    ORG_ID = models.IntegerField(null=True)
    CLIENT_ID = models.IntegerField(null=True)
    username = models.CharField(max_length=50, null=True, verbose_name='用户名')
    gender = models.CharField(max_length=5, null=True, verbose_name='性别')
    phone = models.CharField(max_length=50, null=True)
    id_card = models.CharField(max_length=50, null=True)
    birthday = models.DateTimeField(null=True, blank=True)
    checkin_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    imgset_dir = models.CharField(max_length=200, null=True)
    profile_photo = models.CharField(max_length=200, null=True)
    room_number = models.CharField(max_length=50, null=True)
    firstguardian_name = models.CharField(max_length=50, null=True)
    firstguardian_relationship = models.CharField(max_length=50, null=True)
    firstguardian_phone = models.CharField(max_length=50, null=True)
    firstguardian_wechat = models.CharField(max_length=50, null=True)
    secondguardian_name = models.CharField(max_length=50, null=True)
    secondguardian_relationship = models.CharField(max_length=50, null=True)
    secondguardian_phone = models.CharField(max_length=50, null=True)
    secondguardian_wechat = models.CharField(max_length=50, null=True)
    health_state = models.CharField(max_length=50, null=True)
    DESCRIPTION = models.CharField(max_length=200, null=True)
    ISACTIVE = models.CharField(max_length=10, null=True)
    CREATED = models.DateTimeField(null=True, blank=True)
    CREATEBY = models.IntegerField(null=True)
    UPDATED = models.DateTimeField(null=True, blank=True)
    UPDATEBY = models.IntegerField(null=True)
    REMOVE = models.CharField(max_length=1, null=True)

    class Meta:
        db_table = 'oldperson_info'

    def __str__(self):
        return self.username
