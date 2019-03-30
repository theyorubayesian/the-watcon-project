import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import views as v
from . import models as m
from tkinter import messagebox
from .images import WATCON_LOGO, WATCON_LOGO_2
from tkinter.font import nametofont
from os import environ
import platform
from .mainmenu import get_main_menu_for_os


class olaleyeapp(tk.Tk):

    config_dirs = {'Linux': environ.get('$XDG_CONFIG_HOME', '~/.config'),
                   'freebsd7': environ.get('$XDG_CONFIG_HOME', '~/.config'),
                   'Darwin': '~/Library/Application	Support',
                   'Windows': '~/AppData/Local'}

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("WatCon-Est 1.0")
        self.resizable(width= True, height=True)

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.logo = tk.PhotoImage(file=WATCON_LOGO)
        tk.Label(self, image=self.logo).grid(row=0,column=0, sticky=tk.W)

        self.taskbar_icon = tk.PhotoImage(file=WATCON_LOGO_2)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        
        ttk.Label(self, text="Critical Oil Rate Method: Vertical Well", 
                  font=("TkDefaultFont", 16)).grid(row=0, column=0, sticky='NS')

        self.filename = tk.StringVar()
        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "water_coning_calculations_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.data_model = m.CSVModel(filename=self.filename.get())
        
        config_dir = self.config_dirs.get(platform.system(), '~')
        self.settings_model = m.SettingsModel(path=config_dir)
        self.load_settings()

        self.set_font()
        self.settings['font size'].trace('w', self.set_font)

        self.callbacks = {'file->quit': self.quit,
                          'on_calc': self.on_calc}

        menu_class = get_main_menu_for_os(platform.system())
        menu = menu_class(self, self.settings, self.callbacks)
        self.config(menu=menu)

        "data entry form"
        self.data_entry = v.DataEntryForm(self, m.CSVModel.fields,
                                          settings=self.settings, callbacks=self.callbacks)
        self.data_entry.grid(row=2, padx=10, sticky='NSEW')
        
        "results and status display"
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
        
        """result display"
        result = tk.LabelFrame(self, text="Critical Oil Rate:")
        self.result = tk.StringVar()
        self.resultbar = ttk.Label(self, textvariable=self.result)
        self.resultbar.grid(sticky=(tk.E + tk.E), row=)"""
        
    def load_settings(self):

        vartypes = {
            'bool': tk.BooleanVar,
            'str': tk.StringVar,
            'int': tk.IntVar,
            'float': tk.DoubleVar
            }

        self.settings = {}
        for key, data in self.settings_model.variables.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        for var in self.settings.values():
            var.trace('w', self.save_settings)

    def save_settings(self, *args):

        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()

    def set_font(self, *args):
        font_size=self.settings['font size'].get()

        font_names = ('TkDefaultFont', 'TkMenuFont', 'TkTextFont')
        for font_name in font_names:
            tk_font = nametofont(font_name)
            tk_font.config(size=font_size)

    def on_calc(self):
        
        errors = self.data_entry.get_errors()
        if errors:
            self.status.set(
                    "Cannot perform calculation, error in fields: {}"
                    .format(', '.join(errors.keys()))
                    )
            message = "Cannot do calculation"
            detail = "The following fields have errors: \n * {}".format(
                '\n  *   '.join(errors.keys()))

            messagebox.showerror(title='Error', message=message, 
                                 detail=detail)
            return False

        data = self.data_entry.get()
        qoc = self.data_model.calc(data)
        self.data_model.save_record(data)
        self.status.set(
                "Critical Oil Rate:{}".format(qoc))