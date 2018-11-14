#!/usr/bin/env python
from __future__ import unicode_literals
import sys
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Window
from prompt_toolkit.input.defaults import create_input
from checkbox.checkboxlist import CheckboxList


def run():
    content = []
    for line in iter(sys.stdin.readline, ""):
        content.append([line.strip(), False])

    chk = CheckboxList(content)

    root_container = chk
    layout = Layout(root_container)
    kb = KeyBindings()

    @kb.add('q')
    def exit_(event):
        event.app.exit()

    app = Application(
        input=create_input(sys.stdout),
        key_bindings=kb,
        layout=layout,
        full_screen=True
    )
    app.run()

if __name__ == '__main__':
    run()
