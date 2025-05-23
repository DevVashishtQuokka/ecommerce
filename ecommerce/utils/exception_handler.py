from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from utils.responder import Responder 

def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    view_name = context.get('view', context).__class__.__name__

    if response is not None:
        detail = response.data.get("detail", None)
        if detail:
            message = str(detail)
            errors = {"detail": detail}
        else:
            message = "Validation failed"
            errors = response.data

        return Responder.error_response(
            code=4000, 
            errors=errors,
            status_code=response.status_code
        )

    return Responder.error_response(
        code=5000,  
        errors={"error": str(exc)},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
