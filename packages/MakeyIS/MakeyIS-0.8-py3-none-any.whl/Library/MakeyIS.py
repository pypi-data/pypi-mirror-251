import pytest
import functools
import logging
import allure
import threading
import pdb
from typing import Any, Callable, Tuple, Optional

tests_queue = {}


def Queue(q: int):
    def decorator(func):
        tests_queue[func.__name__] = q
        return func

    return decorator


def run_with_timeout(func: Callable, args: Tuple[Any, ...], kwargs: dict, timeout: int) -> Any:
    result: Optional[Any] = None
    exception: Optional[Exception] = None

    def wrapper():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return "timeout"
    if exception is not None:
        raise exception
    return result


def Mark(mark_name):
    def decorator(func):
        if not hasattr(func, "pytestmark"):
            func.pytestmark = []
        func.pytestmark.append(pytest.mark.custom(mark_name))
        return func

    return decorator


@pytest.fixture(scope="function")
def iteration(request):
    return getattr(request, 'param', None)


def Test(run_test=True, repetitions=1, group_name="default", log=False, description=None, debug=False):
    def decorator(func):
        if not run_test:
            return pytest.mark.skip(reason="Тест пропущен на основе параметра run_test")(func)

        if repetitions > 1:
            func = pytest.mark.parametrize("iteration", range(repetitions))(func)

        func = pytest.mark.group(group_name)(func)

        if description:
            func = AllureDescription(func, description)

        if log:
            func = Log(func)

        if debug:
            func = DebugConditionally(True)(func)

        return func

    return decorator


def Log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.info(f"Начало теста {func.__name__}")
        with allure.step(f"Начало теста {func.__name__}"):
            try:
                result = func(*args, **kwargs)
                logger.info(f"Успешное завершение теста {func.__name__}")
                with allure.step(f"Успешное завершение теста {func.__name__}"):
                    return result
            except Exception as e:
                logger.error(f"Ошибка в тесте {func.__name__}: {e}", exc_info=True)
                with allure.step(f"Ошибка в тесте {func.__name__}"):
                    allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
                raise
            finally:
                logger.removeHandler(console_handler)

    return wrapper


def AllureDescription(func, description):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        allure.dynamic.description(description)
        return func(*args, **kwargs)

    return wrapper


def DebugConditionally(enabled=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if enabled:
                print("Запуск отладчика...")
                pdb.set_trace()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def pytest_collection_modifyitems(session, config, items):
    sorted_items = sorted(items, key=lambda item: tests_queue.get(item.name, float('inf')))
    items[:] = sorted_items
