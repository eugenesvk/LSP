from __future__ import annotations
from .constants import ST_PACKAGES_PATH
from typing import Any
import traceback
import inspect


log_debug = False


def set_debug_logging(logging_enabled: bool) -> None:
    global log_debug
    log_debug = logging_enabled


def debug(*args: Any) -> None:
    """Print args to the console if the "debug" setting is True."""
    if log_debug:
        printf(*args)


def trace() -> None:
    current_frame = inspect.currentframe()
    if current_frame is None:
        debug("TRACE (unknown frame)")
        return
    previous_frame = current_frame.f_back
    file_name, line_number, function_name, _, _ = inspect.getframeinfo(previous_frame)  # type: ignore
    file_name = file_name[len(ST_PACKAGES_PATH) + len("/LSP/"):]
    debug(f"TRACE {function_name:<32} {file_name}:{line_number}")


def exception_log(message: str, ex: Exception) -> None:
    print(message)
    ex_traceback = ex.__traceback__
    print(''.join(traceback.format_exception(ex.__class__, ex, ex_traceback)))


def printf(*args: Any, prefix: str = 'LSP') -> None:
    """Print args to the console, prefixed by the plugin name."""
    print(prefix + ":", *args)


def notify(msg: str, status: str = '⚠️LSP: see console log…') -> None:
    """Pick either of the 2 ways to show a message:
      - via a blocking modal dialog
      - via a detailed console message and a short status message"""
    from .settings import userprefs
    if userprefs().show_ui_blocking_message:
        sublime.message_dialog(msg)
    else:
        sublime.status_message(status)
        print(msg)


def notify_err(msg: str, status: str = '❗LSP: see console log…') -> None:
    """Pick either of the 2 ways to show a message:
      - via a blocking modal dialog
      - via a detailed console message and a short status message"""
    from .settings import userprefs
    if userprefs().show_ui_blocking_err_message:
        sublime.message_dialog(msg)
    else:
        sublime.error_message(status)
        print(msg)
