import json as simplejson

import django

from django.core.serializers import serialize
from django.http import HttpResponse
from django.utils.functional import Promise
from django.utils.encoding import force_text


class LazyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return obj


class JSONResponse(HttpResponse):
    """
    A simple subclass of ``HttpResponse`` which makes serializing to JSON easy.
    """
    def __init__(self, object, is_iterable=True):
        if is_iterable:
            content = serialize('json', object)
        else:
            content = simplejson.dumps(object, cls=LazyEncoder)
        if django.VERSION > (1, 5):
            kwargs = {
                'content_type': 'application/json',
            }
        else:
            kwargs = {
                'mimetype': 'application/json',
            }
        super(JSONResponse, self).__init__(content, **kwargs)


class XMLResponse(HttpResponse):
    """
    A simple subclass of ``HttpResponse`` which makes serializing to XML easy.
    """
    def __init__(self, object, is_iterable=True):
        if is_iterable:
            content = serialize('xml', object)
        else:
            content = object
        if django.VERSION > (1, 5):
            kwargs = {
                'content_type': 'application/xml',
            }
        else:
            kwargs = {
                'mimetype': 'application/xml',
            }
        super(XMLResponse, self).__init__(content, **kwargs)
