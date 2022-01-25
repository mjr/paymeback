import json

from django.conf import settings

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.util import underscoreize
from rest_framework.exceptions import ParseError


class CamelCaseJSONParserCustom(CamelCaseJSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)

        try:
            data = stream.body.decode(encoding)
            return underscoreize(json.loads(data), **self.json_underscoreize)
        except ValueError as exc:
            raise ParseError("JSON parse error - %s" % str(exc))
