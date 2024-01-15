# -*- coding: utf-8 -*-

"""
Alfred Workflow UI simulator.
"""

import typing as T
import time
import subprocess
import dataclasses

import readchar
from blessed import Terminal

from .vendor.os_platform import IS_WINDOWS
from . import exc
from . import events
from .constants import SHOW_ITEMS_LIMIT, SCROLL_SPEED
from .item import T_ITEM, Item
from .line_editor import LineEditor
from .dropdown import Dropdown
from .render import UIRender, T_UI_RENDER
from .debug import debugger
from .ui_process_key_pressed import UIProcessKeyPressedMixin


key_to_name = {
    readchar.key.CTRL_C: "CTRL_C",
    readchar.key.TAB: "TAB",
    readchar.key.CTRL_X: "CTRL_X",
    readchar.key.UP: "UP",
    readchar.key.DOWN: "DOWN",
    readchar.key.CTRL_E: "CTRL_E",
    readchar.key.CTRL_D: "CTRL_D",
    readchar.key.CTRL_R: "CTRL_R",
    readchar.key.CTRL_F: "CTRL_F",
    readchar.key.LEFT: "LEFT",
    readchar.key.RIGHT: "RIGHT",
    readchar.key.HOME: "HOME",
    readchar.key.END: "END",
    readchar.key.CTRL_H: "CTRL_H",
    readchar.key.CTRL_L: "CTRL_L",
    readchar.key.CTRL_G: "CTRL_G",
    readchar.key.CTRL_K: "CTRL_K",
    readchar.key.BACKSPACE: "BACKSPACE",
    readchar.key.DELETE: "DELETE",
    readchar.key.ENTER: "ENTER",
    readchar.key.CR: "CR",
    readchar.key.LF: "LF",
    readchar.key.CTRL_A: "CTRL_A",
    readchar.key.CTRL_W: "CTRL_W",
    readchar.key.CTRL_P: "CTRL_P",
}

if IS_WINDOWS:
    OPEN_CMD = "start"
else:
    OPEN_CMD = "open"


@dataclasses.dataclass
class DebugItem(Item):
    def enter_handler(self, ui: "UI"):
        subprocess.run([OPEN_CMD, str(debugger.path_log_txt)])


T_HANDLER = T.Callable[[str, T.Optional["UI"]], T.List[T_ITEM]]


