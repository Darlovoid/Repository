import time


class OperationLogger:
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        print(f"\n>>> Начало операции: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.perf_counter() - self.start_time
        if exc_type is None:
            print(f"<<< Операция '{self.operation_name}' завершена за {elapsed:.4f} сек.")
        else:
            print(f"<<< Операция '{self.operation_name}' завершена с ошибкой "
                  f"{exc_type.__name__}: {exc_value}")
        return False