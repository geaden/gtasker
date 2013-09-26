# -*- coding: utf-8 -*-

from .models import TaskerUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class GoogleOAuthBackend(object):
    supports_inactive_user = False

    def authenticate(self, **kwargs):
        """
        Authenticates according to authentication method.
        Whether `password` and `username` provided, or
        `google_user`

        :params kwargs: dictionary with `username` and `password` or `google_user`
            information
        :returns: user
        """
        authenticated = False
        if 'password' and 'username' in kwargs:
            try:
                user = TaskerUser.objects.get_by_natural_key(
                    kwargs.get('username'))
                authenticated = user.check_password(kwargs.get('password'))
            except TaskerUser.DoesNotExist:
                pass
        elif 'google_user' in kwargs:
            google_user = kwargs.get('google_user')
            email = google_user['email']
            try:
                user = TaskerUser.objects.get_by_natural_key(email)
                authenticated = True
            except TaskerUser.DoesNotExist:
                email = google_user['email']
                try:
                    user = TaskerUser.objects.get_by_natural_key(email)
                    authenticated = True
                except TaskerUser.DoesNotExist:
                    pass
        if authenticated:
            return user
        return None

    def get_user(self, user_id):
        try:
            return TaskerUser.objects.get(pk=user_id)
        except TaskerUser.DoesNotExist:
            return None