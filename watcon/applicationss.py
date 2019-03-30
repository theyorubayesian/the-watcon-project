import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import viewss as v
from . import modelss as m
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

    """data_models = {"<class 'watcon.applicationss.CrtVert'>": ,
                   "<class 'watcon.applicationss.CrtHor'>": m.CriticalRateHorizontalModel,
                   "<class 'watcon.applicationss.WbVert'>": m.WaterBreakthroughVerticalModel,
                   "<class 'watcon.applicationss.WbHor'>": m.WaterBreakthroughHorizontalModel,
                   "<class 'watcon.applicationss.WpVert'>": m.WellPerformanceModel}

    filename_dict = {"<class 'watcon.applicationss.CrtVert'>": ,
                   "<class 'watcon.applicationss.CrtHor'>": 'watcon_calculations_critical_rate_{}.csv',
                   "<class 'watcon.applicationss.WbVert'>": 'watcon_calculations_water_breakthrough_{}.csv',
                   "<class 'watcon.applicationss.WbHor'>": 'watcon_calculations_water_breakthrough_{}.csv',
                   "<class 'watcon.applicationss.WpVert'>": 'watcon_calculations_well_performance_{}.csv'}"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.title("WatCon-Est 1.0")
        self.resizable(width=True, height=True)

        self.logo = tk.PhotoImage(file=WATCON_LOGO)
        tk.Label(self, image=self.logo).grid(row=0, column=0, sticky=tk.W)

        self.taskbar_icon = tk.PhotoImage(file=WATCON_LOGO_2)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        config_dir = self.config_dirs.get(platform.system(), '~')
        self.settings_model = m.SettingsModel(path=config_dir)
        self.load_settings()

        self.callbacks = {'file->quit': self.quit}

        menu_class = get_main_menu_for_os(platform.system())
        menu = menu_class(self, self.settings, self.callbacks)
        self.config(menu=menu)

        self.set_font()
        self.settings['font size'].trace('w', self.set_font)

        container = tk.Frame(self)
        container.grid(sticky='NSEW')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, CrtVert, CrtHor, WbVert, WbHor, WpVert):

            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='NSEW')

        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

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
        font_size = self.settings['font size'].get()

        font_names = ('TkDefaultFont', 'TkMenuFont', 'TkTextFont')
        for font_name in font_names:
            tk_font = nametofont(font_name)
            tk_font.config(size=font_size)


class HomePage(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        ttk.Label(self, text="Home Page").grid(row=0)

        self.navbutton1 = ttk.Button(self,
                                     text="Critical Oil Rate Method: Vertical Well",
                                     command=lambda: controller.show_frame(CrtVert))
        self.navbutton1.grid(padx=10, pady=10, row=2, column=0, sticky=tk.W)

        self.navbutton2 = ttk.Button(self,
                                     text="Critical Oil Rate Method: Horizontal Well",
                                     command=lambda: controller.show_frame(CrtHor))
        self.navbutton2.grid(padx=10, pady=10, row=3, column=0, sticky=tk.W)

        self.navbutton3 = ttk.Button(self,
                                     text="Water Breakthrough Time Method: Vertical Well",
                                     command=lambda: controller.show_frame(WbVert))
        self.navbutton3.grid(padx=10, row=4, column=10, sticky=tk.W)

        self.navbutton4 = ttk.Button(self,
                                     text="Water Breakthrough Time Method: Horizontal Well",
                                     command=lambda: controller.show_frame(WbHor))
        self.navbutton4.grid(padx=10, row=5, column=10, sticky=tk.W)

        self.navbutton5 = ttk.Button(self,
                                     text="Well Performance After Breakthrough Method: Vertical Well",
                                     command=lambda: controller.show_frame(WpVert))
        self.navbutton5.grid(padx=10, row=6, column=5, sticky=tk.W)


class CrtVert(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        ttk.Label(self,
                  text="Critical Oil Rate Method: Vertical Well").grid(row=0)

        self.callbacks = {'on_calc': self.on_calc}

        self.filename = tk.StringVar()
        default_filename = 'watcon_calculations_critical_rate_{}.csv'.format(
            datetime.today().strftime("%Y-%m-%d"))
        self.filename = tk.StringVar(value=default_filename)
        self.data_model = m.CriticalRateVerticalModel(filename=self.filename)

        self.data_entry = v.CrtVertForm(self, fields=m.CSVModel.fields, callbacks=self.callbacks)
        self.data_entry.grid(row=1, padx=10)

        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky='NSEW', row=3, padx=10)

        self.navbutton = ttk.Button(self, text="Back",
                                    command=lambda: controller.show_frame(HomePage))
        self.navbutton.grid(padx=10, pady=10, row=0, column=5, sticky=tk.E)

    def on_calc(self):

        errors = self.data_entry.get_errors()
        if errors:
            self.status.set(
                "Cannot perform calculation, error in fields: {}".format(
                    ', '.join(errors.keys()))
            )
            message = "Cannot do calculation"
            detail = "The following fields have errors: \n * {}".format(
                '\n  *   '.join(errors.keys()))

            messagebox.showerror(title='Error', message=message,
                                 detail=detail)
            return False

        data = self.data_entry.get()
        result = self.data_model.calc(data)
        self.data_model.save_record(data)
        self.status.set(
            "Critical Oil Rate:{}".format(result))


class CrtHor(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)


class WbVert(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)


class WbHor(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)


class WpVert(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)


