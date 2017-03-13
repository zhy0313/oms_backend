#!/usr/bin/env python
# -*- coding:utf-8 -*-

from peewee import *
from playhouse.pool import PooledMySQLDatabase

# mysql connection pool
db = PooledMySQLDatabase(
    database='oms',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    charset='utf8',
    max_connections=20,
    stale_timeout=300
)


# base model
class BaseModel(Model):
    class Meta:
        database = db


# task table
class Task(BaseModel):
    id = IntegerField()
    task_id = CharField(unique=True)
    creator = CharField()
    ip = CharField()
    create_time = IntegerField()
    target = CharField()
    version = IntegerField()
    type = CharField()
    content = CharField()
    description = CharField()
    executor = CharField()
    status = BooleanField()
    start_time = IntegerField()
    revert_time = IntegerField()
    percent = IntegerField()
    revert = BooleanField()

    class Meta:
        db_table = 'task'


def get_user_task_num_by_time(begin_time=0, end_time=0, username=None):
    if begin_time == 0 or end_time == 0 or begin_time > end_time or not username:
        return False

    data_list = []
    try:
        query = (Task
                 .select(Task.creator, fn.COUNT(Task.task_id).alias('task_sum'),
                         fn.FROM_UNIXTIME(Task.create_time, '%Y%m%d').alias('create_date'))
                 .where(
                        (Task.creator == username) &
                        (Task.create_time >= begin_time) &
                        (Task.create_time <= end_time))
                 .group_by(Task.creator, 'create_date'))

        for info in query.execute():
            data = info.__dict__['_data']
            data['task_sum'] = info.__dict__['task_sum']
            data['create_date'] = info.__dict__['create_date']
            print data
            data_list.append(data)
    except Exception as e:
        print e
        print "aaa"
    else:
        return data_list


get_task_num_by_time(1487658528, 1487661737, 'guoxu')

