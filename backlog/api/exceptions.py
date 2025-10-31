# backlog/api/exceptions.py
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    resp = exception_handler(exc, context)
    if resp is None:
        return resp
    data = resp.data

    error = {"code": None, "detail": None, "fields": None}

    if isinstance(data, dict):
        error["detail"] = data.get("detail")
        fields = {k: v for k, v in data.items() if k != "detail"}
        error["fields"] = fields or None
    elif isinstance(data, list):
        error["detail"] = "; ".join(map(str, data))

    resp.data = {"ok": False, "error": error}
    return resp
