from use_logger import useLogger, useLoggerInterceptUvicorn
from use_logger.handlers import logstash_handler


def register_logger(packages=None, extra=None, uvicorn=True, **kwargs):
    useLogger(
        handlers=[
            logstash_handler(**kwargs),
        ],
        packages=packages,
        extra=extra
    )
    if uvicorn:
        useLoggerInterceptUvicorn()
