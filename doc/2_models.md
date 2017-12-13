# 模型设计

## 模型分析
#### 分析
- 从功能的实现上来设计模型。
    - 登录验证。登录验证时需要用到用户的登录信息，这些信息就需要保存在数据库中，因此我们**需要创建一张用户表用来存放用户的登录名和密码**
        - 细节
            1. 用户名应该是唯一的
            2. 密码应该加密保存，方法是使用python提供的hashlib模块的sha256,一般我们要进行加盐处理。
                - 本项目中，为了方便测试，没有对密码进行加密，但是在实际开发中，一定要保证加密！！！
    - 预订界面。
        - 预订界面要想渲染出表格中的会议室，得__需要会议室表来储存会议室对象及其相关信息，因此我们需要创建一个会议室表__
        - 对于每一条预订记录，我们也需要用一张表来保存，这张表需要与其他表建立关联关系，主要字段如下
            - id
            - date: 预订的日期
            - period: 预订的时间段
                - 在这里没有额外创建个时间段表，因为时间段本身不经常变化，我们可以在模型中以choices代替，在一些大的项目中，我们应尽量避免使用过多的外键，因为跨表操作肯定会产生额外的性能损耗和IO
            - ForeignKey: user，一个用户可以预订多个，但是一条预订记录只能对应一个用户
            - ForeignKey: room，一个会议室可以有多条预订记录，但是一条预订记录只能对应一个会议室
            - 联合唯一: ("date", "id", "room")
                - 要保证，同一天内，一个会议室的同一个时间段只能有一条预订记录，这里不需要与user建立联合唯一
        
                
- 综上，我们需要创建三张表就可以实现需求中的功能
    - 会议室表
    - 用户表
    - 预订记录表
    

#### 实现

```python
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

```


