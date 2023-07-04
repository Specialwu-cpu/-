from django.db import models


class EventInfo(models.Model):
    event_type = models.IntegerField(null=True, blank=True, verbose_name='事件类型')
    event_date = models.DateTimeField(null=True, blank=True, verbose_name='事件日期')
    event_location = models.CharField(max_length=200, null=True, blank=True, verbose_name='事件地点')
    event_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='事件描述')
    oldperson_id = models.IntegerField(null=True, blank=True, verbose_name='老人ID')

    class Meta:
        db_table = 'event_info'  # 指明数据库表名

    def __str__(self):
        return f"Event ID: {self.id}"
