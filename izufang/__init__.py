import os

import celery
import pymysql
from celery.schedules import crontab

from izufang import settings

pymysql.install_as_MySQLdb()

# Celery 配置信息。注意顺序。
# 1. 加载配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'izufang.settings')

# 2. 创建对象
app = celery.Celery('izufang',
                    broker='amqp://gyp:gyp@127.0.0.1:5672/ivhost',
                    backend='django-db')

"""定时任务配置"""
app.conf.update(
    # 设置时区要和settings中保持一致
    timezone=settings.TIME_ZONE,
    enable_utc=True,

    # 定时任务(计划任务)相当于消息的生产者，如果只有生产者没有消费者
    # 那么消息会在消息队列中积压。
    # 将来实际部署项目的时候生产者、消费者、消息队列可能都是不同节点
    beat_schedule={
        'task1': {
            # 指定消费者在哪一个模块下的哪个包中的哪个函数
            'task': 'common.tasks.display_info',
            # 设置定时时间。分钟 小时 日份 月份 年份
            'schedule': crontab('*', '*', '*', '*', '*'),
            # 要给display_info函数的参数
            'args': ('Hello workld！',)
        }
    }
)

# 3. 读取配置文件。定时任务无需此配置
# app.config_from_object('django.conf:settings')

# 4. 发现异步任务
app.autodiscover_tasks(['common', ])
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
