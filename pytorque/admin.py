from pytorque.models import PBSServer
from pytorque.models import PBSQueue
from pytorque.models import PBSJob
from pytorque.models import PBSUserStat
from django.contrib import admin

admin.site.register(PBSServer)
admin.site.register(PBSQueue)
admin.site.register(PBSJob)
admin.site.register(PBSUserStat)