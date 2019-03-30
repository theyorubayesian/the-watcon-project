from functools import partial
import tkinter as tk
from tkinter import messagebox

"""Well well well"""

class GenericMainMenu(tk.Menu):

    def __init__(self, parent, settings, callbacks, **kwargs):
        super().__init__(parent, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self._build_menu()

    def _build_menu(self):
        file_menu = tk.Menu(self, tearoff=False)
        """file_menu.add_command(label="Select file...",
                command=self.callbacks['file->open'])

        file_menu.add_separator()"""

        file_menu.add_command(label='Quit',
                              command=self.callbacks['file->quit'],
                              accelerator='Ctrl+q')

        self.add_cascade(label='File', menu=file_menu)

        options_menu = tk.Menu(self, tearoff=False)
        font_size_menu = tk.Menu(self, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size, variable=self.settings['font size'])
        options_menu.add_cascade(label='Font size', menu=font_size_menu)
        self.add_cascade(label='Options', menu=options_menu)

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def get_keybinds(self):
        return {'<Control-q>': self.callbacks['file->quit']}

    @staticmethod
    def _argstrip(function, *args):
        return function()

    def _bind_accelerators(self):
        keybinds = self.get_keybinds()
        for key, command in keybinds.items():
            self.bind_all(key, partial(self._argstrip, command))

    def show_about(self):
        """Show the about dialog"""

        about_message = 'WatCon-Est 2.0'
        about_detail = ('by Toheeb Olaleye\n'
                        'For assistance please contact the author')
        messagebox.showinfo(title='About', message=about_message,
                            detail=about_detail)


class WindowsMainMenu(GenericMainMenu):

    def _build_menu(self):

        file_menu = tk.Menu(self, tearoff=False)
        """file_menu.add_command(label="Select file...",
                command=self.callbacks['file->open'])

        file_menu.add_separator()"""

        file_menu.add_command(label='Exit',
                              command=self.callbacks['file->quit'])

        self.add_cascade(label='File', menu=file_menu)

        tools_menu = tk.Menu(self, tearoff=False)
        options_menu = tk.Menu(self, tearoff=False)
        font_size_menu = tk.Menu(self, tearoff=False)

        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size, variable=self.settings['font size'])
        options_menu.add_cascade(label='Font size', menu=font_size_menu)

        tools_menu.add_separator()
        tools_menu.add_cascade(label='Options', menu=options_menu)
        self.add_cascade(label='Tools', menu=tools_menu)

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def get_keybinds(self):
        return {}


class LinuxMainMenu(GenericMainMenu):

    def _build_menu(self):
        file_menu = tk.Menu(self, tearoff=False)
        """file_menu.add_command(label="Select file...",
                command=self.callbacks['file->open'])

        file_menu.add_separator()"""

        file_menu.add_command(label='Quit',
                              command=self.callbacks['file->quit'],
                              accelerator='Ctrl+q')

        self.add_cascade(label='File', menu=file_menu)

        """edit_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Edit', menu=edit_menu)"""

        view_menu = tk.Menu(self, tearoff=False)
        font_size_menu = tk.Menu(view_menu, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size, variable=self.settings['font size'])
        view_menu.add_cascade(label='Font size', menu=font_size_menu)
        self.add_cascade(label='View', menu=view_menu)

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)


class MacOsMainMenu(GenericMainMenu):

    def _build_menu(self):

        file_menu = tk.Menu(self, tearoff=False)
        """file_menu.add_command(label="Select file...",
                command=self.callbacks['file->open'])

        file_menu.add_separator()"""

        file_menu.add_command(label='Quit',
                              command=self.callbacks['file->quit'],
                              accelerator='Cmd-q')

        self.add_cascade(label='File', menu=file_menu)

        app_menu = tk.Menu(self, tearoff=False, name='apple')
        app_menu.add_command(label='About WatCon Est.', command=self.show_about())
        self.add_cascade(label='Watcon Est.', menu=app_menu)

        """edit_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Edit', menu=edit_menu)"""

        view_menu = tk.Menu(self, tearoff=False)
        font_size_menu = tk.Menu(view_menu, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size, variable=self.settings['font size'])
        view_menu.add_cascade(label='Font size', menu=font_size_menu)
        self.add_cascade(label='View', menu=view_menu)

        """window_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Window', menu=window_menu)"""

    def get_keybinds(self):
            return {}


def get_main_menu_for_os(os_name):

    menus = {'Linux': LinuxMainMenu,
             'Darwin': MacOsMainMenu,
             'freebsd7': LinuxMainMenu,
             'Windows': WindowsMainMenu}
    return menus.get(os_name, GenericMainMenu)
