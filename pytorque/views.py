import os
import string
import urlparse
from django.core.servers.basehttp import FileWrapper
from django.utils.translation import ugettext as _
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.http import  HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import getpass
import logging
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
import jsonpickle
import time
from pytorque import strings
from pytorque.forms import UploadFileForm, SubmitScriptForm
from pytorque.libs.file_node import FileNode
from pytorque.libs.torque_service import TorqueService
from pytorque.libs.upload_handler import UploadHandler
from pytorque.models import FileObject

import settings

server_logger = logging.getLogger('pytorque.custom')

ROOT_URL = "/"


def is_allowed_user(orig_func):
    def _decorated(request, username=None):
        if username:
            if request.user.username == username:
                return orig_func(request, username)
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()

    return _decorated


@login_required
@is_allowed_user
def index(request, username=None):
    return render_to_response('pytorque/index.html',
        RequestContext(request, {'userName': username, 'py_userName': getpass.getuser()}))


def central_dispatch_view(request):
    if request.user and request.user.is_authenticated():
        requestedPath = request.get_full_path()
        return HttpResponseRedirect(ROOT_URL + "user/" + request.user.username + requestedPath)
    else:
        return HttpResponseRedirect(ROOT_URL + "login/")


@csrf_protect
@never_cache
def login(request, template_name='registration/login_reg.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            request.session['userPWD'] = form.cleaned_data['password']

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
        context_instance=RequestContext(request, current_app=current_app))


def logout(request, next_page=None,
           template_name='registration/logged_out_reg.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            return HttpResponseRedirect(redirect_to)

    if next_page is None:
        current_site = get_current_site(request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Logged out')
        }
        context.update(extra_context or {})
        return render_to_response(template_name, context,
            context_instance=RequestContext(request, current_app=current_app))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)


@login_required
@is_allowed_user
def browse(request, username=None):
    return render_to_response('pytorque/browse.html',
        RequestContext(request, {'userName': username, 'py_userName': getpass.getuser()}))


@login_required
@is_allowed_user
def get_children(request, username=None):
    resultJSON = {}

    if request.method == 'GET':
        selectedNodeId = request.GET.get('id')
        if selectedNodeId:
            nodeId = selectedNodeId
        else:
            nodeId = "/home/" + username

        fileNode = FileNode.createDirectoryNode(nodeId)
        resultJSON = jsonpickle.encode(fileNode, unpicklable=False)

    return HttpResponse(resultJSON, content_type="application/json")


@login_required
@is_allowed_user
def fileUpload(request, username=None):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        destinationPath = request.POST.get('currentDirectory')
        if form.is_valid() and destinationPath:
            uploadedFile = request.FILES['file']

            server_logger.info("User '%s' is trying to upload file: %s" % (username, uploadedFile.name))
            try:
                UploadHandler.handle(destinationPath, uploadedFile)

                #                userFile = FileObject(user = request.user, file_name = os.path.join(destinationPath, uploadedFile.name))
                #                userFile.save()

                FileObject.objects.create(user=request.user, file_name=os.path.join(destinationPath, uploadedFile.name))
            except Exception as exc:
                server_logger.error(
                    strings.STR_HANDLE_FILE_EXCEPTION_MSG % ('uploading file: ' + uploadedFile.name, str(exc)))

            return HttpResponseRedirect('/user/' + username + '/browse')

        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render_to_response('pytorque/upload.html', RequestContext(request, {'userName': username, 'form': form,
                                                                               'currentDirectory': destinationPath}))


@login_required
@is_allowed_user
def fileDownload(request, username=None):
    if request.method == 'POST':
        fileName = request.POST.get('currentFile')
        server_logger.info("User '%s' is trying to download file: %s" % (username, fileName))

        try:
            fileToSend = file(fileName, 'r')

            wrapper = FileWrapper(fileToSend)
            response = HttpResponse(wrapper, content_type="application/force-download")
            response['Content-Length'] = os.path.getsize(fileName)
            response['Content-Disposition'] = 'attachment; filename=' + fileToSend.name.encode('utf8')
            return response
        except Exception as exc:
            server_logger.error(strings.STR_IO_EXCEPTION_MSG % ("opening file " + fileName, str(exc)))

    return render_to_response('pytorque/browse.html', RequestContext(request, {'userName': username}))