class UI(
    UIProcessKeyPressedMixin,
):
    """
    Zelfred terminal UI implementation.

    :param handler: the handler is the core of a Zelfred App. It's a user-defined
        function that takes the entered query and the UI object as inputs
        and returns a list of items to render.
    :param handler: a callable function that takes a query string as input and
        returns a list of items.
    :param hello_message: sometimes the handler execution for the first time
        run takes long. This message will be shown to user to indicate that
        the handler is still running, and the UI will show the returned items
        once the handler is done.
    :param capture_error: whether you want to capture the error and show it
        in the UI, or you want to raise the error immediately.
    :param process_input_immediately: the handler will be called immediately
        after user input. This is the default behavior.
    :param process_input_after_query_delay: the handler will be called after
        a delay of `query_delay` seconds after the first user input. For example,
        let's say the query delay is 0.3 second. At begin, the user input is empty,
        then user entered "a". If then the user entered "bcd" within 0.3 second,
        the handler will not be called to give you the latest items. The handler
        will be called until the user entered a new key, let's say "e", from
        0.4 second after he entered "a".
    :param query_delay: read above.
    :param show_items_limit: max number of items to show in the dropdown menu.
    :param scroll_speed: scroll speed in the dropdown menu.

    Additional private attributes:

    :param _handler_queue: user may nest session in another session, this LIFO
        queue stores the handler functions of the parent sessions, so that
        when we exit the inner session and go back to the previous session.
    :param _line_editor_input_queue: similar to ``_handler_queue``, but stores
        the parent sessions' user input queries.
    """

    def __init__(
        self,
        handler: T_HANDLER,
        hello_message: T.Optional[str] = "Welcome to interactive UI!",
        capture_error: bool = True,
        process_input_immediately: bool = False,
        process_input_after_query_delay: bool = False,
        query_delay: float = 0.3,
        show_items_limit: int = SHOW_ITEMS_LIMIT,
        scroll_speed: int = SCROLL_SPEED,
        terminal: T.Optional[Terminal] = None,
        render_class: T.Type[T_UI_RENDER] = UIRender,
    ):
        # -------------------- input arguments
        self.handler: T_HANDLER = handler
        self._handler_queue: T.List[T_HANDLER] = list()
        self._line_editor_input_queue: T.List[str] = list()
        self.hello_message: T.Optional[str] = hello_message
        self.capture_error: bool = capture_error
        self.query_delay: float = query_delay

        # -------------------- internal implementation related
        if terminal is None:
            self.terminal = Terminal()
        else:
            self.terminal = terminal
        self.render: T_UI_RENDER = render_class(terminal=self.terminal)
        self.event_generator = events.KeyEventGenerator()
        self._process_input: T.Callable
        flag = sum(
            [
                process_input_immediately,
                process_input_after_query_delay,
            ]
        )
        if flag == 0:
            process_input_immediately = True
        elif flag > 1:
            raise ValueError
        else:  # pragma: no cover
            pass

        if process_input_immediately:
            self._process_input = self._process_input_v1_immediately
        elif process_input_after_query_delay:
            self._process_input = self._process_input_v2_after_query_delay
        else:  # pragma: no cover
            raise NotImplementedError

        self._create_key_processor_mapper()
        # -------------------- items related --------------------
        self.line_editor: LineEditor = LineEditor()
        self.dropdown: Dropdown = Dropdown(
            items=[],
            show_items_limit=show_items_limit,
            scroll_speed=scroll_speed,
        )
        self.n_items_on_screen: int = 0

        # -------------------- controller flags --------------------
        self.need_run_handler: bool = True
        self.need_move_to_end: bool = True
        self.need_clear_items: bool = True
        self.need_clear_query: bool = True
        self.need_print_query: bool = True
        self.need_print_items: bool = True
        self.need_process_input: bool = True

    def _debug_controller_flags(self):
        print(f"self.need_run_handler = {self.need_run_handler}")
        print(f"self.need_move_to_end = {self.need_move_to_end}")
        print(f"self.need_clear_items = {self.need_clear_items}")
        print(f"self.need_clear_query = {self.need_clear_query}")
        print(f"self.need_print_query = {self.need_print_query}")
        print(f"self.need_print_items = {self.need_print_items}")
        print(f"self.need_process_input = {self.need_process_input}")

    def replace_handler(self, handler: T_HANDLER):
        """
        Replace the current handler with a new handler, and store the
        current handler and the current user input query, so that we can
        recover them when we need.
        """
        self._handler_queue.append(self.handler)
        self._line_editor_input_queue.append(self.line_editor.line)
        self.handler = handler

    def _clear_query(self):
        """
        Clear the ``(Query): {user_query}`` line.
        """
        self.render.clear_line_editor()
        return True

    def clear_query(self):
        """
        A wrapper of the ``_clear_query()`` method, ensures that the
        ``need_clear_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- clear_query --------------------")
        try:
            if self.need_clear_query:
                debugger.log("before clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                self._clear_query()
                debugger.log("after clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_clear_query = True

    def _clear_items(self) -> bool:
        """
        Clear the item dropdown menu.
        """
        if self.render.line_number > 1:
            # time.sleep(1)
            self.render.clear_dropdown()
            # time.sleep(1)
            return True
        else:
            return False

    def clear_items(self):
        """
        A wrapper of the ``_clear_items()`` method, ensures that the
        ``need_clear_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- clear_items --------------------")
        try:
            if self.need_clear_items:
                debugger.log("before clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                flag = self._clear_items()
                debugger.log("after clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                if flag:
                    debugger.log(f"nothing happen")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_clear_items = True

    def _print_query(self):
        """
        Print the ``(Query): {user_query}`` line
        """
        content = self.render.print_line_editor(self.line_editor)
        debugger.log(f"printed: {content!r}")

    def print_query(self):
        """
        A wrapper of the core logic for printing query, ensures that the
        ``need_print_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- print_query --------------------")
        try:
            if self.need_print_query:
                debugger.log("before print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                self._print_query()
                debugger.log("after print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_print_query = True

    def _print_items(self):
        """
        Core logic for printing items in the dropdown menu.
        """
        debugger.log("render dropdown")
        n_items_on_screen = self.render.print_dropdown(
            self.dropdown, self.render.terminal.width
        )
        self.n_items_on_screen = n_items_on_screen

    def print_items(self):
        """
        A wrapper of the core logic for printint items, ensures that the
        ``need_print_items`` and ``need_run_handler`` flag is set to ``True``
        at the end regardless of whether an exception is raised.
        """
        debugger.log("-------------------- print_items --------------------")
        try:
            if self.need_print_items:
                debugger.log("before print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                self._print_items()
                # manually move the cursor to the edge to maximize the room for rendering
                self.render.move_down(1)
                self.render.move_up(1)
                debugger.log("after print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            debugger.log(f"move_cursor_to_line_editor ...")
            debugger.log(f"render.line_number: {self.render.line_number}")
            debugger.log(f"render.n_lines: {self.render.n_lines}")
            # always move cursor back to line editor after printing items
            n_vertical, n_horizontal = self.render.move_cursor_to_line_editor(
                self.line_editor
            )
            debugger.log(f"n_vertical: {n_vertical}")
            debugger.log(f"n_horizontal: {n_horizontal}")
            self.need_print_items = True
            self.need_run_handler = True

    # --------------------------------------------------------------------------
    # handle key pressed
    # --------------------------------------------------------------------------
    def process_key_pressed_input(self, pressed: str):
        """
        Process user keyboard input.

        Zelfred default key bindings:

        - ⬆: tap ``Ctrl + E`` or ``UP`` to move item selection cursor up (previous item).
        - ⏫: tap ``Ctrl + R`` to scroll item selection cursor up.
        - ⬇️: tap ``Ctrl + D`` or ``DOWN`` to move item selection cursor down (next item).
        - ⏬: tap ``Ctrl + F`` to scroll item selection cursor down.
        - ⬅️: tap ``LEFT`` to move query input cursor to the left.
        - ➡️: tap ``RIGHT`` to move query input cursor to the right.
        - ⏪: tap ``Alt + LEFT`` to move query input cursor to the previous word.
        - ⏩: tap ``Alt + Right`` to move query input cursor to the next word.
        - ⏮️: tap ``HOME`` to move query input cursor to the beginning of the line.
        - ⏭️: tap ``END`` to move query input cursor to the end of the line.
        - ◀️: tap ``Ctrl + K`` to delete the previous word.
        - ▶️: tap ``Ctrl + L`` to delete the next word.
        - ↩️: tap ``Ctrl + X`` to clear the query input.
        - ◀️: tap ``BACKSPACE`` to delete query input backward.
        - ▶️: tap ``DELETE`` to delete query input forward.
        - 🔴: tap ``Ctrl + C`` to quit the app.
        - ⤴️: tap ``F1`` to quit the current sub session and go back to the previous session and recover previous user input.

        User defined (customizable) item action:

        - 🚀: tap ``Enter`` to perform custom user action.
        - 🚀: tap ``Ctrl + A`` to perform custom item action.
        - 🚀: tap ``Ctrl + W`` to perform custom item action.
        - 🚀: tap ``Ctrl + U`` to perform custom item action.
        - 🚀: tap ``Ctrl + P`` to perform custom item action.

        User defined UI keybinding:

        - 🚀: tap ``CTRL + T`` to perform custom UI action, default is "do nothing.
        - 🚀: tap ``CTRL + G`` to perform custom UI action, default is "do nothing.
        - 🚀: tap ``CTRL + B`` to perform custom UI action, default is "do nothing.
        - 🚀: tap ``CTRL + N`` to perform custom UI action, default is "do nothing.
        """
        pressed_key_name = key_to_name.get(pressed, pressed)
        debugger.log(f"pressed: {pressed_key_name!r}, key code: {pressed!r}")
        self._process_key_pressed_input(pressed)

    def _process_input_v1_immediately(self):
        event = self.event_generator.next()
        if isinstance(event, events.KeyPressedEvent):
            self.process_key_pressed_input(pressed=event.value)

    def _process_input_v2_after_query_delay(self):
        start_time: T.Optional[float] = None
        while 1:
            event = self.event_generator.next()
            if isinstance(event, events.KeyPressedEvent):
                self.process_key_pressed_input(pressed=event.value)
            self.clear_query()
            self.print_query()
            self.render.move_cursor_to_line_editor(self.line_editor)
            if start_time is None:
                start_time = time.time()
            else:
                event_time = time.time()
                if event_time - start_time > self.query_delay:
                    break

    def process_input(self):
        """
        A wrapper of the core logic for processing input, ensures that the
        ``need_process_input`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- process_input --------------------")
        try:
            if self.need_process_input:
                self._process_input()
        finally:
            self.need_process_input = True

    def run_handler(self, items: T.Optional[T.List[T_ITEM]] = None):
        if self.need_run_handler:
            debugger.log("need to run handler")
            if items is None:
                debugger.log("run handler")
                items = self.handler(self.line_editor.line, self)
            else:
                debugger.log("explicitly give items, skip handler")
            self.dropdown.update(items)

    def move_to_end(self):
        """
        Move the cursor to the next line of the end of the dropdown menu.
        """
        debugger.log("-------------------- move_to_end --------------------")
        try:
            if self.need_move_to_end:
                debugger.log("need to move to end")
                debugger.log("before move to end")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                n_down = self.render.move_to_end()
                debugger.log(f"move down {n_down} lines")
                debugger.log("after move to end")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_move_to_end = True

    def repaint(self):
        """
        Repaint the UI right after the items is ready. This is useful when you want
        to show a message before running the real handler.
        """
        self.move_to_end()
        self.clear_items()
        self.clear_query()
        self.print_query()
        self.print_items()

    def run_sub_session(
        self,
        handler: T_HANDLER,
        initial_query: str = "",
    ):
        """
        Run a sub session with a new handler. User can tap "F1" to go back to the
        previous session. See :meth:`~zelfred.ui_process_key_pressed.UIProcessKeyPressedMixin.process_f1
        and the ``except exc.JumpOutSessionError:`` part in :meth:`~zelfred.ui.UI.run_session`
        to see how it works.

        :param handler: see :class:`UI`
        :param initial_query: the initial user input query in the sub session.
            it is the start-up text in the user input line editor.
        """
        # replace the current handler with the new handler
        self.replace_handler(handler)
        # update the dropdown items and the line editor content
        self.run_handler()
        self.line_editor.clear_line()
        self.line_editor.enter_text(initial_query)
        # re-paint the UI
        self.repaint()
        # enter the main event loop of the sub query session
        self.run_session(_do_init=False)

    def print_hello_items(self):
        items = [
            Item(
                uid="uid-hello-item",
                title="Welcome to the interactive UI",
            )
        ]
        self.dropdown.update(items)
        self.print_items()

    def print_debug_items(self, e: Exception):
        # if dropdown has items, then there must be one selected item
        # include the selected item information in the error message
        if self.dropdown.items:
            selected_item = self.dropdown.selected_item
            title = selected_item.title
            # handle the error in debug loop special case
            if title.startswith("Error on item: "):
                title = title[len("Error on item: ") :]
            processed_title = self.render.process_title(
                title,
                self.render.terminal.width - 15,
            )
            items = [
                DebugItem(
                    uid="uid",
                    title=f"Error on item: {processed_title}",
                    subtitle=f"{e!r}",
                )
            ]
        else:
            items = [
                DebugItem(
                    uid="uid",
                    title=f"Error on item: NA",
                    subtitle=f"{e!r}",
                )
            ]
        self.dropdown.update(items)
        self.print_items()

    def initialize_loop(self):
        """
        Process the first loop of a session. This loop starts with a hello message,
        and then run the handler, then render the UI.
        """
        debugger.log("=== initialize loop start ===")
        self.print_query()  # show initial query, mostly it is empty
        self.print_hello_items()  # show hello items
        self.run_handler()  # run handler using initial query
        self.move_to_end()  # move cursor to the end
        self.clear_items()  # clear items
        self.clear_query()  # clear query
        self.print_query()  # print query
        self.print_items()  # print items
        debugger.log("=== initialize loop end ===")

    def main_loop(self, _ith: int = 0):
        """
        This is the main loop of the UI. It starts with waiting for user input,
        and the run the handler, then render the UI.
        """
        while True:
            _ith += 1
            debugger.log(f"=== {_ith}th main loop start ===")
            self.process_input()
            # self._debug_controller_flags()
            self.run_handler()
            self.move_to_end()
            self.clear_items()
            self.clear_query()
            self.print_query()
            self.print_items()
            debugger.log(f"=== {_ith}th main loop end ===")

    def jump_out_session_loop(self):
        """
        This loop is executed after a :class:`~zelfred.exc.JumpOutSessionError` is raised.

        It pops up the current session from the queue and use the handler
        of previous session to run handler, and then render the UI.
        """
        if self._handler_queue:
            self.handler = self._handler_queue.pop()
        if self._line_editor_input_queue:
            self.line_editor.clear_line()
            self.line_editor.enter_text(self._line_editor_input_queue.pop())

        self.run_handler()
        self.move_to_end()
        self.clear_items()
        self.clear_query()
        self.print_query()
        self.print_items()

    def debug_loop(self, e: Exception):
        """
        Display error message in the UI and wait for new user input.
        New user input may fix the problem or trigger another error.
        """
        debugger.log("=== debug loop start ===")
        self.move_to_end()
        self.clear_items()
        self.clear_query()
        self.print_query()
        self.print_debug_items(e)
        debugger.log("=== debug loop end ===")

    def run_session(self, _do_init: bool = True):
        """
        Run a "session" in the UI. A "session" has a main loop, and it's handler
        to process user input query.

        Read :ref:`ui-event-loop`
        (or `this link <https://zelfred.readthedocs.io/en/latest/03-UI-Event-Loop/index.html>`_)
        for more information.


        ``except exc.JumpOutSessionError:``

        This error will be raised when user
        :meth:`press F1 <zelfred.ui_process_key_pressed.JumpOutSessionError.process_f1>`
        If the current session is a sub session, then it rolls backs the handler
        and line editor input to the previous state. If the current session is
        the main session, then it will do nothing.

        ``except exc.KeyboardInterrupt:``

        This error will be raised when user press ``Ctrl-C``. It will move the
        cursor to the end and prepare to exit the UI.
        """
        try:
            if _do_init:
                self.initialize_loop()
            self.main_loop()
        except exc.EndOfInputError as e:
            return e.selection
        except exc.JumpOutSessionError:
            self.jump_out_session_loop()
            return self.run_session(_do_init=False)
        except KeyboardInterrupt as e:
            self.move_to_end()
            raise e
        except Exception as e:
            if self.capture_error:
                self.debug_loop(e)
                return self.run_session(_do_init=False)
            else:
                raise e

    def run(self):
        """
        Run the UI.
        """
        try:
            self.run_session()
        except KeyboardInterrupt:
            print("🔴 keyboard interrupt, exit.", end="")
        finally:
            print("")


T_UI = T.TypeVar("T_UI", bound=UI)
