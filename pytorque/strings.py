__author__ = 'rauch'


#Login page
STR_LOGIN_GREETING = "Please log in below: "
STR_LOGIN_SUCCESS = "You're successfully logged in!"
STR_LOGIN_INACTIVE = "Your account is not active, please contact the site admin."
STR_LOGIN_WRONG_CREDENTIAL = "Your name and/or password were incorrect."

#Errors messages
STR_SHELL_EXCEPTION_MSG = "ShellException occurs while %s with: %s"
STR_PARSE_SHELL_EXCEPTION_MSG = "ParseException occurs while %s with: %s"
STR_HANDLE_FILE_EXCEPTION_MSG = "FileHandling error occurs while %s with: %s"
STR_SUBMITTING_FILE_EXCEPTION_MSG = "FileSubmitting error occurs while %s with: %s"

#System errors
STR_UNKNOWN_EXCEPTION_MSG = "Unknown error occurs while %s with: %s"
STR_IO_EXCEPTION_MSG = "IO error occurs while %s with: %s"


#PBS HOST Headers
STR_PBS_HOST_NAME_HEADER = "Host Name"
STR_PBS_HOST_NAME_KEY = "name"
STR_PBS_HOST_STATE_HEADER = "Server State"
STR_PBS_HOST_STATE_KEY = "server_state"
STR_PBS_HOST_TOTAL_QUEUES_HEADER = "Total Queues"
STR_PBS_HOST_TOTAL_QUEUES_KEY = "total_queues"
STR_PBS_HOST_TOTAL_JOBS_HEADER = "Total Jobs"
STR_PBS_HOST_TOTAL_JOBS_KEY = "total_jobs"
STR_PBS_HOST_VERSION_HEADER = "PBS Version"
STR_PBS_HOST_VERSION_KEY = "pbs_version"

#PBS QUEUE Headers
STR_PBS_QUEUE_NAME_HEADER = "Queue Name"
STR_PBS_QUEUE_NAME_KEY = "name"
STR_PBS_QUEUE_TOTAL_JOBS_HEADER = "Total Jobs"
STR_PBS_QUEUE_TOTAL_JOBS_KEY = "total_jobs"
STR_PBS_QUEUE_NODES_NUMBER_HEADER = "Total Nodes"
STR_PBS_QUEUE_NODES_NUMBER_KEY = "resources_default.nodes"
STR_PBS_QUEUE_ENABLED_HEADER = "Enabled"
STR_PBS_QUEUE_ENABLED_KEY = "enabled"
STR_PBS_QUEUE_TYPE_HEADER = "Queue Type"
STR_PBS_QUEUE_TYPE_KEY = "queue_type"
#different properties: walltime and so on

#PBS JOB Headers
STR_PBS_JOB_ID_HEADER = "Job ID"
STR_PBS_JOB_ID_KEY = "Job Id"
STR_PBS_JOB_NAME_HEADER = "Job Name"
STR_PBS_JOB_NAME_KEY = "Job_Name"
STR_PBS_JOB_USER_HEADER = "Owner"
STR_PBS_JOB_USER_KEY = "Job_Owner"
STR_PBS_JOB_STATE_HEADER = "State"
STR_PBS_JOB_STATE_KEY = "job_state"
STR_PBS_JOB_TIME_USE_HEADER = "Time Used"
STR_PBS_JOB_TIME_USE_KEY = "resources_used.walltime"
STR_PBS_JOB_CPU_TIME_USE_HEADER = "CPU Time Used"
STR_PBS_JOB_CPU_TIME_USE_KEY = "resources_used.cput"
STR_PBS_JOB_EXIT_STATUS_HEADER = "Exit Status"
STR_PBS_JOB_EXIT_STATUS_KEY = "exit_status"