@login_required
@is_allowed_user
def fileRemove(request, username=None):
    resultDict = {"status": "success", "message": ""}

    if request.POST:
        itemToRemove = request.POST.get('id')
        server_logger.info("User '%s' is trying to remove file: %s" % (username, itemToRemove))

        if itemToRemove:
            if os.path.isfile(itemToRemove):
                try:
                    os.remove(itemToRemove)
                    resultDict["status"] = "success"
                except Exception as exc:
                    server_logger.error(strings.STR_HANDLE_FILE_EXCEPTION_MSG % ('removing file', str(exc)))
                    resultDict["status"] = "error"
                    resultDict["message"] = (strings.STR_HANDLE_FILE_EXCEPTION_MSG % ('removing file', str(exc)))
            else:
                resultDict["status"] = "error"
                resultDict["message"] = "File could be removed only"
        else:
            resultDict["status"] = "error"
            resultDict["message"] = "Item to remove must be selected"
    else:
        resultDict["status"] = "error"
        resultDict["message"] = "Please, use `post` request"

    resultJSON = jsonpickle.encode(resultDict)
    return HttpResponse(resultJSON, content_type="application/json")


@login_required
@is_allowed_user
def monitor(request, username=None):
    return render_to_response('pytorque/monitor.html',
        RequestContext(request, {'userName': username}))


@login_required
@is_allowed_user
def get_jobs(request, username=None):
    resultJSON = {}

    if request.method == 'POST':
        jobs = TorqueService.getJobs()
        resultJSON['Result'] = 'OK'
        resultJSON['Records'] = jobs

    else:
        resultJSON['Result'] = 'ERROR'
        resultJSON['Message'] = 'Use \'POST\' request, please'

    return HttpResponse(jsonpickle.encode(resultJSON, unpicklable=False), content_type="application/json")


@login_required
@is_allowed_user
def submit(request, username=None):
    resultJSON = {}

    if request.method == 'POST':
        form = SubmitScriptForm(request.POST)
        if form.is_valid():
            script = {}

            script['jobName'] = form.cleaned_data['jobName']
            script['queue'] = form.cleaned_data['queueToSubmitJobTo']
            script['cpuNumber'] = form.cleaned_data['cpuToUse']
            script['maxTime'] = form.cleaned_data['maxTime']
            script['sendMessageAbort'] = form.cleaned_data['sendMessageAbort']
            script['sendMessageEnd'] = form.cleaned_data['sendMessageEnd']
            script['sendMessageStart'] = form.cleaned_data['sendMessageStart']
            script['sendMessageTo'] = form.cleaned_data['sendMessageTo']
            script['executionCommands'] = form.cleaned_data['executionCommands']
            script['stageInFrom'] = form.cleaned_data['stageInFrom']
            script['stageInTo'] = form.cleaned_data['stageInTo']
            script['stageOutFrom'] = form.cleaned_data['stageOutFrom']
            script['stageOutTo'] = form.cleaned_data['stageOutTo']

            script['scriptName'] = os.path.join('/home/' + username,
                script['jobName'] + "." + time.strftime("%d.%m.%Y_%H:%M:%S",
                    time.localtime()) + ".pbs")

            #creates file script
            try:
                scriptFile = open(script['scriptName'], 'w', 0744)
                temp = string.replace(script['executionCommands'], '\r\n', '\n')
                temp = string.replace(temp, '\r', '\n')
                scriptFile.write(temp)
            except Exception as err:
                server_logger.error(str(err))
            finally:
                scriptFile.close()

            result = TorqueService.submitScript(script)

            if result["Result"] == "OK":
                return HttpResponseRedirect('/user/' + username + '/monitor')
    else:
        form = SubmitScriptForm()
        resultJSON['Result'] = 'ERROR'
        resultJSON['Message'] = 'Use \'POST\' request, please'

    return render_to_response('pytorque/submit.html',
        RequestContext(request, {'userName': username, 'form': form}))

