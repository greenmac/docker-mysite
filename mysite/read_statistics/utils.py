from django.contrib.contenttypes.models import ContentType
from .models import ReadNum

def readStatisticsOnceRead(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在紀錄
            readrum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在對應的紀錄
            readrum = ReadNum(content_type=ct, object_id=obj.pk)
        # 計數+1
        readrum.read_num += 1
        readrum.save()
    return key
