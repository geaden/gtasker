# -*- coding: utf-8 -*-
from functools import wraps
import json

from django.db import models
from django.core import serializers

# Describe nullable field
nullable = {'null': True, 'blank': True}
# Bootstrap attributes
battrs = lambda x: {'class': 'form-control', 'placeholder': x}

# Color choices
COLOR_CHOICES = tuple(enumerate([
        '#CEC5C6',   # 'light-warm-gray',
        '#AD3F98',   # 'dark-pink',
        '#487E4E',   # 'dark-green',
        '#3C67C1',   # 'dark-blue',
        '#C3411E',   # 'dark-red',
        '#8E6460',   # 'dark-teal',
        '#DD7100',   # 'dark-brown',
        '#6341B9',   # 'dark-orange',
        '#483C3D',   # 'dark-purple',
        '#F1B6DE',   # 'dark-warm-gray',
        '#B9D07C',   # 'light-pink',
        '#B6C3DD',   # 'light-green',
        '#EDBDBC',   # 'light-blue',
        '#ACD1EE',   # 'light-red',
        '#FFEE9A',   # 'light-teal',
        '#D5BEE7',   # 'light-yellow',
        '#483C3D',   # 'light-orange',
        '#F8CEA5'    # 'light-purple'
], start=1))


def create_fixture(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        json.dump(serializers.serialize('json', f(*args, **kwargs), indent=4),
                  open('fixtures/test.json'))
    return wrapper
