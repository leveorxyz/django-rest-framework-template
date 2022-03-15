from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.mixins import CustomListUpdateModelMixin, CustomListModelMixin
from .utils import set_user_ip

# Create your views here.


def custom_response(response):
    response_data = {
        "message": "success",
        "status_code": response.status_code,
        "result": response.data,
    }
    response.data = response_data
    return response


class CustomRetrieveAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomListUpdateAPIView(
    GenericAPIView, CustomListModelMixin, CustomListUpdateModelMixin
):
    pagination_class = None

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def delete(self, request, *args, **kwargs):
        set_user_ip(request)
        return super().delete(request, *args, **kwargs)


class CustomCreateAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomListAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomListCreateAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def delete(self, request, *args, **kwargs):
        set_user_ip(request)
        return super().delete(request, *args, **kwargs)


class CustomDestroyAPIView(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        set_user_ip(request)
        return super().delete(request, *args, **kwargs)


class CustomUpdateAPIView(UpdateAPIView):
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        set_user_ip(request)
        return custom_response(response)


class CustomAPIView(APIView):
    http_method_names = ["get", "post", "patch", "put", "delete", "head", "options"]

    def get(self, request, response_data=None, *args, **kwargs):
        if not response_data:
            response_data = {}
        response = Response(response_data)
        return custom_response(response)

    def post(self, request, response_data=None, *args, **kwargs):
        return self.get(request, response_data, *args, **kwargs)

    def patch(self, request, response_data=None, *args, **kwargs):
        return self.get(request, response_data, *args, **kwargs)

    def put(self, request, response_data=None, *args, **kwargs):
        return self.get(request, response_data, *args, **kwargs)

    def delete(self, request, response_data=None, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
