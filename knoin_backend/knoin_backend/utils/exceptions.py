import logging
from django.db import DatabaseError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文（包含request和view对象）
    :return: Response响应对象
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        # 数据库异常
        if isinstance(exc, DatabaseError):
            logger.error('[{}] {}'.format(context['view'], exc))
            response = Response(exc.args[-1], status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
