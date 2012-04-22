from datetime import datetime
from PBSQuery import  PBSError
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from pytorque.libs.torque_service import TorqueService

class Command(BaseCommand):
#    args = '<poll_id poll_id ...>'
    help = 'Just store\'s pbs_server\'s info to db'

    def handle(self, *args, **options):
        #todo: get PyQuery data: server, queues, jobs
        #todo: create model's objects
        #todo: store objects to db (save) with concrete time (+-epsilon)

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




        except PBSError as pbsErr:
            print(pbsErr)
