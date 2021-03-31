import os

import celery
import pymysql

from izufang import settings

pymysql.install_as_MySQLdb()

# Celery 配置信息。注意顺序。
# 1. 加载配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'izufang.settings')

# 2. 创建对象
app = celery.Celery('izufang',
                    broker='amqp://gyp:gyp@127.0.0.1:5672/ivhost',
                    backend='redis://127.0.0.1:6379/2')

# 3. 读取配置文件
app.config_from_object('django.conf:settings')

# 4. 发现异步任务
app.autodiscover_tasks(['common', ])
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
