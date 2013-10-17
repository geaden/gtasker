# -*- coding: utf-8 -*-
from django.http import HttpResponse

from django.views.generic import View


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class SmsReplyView(View):
    def get(self, request, *arg, **kwargs):
        content ="""<Response>
                 <Sms>
                 Thanks for reply. Take care.
                 </Sms>
                 </Response>"""
        return HttpResponse(
            content, content_type='application/xml')