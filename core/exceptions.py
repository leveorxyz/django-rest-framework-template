from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

from .views import set_user_ip


def recursive_error_message_creator(error_dict):
    """
    Recursively creates a string from a dictionary of errors.
    """
    if isinstance(error_dict, list):
        return " ".join([error.__str__() for error in error_dict])
    message_list = ""
    for k, v in error_dict.items():
        if isinstance(v, str):
            message_list += v
        else:
            if message_list != "":
                message_list += " "
            message_list += f"{k}: {recursive_error_message_creator(v)}"
    return message_list


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    set_user_ip(context["request"])
    if response:
        data = response.data
        message_list = []
        if isinstance(data, dict):
            message_list.append(recursive_error_message_creator(data))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    message_list.append(item)
                elif isinstance(item, ErrorDetail):
                    message_list.append(item.__str__())
        custom_response = {
            "status_code": response.status_code,
            "message": " ".join(message_list),
            "result": None,
        }
        response.data = custom_response
    return response


# base exception
class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
