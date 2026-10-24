import time
from functools import wraps
from typing import Callable, Any


def log_call(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"[LOG] Вызов: {func.__name__}")
        if args:
            print(f"[LOG]   args: {args[1:] if len(args) > 1 else args}")
        if kwargs:
            print(f"[LOG]   kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG]   -> {result}")
        return result

    return wrapper


def measure_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[PERFORMANCE] {func.__name__}: {elapsed:.4f} сек.")
        return result

    return wrapper


def repeat(count: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = None
            for i in range(count):
                print(f"[REPEAT] Итерация {i + 1}/{count}")
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def require_status(*allowed_statuses) -> Callable:
    from models import Student

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, student: "Student", *args, **kwargs):
            if student.status not in allowed_statuses:
                raise ValueError(
                    f"Операция '{func.__name__}' запрещена для статуса «{student.status.value}»"
                )
            return func(self, student, *args, **kwargs)

        return wrapper

    return decorator