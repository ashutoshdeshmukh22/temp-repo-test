import logging

logger = logging.getLogger(__name__)

def error(msg=""):
    if not msg:
        msg = "There was error Processing request"
    data = {
        "status": "error",
        "message": msg,
    }
    return data

def logerror(request=None, msg=""):
    if request:
        user_info = f"User ID: {request.user.id}, Username: {request.user.username}" if request.user.is_authenticated else "Anonymous User"
        logger.exception("An exception occurred. User: %s. Exception: %s", user_info, str(msg))
    else:
        logger.exception("Exception: %s", str(msg))
