from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
import getpass
import logging

from pytorque import strings

server_logger = logging.getLogger('pytorque.custom')

def is_allowed_user(orig_func):
    def _decorated(request, username=None):
        if request:
            if username:
                if request.user.username == username:
                    return orig_func(request)
            else:
                return HttpResponseRedirect("/pytorque/login")

        return HttpResponseForbidden()

    return _decorated


@login_required
@is_allowed_user
def index(request, username=None):
    username = getpass.getuser()
    return render_to_response('pytorque/index.html', RequestContext(request, {'userName': username}))


def login(request):
    state = strings.STR_LOGIN_GREETING
    userName = password = ''
    if request.POST:
        userName = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=userName, password=password)
        server_logger.info("User '%s' has logged in." % userName)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                request.session['userPWD'] = password
                next = '/pytorque/user/' + userName
                response = HttpResponseRedirect(next)
                return response
            else:
                state = strings.STR_LOGIN_INACTIVE
        else:
            state = strings.STR_LOGIN_WRONG_CREDENTIAL

    return render_to_response('registration/login.html', RequestContext(request, {'state': state, 'username': userName,
                                                                                  'next': request.GET.get('next')}))


def logout(request):
    userName = request.user.username

    auth.logout(request)
    server_logger.info("User '%s' has logged out." % userName)

    return render_to_response('registration/logout.html', RequestContext(request))
