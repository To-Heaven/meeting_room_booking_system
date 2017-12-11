from django.db import models


class User(models.Model):
    """ 用户表
    普通字段:
        id, username, password
    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户表'


class MeetingRoom(models.Model):
    """ 会议室表
    普通字段:
        id, title
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='会议室名称')
    number_of_people = models.IntegerField(verbose_name='会议室最大容纳人数', default=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '会议室表'


class Order(models.Model):
    """ 会议室预定表
    普通字段:
        id, schedule_date
    关联字段:
        period, user
    """

    id = models.AutoField(primary_key=True)

    period_list = [
        (1, "8:00~9:00"),
        (2, "9:00~10:00"),
        (3, "10:00~11:00"),
        (4, "11:00~12:00"),
        (5, "12:00~13:00"),
        (6, "13:00~14:00"),
        (7, "14:00~15:00"),
        (8, "15:00~16:00"),
        (9, "16:00~17:00"),
        (10, "17:00~18:00"),
        (11, "18:00~19:00"),
        (12, "19:00~20:00"),
        (13, "20:00~21:00")
    ]
    period = models.IntegerField(choices=period_list, verbose_name='时间段')

    schedule_date = models.DateField(verbose_name='预定时间')
    room = models.ForeignKey(to='MeetingRoom', to_field='id', on_delete=True)
    user = models.ForeignKey(to='User', to_field='id', on_delete=True)

    def __str__(self):
        return 'date:{} period:{} room：{}'.format(self.schedule_date, self.period, self.room)

    class Meta:
        verbose_name_plural = '会议室预定表'
        unique_together = (("room", "period", "schedule_date"), )
