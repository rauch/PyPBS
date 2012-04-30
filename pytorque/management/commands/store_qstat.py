from datetime import datetime
import logging
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from pytorque.libs.torque_service import TorqueService
from pytorque.models import PBSUserStat

server_logger = logging.getLogger('pytorque.custom')

class Command(BaseCommand):
    help = 'Just store\'s pbs_server\'s info to db'

    def handle(self, *args, **options):
        currentTime = datetime.now()

        try:
            pbsServers = TorqueService.getModelServers()
            for pbsServer in pbsServers:
                pbsServer.time = currentTime
                pbsServer.save()

                pbsQueues = TorqueService.getModelQueues(pbsServer)
                for pbsQueue in pbsQueues:
                    pbsQueue.time = currentTime
                    pbsQueue.save()

                pbsJobs = TorqueService.getModelJobs()
                TorqueService.mapJobsToQueue(pbsQueues, pbsJobs)

                users = User.objects.all()
                TorqueService.mapJobsToUser(users, pbsJobs)

                for pbsJob in pbsJobs:
                    pbsJob.time = currentTime
                    pbsJob.save()

            #make raw query, fill user_stat
            pUserQuerySet = User.objects.raw('SELECT auth_user.*, COUNT(DISTINCT pytorque_pbsjob.jobId) as jobCount FROM pytorque_pbsjob, auth_user\
                                            WHERE pytorque_pbsjob.user_id = auth_user.id\
                                            GROUP BY auth_user.username')
            for rowQuerySet in pUserQuerySet:
                userStat = PBSUserStat()
                userStat.jobCount = rowQuerySet.jobCount
                userStat.username = rowQuerySet.username
                userStat.time = currentTime
                userStat.save()



        except Exception as exc:
            server_logger.error("An unexpected error occurred while running cron task: %s" % str(exc))
