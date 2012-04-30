from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    executedScript = models.CharField(max_length=100, default="New script")

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User, dispatch_uid="users_profilecreation_signal")


class FileObject(models.Model):
    user = models.ForeignKey(User)

    file_name = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.file_name


#class SubmitScript(models.Model):
#    user = models.ForeignKey(User)
#
#    jobName = models.CharField(max_length=50)
#    queueName = models.CharField(max_length=50)
#    cpuNumber = models.SmallIntegerField()
#    requestedTime = models.CharField(max_length=8)
#    commands = models.CharField()
#
#    def __unicode__(self):
#        return self.jobName + "@" + self.queueName

class PBSServer(models.Model):
    time = models.DateTimeField(
        default=datetime.now)#auto_now_add=True sets datetime with creating object, not with every modifying action

    name = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    total_jobs = models.IntegerField()
    running_jobs = models.IntegerField()
    queued_jobs = models.IntegerField()
    pbs_version = models.CharField(max_length=10)


class PBSQueue(models.Model):
    server = models.ForeignKey(PBSServer)#, blank=True, null=True, on_delete=models.SET_NULL
    time = models.DateTimeField(default=datetime.now)

    name = models.CharField(default='', max_length=100, blank=True, null=True)
    type = models.CharField(default='', max_length=20, blank=True, null=True)
    total_jobs = models.IntegerField(default=0)
    running_jobs = models.IntegerField(default=0)
    queued_jobs = models.IntegerField(default=0)
    resource_walltime = models.CharField(default='', max_length=20, blank=True, null=True)
    resource_nodes = models.IntegerField(default=0)


class PBSJob(models.Model):
    user = models.ForeignKey(User)
    queue = models.ForeignKey(PBSQueue)
    time = models.DateTimeField(default=datetime.now)

    jobId = models.CharField(default='', max_length=50, blank=True, null=True)
    name = models.CharField(default='', max_length=100, blank=True, null=True)
    owner = models.CharField(default='', max_length=100, blank=True, null=True)
    state = models.CharField(default='', max_length=10, blank=True, null=True)
    queue_raw = models.CharField(default='', max_length=100, blank=True, null=True)

    start_time = models.DateTimeField(default=datetime.now, blank=True, null=True)
    resource_cput = models.CharField(default='', max_length=20, blank=True, null=True)
    resource_mem = models.CharField(default='', max_length=20, blank=True, null=True)
    resource_vmem = models.CharField(default='', max_length=20, blank=True, null=True)
    resource_walltime = models.CharField(default='', max_length=20, blank=True, null=True)


class PBSUserStat(models.Model):
    time = models.DateTimeField(default=datetime.now, auto_now_add=True)

    username = models.CharField(default='', max_length=100, blank=True, null=True)
    jobCount = models.IntegerField(default=0, blank=True, null=True)
