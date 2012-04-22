# -*- coding: utf-8 -*-
from datetime import  datetime

from PBSQuery import PBSQuery, PBSError
import time
import pbs
from pytorque.models import PBSServer, PBSQueue, PBSJob


class Job():
    __datetime_format = "%d-%m-%Y  %H:%M"

    jobId = None
    state = None
    user = None
    queue = None
    name = None
    cpu_time = None
    n_p = None
    queued = None
    started = None
    running_time = None

    def __init__(self, jobId):
        self.jobId = jobId

    def setQueued(self, queuedTime):
        self.queued = time.strftime(self.__datetime_format, time.localtime(int(queuedTime)))

    #        self.queued = "/Date(" + str(1000 * int(queuedTime)) + ")/"

    def setStarted(self, startedTime):
        self.started = time.strftime(self.__datetime_format, time.localtime(int(startedTime)))


class TorqueService():
    @staticmethod
    def _listToStr(list, delimiter):
        result = ''
        if list:
            for element in list:
                result += str(element) + delimiter
            result = result[:-1]

        return result

    @staticmethod
    def _listToInt(list, default_value=0):
        result = default_value
        if list and len(list) == 1:
            result = int(list[0])

        return result

    @staticmethod
    def _strToDict(str, delimiter=' '):
        dict = {}
        list = str.split(delimiter)
        for entry in list:
            entryList = entry.split(':')
            if len(entryList) == 2:
                dict[entryList[0]] = entryList[1]

        return dict

    @staticmethod
    def getJobs():
        resultJobs = []
        p = PBSQuery()

        try:
            jobs = p.getjobs()
            for jobId, pbsJob in jobs.items():
                customJob = Job(jobId)
                try:
                    customJob.state = TorqueService._listToStr(pbsJob[pbs.ATTR_state], '|')
                except KeyError:
                    pass
                try:
                    customJob.user = TorqueService._listToStr(pbsJob[pbs.ATTR_owner], '|')
                except KeyError:
                    pass
                try:
                    customJob.queue = TorqueService._listToStr(pbsJob[pbs.ATTR_queue], '|')
                except KeyError:
                    pass
                try:
                    customJob.name = TorqueService._listToStr(pbsJob[pbs.ATTR_name], '|')
                except KeyError:
                    pass
                try:
                    customJob.cpu_time = TorqueService._listToStr(pbsJob[pbs.ATTR_l]['walltime'], '|')
                except KeyError:
                    pass
                try:
                    customJob.n_p = TorqueService._listToStr(pbsJob[pbs.ATTR_l]['neednodes'], '|') + '/' +\
                                    TorqueService._listToStr(pbsJob[pbs.ATTR_l]['nodes'], '|')
                except KeyError:
                    pass
                try:
                    customJob.setQueued(TorqueService._listToStr(pbsJob[pbs.ATTR_qtime], '|'))
                except KeyError:
                    pass
                try:
                    customJob.setStarted(TorqueService._listToStr(pbsJob[pbs.ATTR_start_time], '|'))
                except KeyError:
                    pass
                try:
                    customJob.running_time = TorqueService._listToStr(pbsJob[pbs.ATTR_used]['walltime'], '|')
                except KeyError:
                    pass

                resultJobs.append(customJob)
        except PBSError as pbsErr:
            print(pbsErr)

        return resultJobs

    @staticmethod
    def getModelServers():
        resultServers = []
        pQuery = PBSQuery()

        try:
            servers = pQuery.get_serverinfo()
            for serverName, pbsServer in servers.items():
                customServer = PBSServer(name=serverName)
                try:
                    customServer.state = TorqueService._listToStr(pbsServer[pbs.ATTR_status], '|')
                except KeyError:
                    pass
                try:
                    customServer.total_jobs = TorqueService._listToInt(pbsServer[pbs.ATTR_total])
                except KeyError:
                    pass
                try:
                    customServer.running_jobs = int(TorqueService._strToDict(pbsServer[pbs.ATTR_count][0])['Running'])
                except KeyError:
                    pass
                try:
                    customServer.queued_jobs = int(TorqueService._strToDict(pbsServer[pbs.ATTR_count][0])['Queued'])
                except KeyError:
                    pass
                try:
                    customServer.pbs_version = TorqueService._listToStr(pbsServer[pbs.ATTR_pbsversion], '|')
                except KeyError:
                    pass

                resultServers.append(customServer)
        except PBSError as pbsErr:
            print(pbsErr)

        return resultServers

    @staticmethod
    def getModelQueues(pbsServer):
        resultQueues = []
        pQuery = PBSQuery()

        try:
            queues = pQuery.getqueues()
            for queueName, pbsQueue in queues.items():
                customQueue = PBSQueue(server=pbsServer, name=queueName)
                #                customQueue.server=pbsServer
                #                customQueue.name=queueName
                try:
                    customQueue.type = TorqueService._listToStr(pbsQueue['queue_type'], '|')
                except KeyError:
                    pass
                try:
                    customQueue.total_jobs = TorqueService._listToInt(pbsQueue[pbs.ATTR_total])
                except KeyError:
                    pass
                try:
                    customQueue.running_jobs = int(TorqueService._strToDict(pbsQueue[pbs.ATTR_count][0])['Running'])
                except KeyError:
                    pass
                try:
                    customQueue.queued_jobs = int(TorqueService._strToDict(pbsQueue[pbs.ATTR_count][0])['Queued'])
                except KeyError:
                    pass
                try:
                    customQueue.resource_walltime = TorqueService._listToStr(pbsQueue[pbs.ATTR_rescdflt]['walltime'],
                        '|')
                except KeyError:
                    pass
                try:
                    customQueue.resource_nodes = TorqueService._listToInt(pbsQueue[pbs.ATTR_rescdflt]['nodes'])
                except KeyError:
                    pass

                resultQueues.append(customQueue)
        except PBSError as pbsErr:
            print(pbsErr)

        return resultQueues

    @staticmethod
    def getModelJobs():
        """
        1. get jobs
        2. get users
        3. map each job to User and Queue
        4. save all jobs
        """
        resultJobs = []
        pQuery = PBSQuery()
        try:
            jobs = pQuery.getjobs()
            for jobName, pbsJob in jobs.items():
                customJob = PBSJob(jobId=jobName)
                try:
                    customJob.name = TorqueService._listToStr(pbsJob[pbs.ATTR_name], '|')
                except KeyError:
                    pass
                try:
                    customJob.owner = TorqueService._listToStr(pbsJob[pbs.ATTR_owner], '|')
                except KeyError:
                    pass
                try:
                    customJob.state = TorqueService._listToStr(pbsJob[pbs.ATTR_status], '|')
                except KeyError:
                    pass
                try:
                    customJob.queue_raw = TorqueService._listToStr(pbsJob[pbs.ATTR_queue], '|')
                except KeyError:
                    pass
                try:
                    customJob.start_time = datetime.fromtimestamp(TorqueService._listToInt(pbsJob[pbs.ATTR_start_time]))
                except KeyError:
                    pass
                try:
                    customJob.resource_cput = TorqueService._listToStr(pbsJob[pbs.ATTR_used]['cput'], '|')
                except KeyError:
                    pass
                try:
                    customJob.resource_mem = TorqueService._listToStr(pbsJob[pbs.ATTR_used]['mem'], '|')
                except KeyError:
                    pass
                try:
                    customJob.resource_vmem = TorqueService._listToStr(pbsJob[pbs.ATTR_used]['vmem'], '|')
                except KeyError:
                    pass
                try:
                    customJob.resource_walltime = TorqueService._listToStr(pbsJob[pbs.ATTR_used]['walltime'], '|')
                except KeyError:
                    pass

                resultJobs.append(customJob)
        except PBSError as pbsErr:
            print(pbsErr)

        return resultJobs

    @staticmethod
    def mapJobsToQueue(pbsQueues, pbsJobs):
        for pbsJob in pbsJobs:
            for pbsQueue in pbsQueues:
                if pbsQueue.name == pbsJob.queue_raw:
                    pbsJob.queue = pbsQueue
                    break

    @staticmethod
    def mapJobsToUser(users, pbsJobs):
        for pbsJob in pbsJobs:
            for user in users:
                if user.username == pbsJob.owner.split('@')[0]:
                    pbsJob.user = user
                    break


    @staticmethod
    def submitScript(script):
        result = {}
        try:
            pbs_connection = pbs.pbs_connect(pbs.pbs_default())
            #    queues = pbs.pbs_statque(pbs_connection, "batch", "NULL", "NULL")

            attropl = pbs.new_attropl(4)

            # Set the name of the job
            #
            attropl[0].name = pbs.ATTR_N
            attropl[0].value = str(script['jobName']) if script['jobName'] else "new_job"

            # Job is Rerunable
            #
            attropl[1].name = pbs.ATTR_r
            attropl[1].value = 'y'

            # Walltime
            #
            attropl[2].name = pbs.ATTR_l
            attropl[2].resource = 'walltime'
            attropl[2].value = str(script['maxTime']) if script['maxTime'] else '01:00:00'

            # Nodes
            #
            attropl[3].name = pbs.ATTR_l
            attropl[3].resource = 'nodes'
            attropl[3].value = str(script['cpuNumber']) if script['cpuNumber'] else '1'


            # A1.tsk is the job script filename
            #
            job_id = pbs.pbs_submit(pbs_connection, attropl, str(script['scriptName']), '', 'NULL')

            e, e_txt = pbs.error()
            if e:
                result['Result'] = 'ERROR'
                result['Message'] = e_txt
            else:
                result['Result'] = 'OK'
                result['Message'] = job_id
        except Exception as exc:
            result['Result'] = 'ERROR'
            result['Message'] = str(exc)

        return result


if __name__ == "__main__":
#    servers = TorqueService.getModelServers()
#    for server in servers:
#        queues = TorqueService.getModelQueues(server)
#        for queue in queues:
#            print queue.name
#            print queue

    pQuery = PBSQuery()
    attr = list()
    attr.append(pbs.ATTR_used)
    jobs = pQuery.getjobs(attr)
    #    for jobName, job in jobs.items():
    #        jobDate = datetime.fromtimestamp(TorqueService._listToInt(job[pbs.ATTR_start_time]))
    #        print jobDate
    #        print time.localtime(int(job['start_time'][0]))
    print(jobs.items())
