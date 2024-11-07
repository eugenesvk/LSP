from __future__ import annotations
from typing import Any
import traceback
import inspect
import sublime


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
    file_name = file_name[len(sublime.packages_path()) + len("/LSP/"):]
    debug(f"TRACE {function_name:<32} {file_name}:{line_number}")


def exception_log(message: str, ex: Exception) -> None:
    print(message)
    ex_traceback = ex.__traceback__
    print(''.join(traceback.format_exception(ex.__class__, ex, ex_traceback)))


def printf(*args: Any, prefix: str = 'LSP') -> None:
    """Print args to the console, prefixed by the plugin name."""
    print(prefix + ":", *args)


def notify(window: sublime.Window, message: str, status: str = 'LSP: see console log…') -> None:
    """Pick either of the 2 ways to show a message:
      - via a blocking modal dialog
      - via a detailed console message and a short status message"""
    from .settings import userprefs
    if userprefs().suppress_error_dialogs:
        window.status_message(status)
        print(message)
    else:
        window.message_dialog(message)


def notify_error(window: sublime.Window, message: str, status: str = '❗LSP: see console log…') -> None:
    """Pick either of the 2 ways to show a message:
      - via a blocking modal dialog
      - via a detailed console message and a short status message"""
    from .settings import userprefs
    if userprefs().suppress_error_dialogs:
        window.status_message(status)
        print(message)
    else:
        sublime.error_message(message)
    show_popup_count(window.active_view(),"LSP: see console log…")

from sublime import active_window, PopupFlags

CFG = dict(
     enable     = True
    ,prefix     = '❗'
    ,template   = '''<body id="nv_motion_count"><span>{prefix}{count}</span></body>'''
    ,maxwidth   = 80
    ,maxheight  = 30
)
def get_popup_html(sym) -> str:
    return CFG['template'].format_map(dict(prefix=CFG['prefix'],count=sym))

def show_popup_count(view:sublime.View, sym:str, point:int=-1) -> None:
    view.show_popup(
      content       = get_popup_html(sym)                   # str
      , flags       = PopupFlags.HIDE_ON_CHARACTER_EVENT    #
      , location    = point                                 # Point -1
      , max_width   = 420                       # DIP
      , max_height  = 30                      # DIP
    )
