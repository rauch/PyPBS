import os
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
from pytorque import strings
from pytorque.libs.file_node import FileNode

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
    username = getpass.getuser()
    return render_to_response('pytorque/index.html', RequestContext(request, {'userName': username}))


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
    userName = request.user.username
    return render_to_response('pytorque/browse.html',
        RequestContext(request, {'userName': userName}))


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

#@login_required
#@is_allowed_user
#def fileUpload(request):
#    userName = request.user.username
#
#    jsonTree = {}
#    try:
#        jsonTree = DirectoryNode.getFileTreeJSON(userName, userPWD)
#    except errors.ShellException as shExc:
#        server_logger.error(strings.STR_SHELL_EXCEPTION_MSG % ('getting file tree JSON', str(shExc)))
#    except errors.ParseException as pExc:
#        server_logger.error(strings.STR_PARSE_SHELL_EXCEPTION_MSG % ('getting file tree JSON', str(pExc)))
#
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
#        currentDirectory = request.POST.get('currentDirectory')
#        if form.is_valid():
#            uploadedFile = request.FILES['file']
#            fileName = uploadedFile.name
#            destinationPath = '%s/%s' % (MEDIA_ROOT, fileName)
#
#            try:
#                UploadHandler.handleUploadedFile(destinationPath, uploadedFile)
#            except Exception as exc:
#                server_logger.error(
#                    strings.STR_HANDLE_FILE_EXCEPTION_MSG % ('handling upload file: ' + destinationPath, str(shExc)))
#
#            #copies uploaded file to user's selected directory
#            shellExecutor = ShellCommandExecutor()
#            try:
#                resultExecutionDict = shellExecutor.shellCommand(userName, userPWD,
#                    shellExecutor.STR_CMD_COPY_FILE + destinationPath + " " +\
#                    currentDirectory + "/" + fileName)
#            except errors.ShellException as shExc:
#                server_logger.error(strings.STR_SHELL_EXCEPTION_MSG % ('copying', str(shExc)))
#                #removes temp file
#            try:
#                os.remove(destinationPath)
#            except OSError as osErr:
#                server_logger.error(str(shExc))
#
#            if resultExecutionDict['success']:
#                return HttpResponseRedirect('/webtorque/browse')
#            else:
#                form = UploadFileForm()
#                server_logger.error(resultExecutionDict['result'])
#        else:
#            form = UploadFileForm()
#    else:
#        form = UploadFileForm()
#    return render_to_response('webtorque/fileUpload.html', RequestContext(request, {'jsonTree': jsonTree, 'form': form,
#                                                                                    'currentDirectory': currentDirectory}))

@login_required
@is_allowed_user
def fileDownload(request, username=None):
    if request.method == 'POST':
        fileName = request.POST.get('currentFile')
        server_logger.info("User '%s' is trying to download file: %s" % (username, fileName))

        try:
            fileToSend = file(fileName, 'r')

            wrapper = FileWrapper(fileToSend)
            response = HttpResponse(wrapper) #, content_type='text/plain')
            response['Content-Length'] = os.path.getsize(fileName)
            response['Content-Disposition'] = 'attachment; filename=' + fileToSend.name
            return response
        except IOError as ioError:
            server_logger.error(
                strings.STR_IO_EXCEPTION_MSG % ("opening file", fileName) + str(ioError))

            return HttpResponse("Something goes wrong1!")
    return HttpResponse("Something goes wrong2!")
