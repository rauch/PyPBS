import urlparse
from django.utils.translation import ugettext as _
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.http import  HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
import getpass
import logging
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from pytorque import strings
import settings

server_logger = logging.getLogger('pytorque.custom')

HOME_URL = "/pytorque/"


def is_allowed_user(orig_func):
    def _decorated(request, username=None):
        if username:
            if request.user.username == username:
                return orig_func(request)
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
        return HttpResponseRedirect(HOME_URL + "user/" + request.user.username)
    else:
        return HttpResponseRedirect(HOME_URL + "login/")

@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
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
           template_name='registration/logged_out.html',
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
