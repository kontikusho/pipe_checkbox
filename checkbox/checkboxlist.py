from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import FormattedTextControl, Window
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.formatted_text import to_formatted_text


class CheckboxList(object):
    """
    List of check boxes. Multi checked at the same time.
    -> Japanese: チェックボックスのリストです。複数選択できます。
    :param values: List of [value, checked].
    """

    def __init__(self, values):
        assert isinstance(values, list)
        assert len(values) > 0
        assert all(isinstance(i, list) and len(i) == 2
                   for i in values)

        self.values = values
        self._selected_index = 0

        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add('down')
        def _(event):
            self._selected_index = min(
                len(self.values) - 1, self._selected_index + 1)

        @kb.add('pageup')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = max(
                0,
                self._selected_index - len(w.render_info.displayed_lines)
            )

        @kb.add('pagedown')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + len(w.render_info.displayed_lines)
            )

        @kb.add('enter')
        @kb.add(' ')
        def _(event):
            self.values[self._selected_index][1] = not self.values[self._selected_index][1]

        @kb.add(Keys.Any)
        def _(event):
            # We first check values after the selected value, then all values.
            for value in self.values[self._selected_index + 1:] + self.values:
                if value[0].startswith(event.data):
                    self._selected_index = self.values.index(value)
                    return

        # Control and window.
        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True)

        self.window = Window(
            content=self.control,
            style='class:checkbox-list',
            right_margins=[
                ScrollbarMargin(display_arrows=True),
            ],
            dont_extend_height=True)

    def _get_text_fragments(self):
        result = []
        for i, value in enumerate(self.values):
            checked = value[1]
            selected = (i == self._selected_index)

            style = ''
            if checked:
                style += ' class:checkbox-checked'
            if selected:
                style += ' class:checkbox-selected'

            result.append((style, '['))

            if selected:
                result.append(('[SetCursorPosition]', ''))

            if checked:
                result.append((style, '*'))
            else:
                result.append((style, ' '))

            result.append((style, ']'))
            result.append(('class:checkbox', ' '))
            result.extend(to_formatted_text(value[0], style='class:checkbox'))
            result.append(('', '\n'))

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window
