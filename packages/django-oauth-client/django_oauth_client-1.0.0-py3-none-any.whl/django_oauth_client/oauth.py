#  _____      _                         _      _____ _____
# /  ___|    | |                       | |    |_   _|_   _|
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/
"""
Main module for OAuth integration into Django applications
"""
import datetime
import json
import logging

from authlib.integrations.django_client import OAuth
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from .settings import oauth_settings
from .verify_token import VerifyToken

logger = logging.getLogger(__name__)

oauth = OAuth()
oauth.register(
    name='keycloak',
    server_metadata_url=oauth_settings.oauth_metadata_url,
    client_id=oauth_settings.oauth_client_id,
    client_secret=oauth_settings.oauth_client_secret,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def protected(roles: list = None):
    """
    Protect endpoints with role assignment (optional)
    """

    def inner(f):  # pylint: disable=invalid-name
        """
        Inner decorator to store 'roles' in this function object
        """

        def wrapper(request, *args, **kwargs):  # pylint: disable=r0911
            """

            """
            if request.headers.get('Authorization', None):
                logger.info("API login! Parsing API token")

                token = request.META.get('HTTP_AUTHORIZATION', '').replace(
                    'Bearer', '').strip()

                profile = VerifyToken(token=token).verify(roles=roles)
                if not isinstance(profile, dict):
                    return HttpResponse(status=401,
                                        content=json.dumps({"status": "error", "message": "Unexpected response from Token verification"}))
                if "status" in profile.keys() and profile.get(
                        "status") == "error":
                    return HttpResponse(status=401,
                                        content=json.dumps({"status": "error", "message": "Unexpected response from Token verification"}))

                return f(request, *args, **kwargs)

            try:
                user = json.loads(
                    request.COOKIES.get('user')) if request.COOKIES.get(
                    'user') else None
            except Exception as exception:
                logger.warning(f"Unable to parse user cookie into dictionary: '{str(exception)}'")
                return redirect("/login/")

            if user:
                if roles:
                    for role in roles:
                        if role in user.get('roles'):
                            return f(request, *args, **kwargs)
                        return HttpResponse('You are not allowed to '
                                            'access this page due to missing '
                                            'role assignment. Speak to your '
                                            'admin if you believe this is a '
                                            'mistake', status=401)
                return f(request, *args, **kwargs)

            return redirect('/login/')

        return wrapper

    return inner


def login(request):
    """

    :param request:
    :return:
    """

    redirect_uri = request.build_absolute_uri(reverse('auth'))

    token = bool(request.GET.get("token", False))
    if token:
        redirect_uri = redirect_uri + "?token=true"
    return oauth.keycloak.authorize_redirect(request, redirect_uri)


def auth(request):
    """

    :param request:
    :return:
    """
    deliver_token = bool(request.GET.get("token", False))
    token = oauth.keycloak.authorize_access_token(request)

    if deliver_token:
        expiry = datetime.datetime.fromtimestamp(token.get('expires_at'))
        data = {"status": "success", "token": token["access_token"],
                "expires": expiry}

        response = JsonResponse(data, status=200)
    else:
        response = HttpResponseRedirect("/")
    response.set_cookie('user', json.dumps(token['userinfo']))

    return response


def logout(request):
    """

    :param request:
    :return:
    """
    # response = HttpResponseRedirect("/")
    response = HttpResponse("You have been logged out!!"
                            '<a href="/">Back to home</a>')
    if request.COOKIES.get('user'):
        response.delete_cookie('user')
    return response
