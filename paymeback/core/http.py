from django.http import HttpResponse

from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class JSONResponseCustom(HttpResponse):
    def __init__(self, data, **kwargs):
        content = CamelCaseJSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super().__init__(content, **kwargs)
