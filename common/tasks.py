from datetime import timedelta

from django.db import DatabaseError
from django.utils import timezone

from common.models import Record
from izufang import app


@app.task
def display_info(content):
    """定期清理过期垃圾记录"""
    check_time = timezone.now() - timedelta(days=90)
    try:
        Record.objects.filter(recorddate__lte=check_time) \
            .delete()
        return True
    except DatabaseError:
        return False