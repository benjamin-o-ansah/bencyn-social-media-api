# users/utils.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        return response

    # For unhandled exceptions, return a friendly JSON
    return Response({
        "error": "Something went wrong. Please try again later.",
        "details": str(exc)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
