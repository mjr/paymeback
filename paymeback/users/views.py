import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from paymeback.core.http import JSONResponseCustom
from paymeback.core.parsers import CamelCaseJSONParserCustom

from .models import User
from .serializers import RegisterSerializer, UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TokenView(OAuthLibMixin, View):
    renderer = CamelCaseJSONRenderer

    def _get_serializer_class(self):
        return UserSerializer

    def _render_data(self, data):
        return self.renderer().render(data).decode('utf-8')

    def _get_response(self, content, status, headers):
        if type(content) == str:
            content = self._render_data(json.loads(content))

        response = HttpResponse(content=content, status=status)

        for k, v in headers.items():
            response[k] = v

        return response

    def _update_request_middleware(self, request):
        new_body = json.loads(request.body.decode('utf-8'))
        new_body['grant_type'] = 'password'
        request._body = JSONRenderer().render(new_body)

    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request, *args, **kwargs):
        self._update_request_middleware(request)

        url, headers, body, status = self.create_token_response(request)

        data = json.loads(request.body.decode('utf-8'))
        if (
            'username' in data
            and not User.objects.filter(username=data['username']).exists()
        ):
            return self._get_response(
                self._render_data(
                    {
                        'error': 'email_not_exists',
                        'error_description': 'Invalid credentials given.',
                    }
                ),
                status,
                headers,
            )

        if status == 200:
            dict_body = json.loads(body)
            access_token = dict_body.get('access_token')
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)

                serializer_class = self._get_serializer_class()
                serializer = serializer_class(token.user, context=dict_body)
                body = self._render_data({'user': serializer.data})

        return self._get_response(body, status, headers)


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(OAuthLibMixin, View):
    renderer = CamelCaseJSONRenderer

    def _get_serializer_class(self):
        return UserSerializer

    def _render_data(self, data):
        return self.renderer().render(data).decode('utf-8')

    def _get_response(self, content, status, headers):
        if type(content) == str:
            content = self._render_data(json.loads(content))

        response = HttpResponse(content=content, status=status)

        for k, v in headers.items():
            response[k] = v

        return response

    def _update_request_middleware(self, request):
        new_body = json.loads(request.body.decode('utf-8'))
        new_body['grant_type'] = 'password'
        request._body = JSONRenderer().render(new_body)

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        self._update_request_middleware(request)

        data = CamelCaseJSONParserCustom().parse(request)
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return JSONResponseCustom(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()

        url, headers, body, status = self.create_token_response(request)

        if status == 200:
            dict_body = json.loads(body)
            access_token = dict_body.get('access_token')
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)

                serializer_class = self._get_serializer_class()
                serializer = serializer_class(token.user, context=dict_body)
                body = self._render_data({'user': serializer.data})

        return self._get_response(body, status, headers)
