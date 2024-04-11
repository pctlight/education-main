import os
import logging
import sys
import time
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Определяем путь к текущему каталогу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Загружаем конфигурацию логгера из файла
logging.config.fileConfig(os.path.join(current_dir, 'logging_config.ini'))
output_log = logging.getLogger("output")

client_host: ContextVar[str | None] = ContextVar("client_host", default=None)

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        try:
            client_host.set(request.client.host)
            start_time = time.time()

            # Вызываем следующую прослойку или обработчик маршрута
            response = await call_next(request)

            # Вычисляем время выполнения запроса
            elapsed_time = time.time() - start_time

            # Логируем информацию о запросе и ответе
            output_log.info(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {{{__file__}: {sys._getframe().f_lineno}}} INFO - | {elapsed_time:.2f} | {request.method} | {request.url} | {response.status_code} |"
            )

            return response
        except Exception as e:
            # Если произошла ошибка, возвращаем код 500 и логируем ошибку
            output_log.error(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {{{__file__}: {sys._getframe().f_lineno}}} ERROR - An error occurred: {e}"
            )
        return Response("Internal Server Error", status_code=500)