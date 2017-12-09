# Generated by Django 2.0 on 2017-12-09 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingRoom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='会议室名称')),
            ],
            options={
                'verbose_name_plural': '会议室表',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('period', models.IntegerField(choices=[(1, '8:00~9:00'), (2, '9:00~10:00'), (3, '10:00~11:00'), (4, '11:00~12:00'), (5, '12:00~13:00'), (6, '13:00~14:00'), (7, '14:00~15:00'), (8, '15:00~16:00'), (9, '16:00~17:00'), (10, '17:00~18:00'), (11, '18:00~19:00'), (12, '19:00~20:00'), (13, '20:00~21:00')], verbose_name='时间段')),
                ('schedule_date', models.DateField(verbose_name='预定时间')),
                ('room', models.ForeignKey(on_delete=True, to='room.MeetingRoom')),
            ],
            options={
                'verbose_name_plural': '会议室预定表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=True, to='room.User'),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('room', 'period', 'schedule_date')},
        ),
    ]
