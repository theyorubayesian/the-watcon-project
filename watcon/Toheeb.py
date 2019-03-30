import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .views2 import CrtVertForm
from .views2 import CrtHorForm
from .views2 import WbVertForm
from .views2 import WbHorForm
from .views2 import WpVertForm
from .models2 import CvCSVModel
from .models2 import ChCSVModel
from .models2 import WvCSVModel
from .models2 import WhCSVModel
from .models2 import WpvCSVModel
from .models2 import CvSettingsModel
from tkinter import messagebox
from os import path
import platform
import subprocess

"image_path = path.join(path.dirname(__file__), 'images/watcon_logo_32x20.jpeg')"
from .images2 import WATCON_LOGO_32
from PIL import ImageTk, Image
from tkinter import filedialog
from .mainmenu2 import get_main_menu_for_os

from os import environ
from tkinter.font import nametofont

LARGE_FONT = ("Verdan", 14)


class olaleyeapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        "tk.Tk.iconbitmap(self,default=WATCON_LOGO_32)"

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("WatCon-Est 1.0")
        self.resizable(width=True, height=True)

        self.frames = {}

        for F in (HomePage, CrtVert, CrtHor, WbVert, WbHor, WpVert):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        ttk.Label(self, text="Home Page",
                  font=("TkDefaultFont", 12)).grid(row=0)

        COR = tk.LabelFrame(self, text="Critical Oil Rate Methods", bg="cyan",
                            padx=10, pady=10)

        self.navbutton = ttk.Button(self,
                                    text="Critical Oil Rate Method: Vertical Well",
                                    command=lambda: controller.show_frame(CrtVert))
        self.navbutton.grid(padx=10, pady=10, row=2, column=0, sticky=tk.W)

        self.navbutton = ttk.Button(self,
                                    text="Critical Oil Rate Method: Horizontal Well",
                                    command=lambda: controller.show_frame(CrtHor))
        self.navbutton.grid(padx=10, pady=10, row=10, column=0, sticky=tk.W)

        COR.grid(row=10, column=0, sticky=tk.W + tk.E)

        WBT = tk.LabelFrame(self, text="Water Breakthrough Time Methods", bg="cyan",
                            padx=10, pady=10)

        self.navbutton = ttk.Button(self,
                                    text="Water Breakthrough Time Method: Vertical Well",
                                    command=lambda: controller.show_frame(WbVert))
        self.navbutton.grid(padx=10, row=2, column=10, sticky=tk.W)

        self.navbutton = ttk.Button(self,
                                    text="Water Breakthrough Time Method: Horizontal Well",
                                    command=lambda: controller.show_frame(WbHor))
        self.navbutton.grid(padx=10, row=10, column=10, sticky=tk.W)

        WBT.grid(row=2, column=0, sticky=tk.W + tk.E)

        WPB = tk.LabelFrame(self, text="Well Performance After Breakthrough Methods", bg="cyan",
                            padx=10, pady=10)

        self.navbutton = ttk.Button(self,
                                    text="Well Performance After Breakthrough Method: Vertical Well",
                                    command=lambda: controller.show_frame(WpVert))
        self.navbutton.grid(padx=10, row=4, column=5, sticky=tk.W)

        WPB.grid(row=2, column=0, sticky=tk.W + tk.E)


class CrtVert(tk.Frame):
    config_dirs = {
        'Linux': environ.get('$XDG_CONFIG_HOME', '~/.config'),
        'freebsd7': environ.get('$XDG_CONFIG_HOME', '~/.config'),
        'Darwin': '~/Library/Application Support',
        'Windows': '~/AppData/Local'}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Critical Oil Rate Method: Vertical Well",
                  font=("TkDefaultFont", 16)).grid(row=0)

        self.navbutton = ttk.Button(self, text="Back to Home Page",
                                    command=lambda: controller.show_frame(HomePage))
        self.navbutton.grid(padx=10, pady=10, row=0, column=5, sticky=tk.E)

        self.callbacks = {
            'file->select': self.on_file_select,
            'file->quit': self.quit
        }

        config_dir = self.config_dirs.get(platform.system(), '~')
        self.settings_model = CvSettingsModel(path=config_dir)
        self.load_settings()

        """menu_class = get_main_menu_for_os(platform.system())
        menu = menu_class(self, self.settings, self.callbacks)
        self.config(menu=menu)"""

        self.entryform = CrtVertForm(self, CvCSVModel.fields, self.settings, self.callbacks)
        self.entryform.grid(row=1, padx=10)

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=self.on_calc)
        self.calcbutton.grid(padx=10, row=2, sticky=tk.E)

        # status display
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

    def on_calc(self):

        errors = self.entryform.get_errors()

        if errors:
            message = "Cannot perform calculation"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            messagebox.showerror(title='Error', message=message, detail=detail)

            return True

        if errors:
            self.status.set(
                "Cannot perform calculation, error in fields: {}"
                    .format(', '.join(errors.keys())))
            return False

        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "water_coning_calculations_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.filename = tk.StringVar
        model = CvCSVModel(filename=default_filename)
        data = self.entryform.get()
        Qoc = model.calc(data)
        model.save_entry(data)
        self.status.set(
            "Critical Oil Rate: {}".format(Qoc))

    def on_file_select(self):

        filename = filedialog.asksaveasfilename(
            title='Select the target file for saving entries and result',
            defaultextension='.csv',
            filetypes=[('Comma=Separated Values', '*.csv * .csv')])

        if filename:
            self.filename.set(filename)

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

        self.set_font()
        self.settings['font size'].trace('w', self.set_font)

        style = ttk.Style()
        theme = self.settings.get('theme').get()
        if theme in style.theme_names():
            style.theme_use(theme)

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


class CrtHor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Critical Oil Rate Method: Horizontal Well",
                  font=("TkDefaultFont", 16)).grid(row=0)

        self.navbutton = ttk.Button(self, text="Back to Home Page",
                                    command=lambda: controller.show_frame(HomePage))
        self.navbutton.grid(padx=10, pady=10, row=0, column=5, sticky=tk.E)

        self.entryform = CrtHorForm(self, ChCSVModel.fields, self.settings)
        self.entryform.grid(row=1, padx=10)

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=self.on_calc)
        self.calcbutton.grid(padx=10, row=2, sticky=tk.E)

        # status display
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

    def on_calc(self):

        errors = self.entryform.get_errors()

        if errors:
            message = "Cannot perform calculation"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            messagebox.showerror(title='Error', message=message, detail=detail)
            return False

        if errors:
            self.status.set(
                "Cannot perform calculation, error in fields: {}"
                    .format(', '.join(errors.keys())))
            return False

        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "water_coning_calculations_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.filename = tk.StringVar
        model = ChCSVModel(filename=default_filename)
        data = self.entryform.get()
        Qoc = model.calc(data)
        model.save_entry(data)
        self.status.set(
            "Critical Oil Rate: {}".format(Qoc))


class WbVert(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Water Breakthrough Time Method: Vertical Well",
                  font=("TkDefaultFont", 16)).grid(row=0)

        self.navbutton = ttk.Button(self, text="Back to Home Page",
                                    command=lambda: controller.show_frame(HomePage))
        self.navbutton.grid(padx=10, pady=10, row=0, column=5, sticky=tk.E)

        self.entryform = WbVertForm(self, WvCSVModel.fields)
        self.entryform.grid(row=1, padx=10)

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=self.on_calc)
        self.calcbutton.grid(padx=10, row=2, sticky=tk.E)

        # status display
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

    def on_calc(self):

        errors = self.entryform.get_errors()

        if errors:
            message = "Cannot perform calculation"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            messagebox.showerror(title='Error', message=message, detail=detail)
            return False

        if errors:
            self.status.set(
                "Cannot perform calculation, error in fields: {}"
                    .format(', '.join(errors.keys())))
            return False

        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "water_coning_calculations_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.filename = tk.StringVar
        model = WvCSVModel(filename=default_filename)
        data = self.entryform.get()
        tBT = model.calc(data)
        model.save_entry(data)
        self.status.set(
            "Water Breakthrough Time: {}".format(tBT))


class WbHor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Water Breakthrough Time Method: Horizontal Well",
                  font=("TkDefaultFont", 16)).grid(row=0)

        self.navbutton = ttk.Button(self, text="Back to Home Page",
                                    command=lambda: controller.show_frame(HomePage))
        self.navbutton.grid(padx=10, pady=10, row=0, column=5, sticky=tk.E)

        self.entryform = WbHorForm(self, WhCSVModel.fields)
        self.entryform.grid(row=1, padx=10)

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=self.on_calc)
        self.calcbutton.grid(padx=10, row=2, sticky=tk.E)

        # status display
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

    def on_calc(self):

        errors = self.entryform.get_errors()

        if errors:
            message = "Cannot perform calculation"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            messagebox.showerror(title='Error', message=message, detail=detail)
            return False

        if errors:
            self.status.set(
                "Cannot perform calculation, error in fields: {}"
                    .format(', '.join(errors.keys())))
            return False

        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "water_coning_calculations_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.filename = tk.StringVar
        model = WhCSVModel(filename=default_filename)
        data = self.entryform.get()
        tBT = model.calc(data)
        model.save_entry(data)
        self.status.set(
            "Water Breakthrough Time: {}".format(tBT))


class WpVert(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Well Performance After Breakthrough Method: Vertical Well",
                  font=("TkDefaultFont", 16)).grid(row=0)

        self.navbutton = ttk.Button(self, text="Back to Home Page",
                                    command=lambda: controller.show_frame(HomePage))
        self.navbutton.grid(padx=10, pady=10, row=0, column=5, sticky=tk.E)

        self.entryform = WpVertForm(self, WpvCSVModel.fields)
        self.entryform.grid(row=1, padx=10)

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=self.on_calc)
        self.calcbutton.grid(padx=10, row=2, sticky=tk.E)

        # status display
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

        # additional result display
        self.title = ttk.Label(self, text="ADDITIONAL RESULTS:")
        self.title.grid(row=5, column=0, sticky=tk.W, padx=10)

        self.tBT = ttk.Label(self, text="Water Breakthrough Time: ")
        self.tBT.grid(row=6, column=0, sticky="W", padx=10)

        self.N = ttk.Label(self, text="Initial Oil In Place: ")
        self.N.grid(row=7, column=0, sticky="W", padx=10)

        self.cummNp = ttk.Label(self, text="Cummulative Oil Production after assumed time(t): ")
        self.cummNp.grid(row=8, column=0, sticky="W", padx=10)

        self.Qw = ttk.Label(self, text="Water Flow Rate: ")
        self.Qw.grid(row=9, column=0, sticky="W", padx=10)

        self.nQo = ttk.Label(self, text="Current Oil Flow Rate: ")
        self.nQo.grid(row=10, column=0, sticky="W", padx=10)

        self.RF = ttk.Label(self, text="Recovery Factor: ")
        self.RF.grid(row=11, column=0, sticky="W", padx=10)

    def on_calc(self):

        errors = self.entryform.get_errors()

        if errors:
            message = "Cannot perform calculation"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            messagebox.showerror(title='Error', message=message, detail=detail)
            return False

        if errors:
            self.status.set(
                "Cannot perform calculation, error in fields: {}"
                    .format(', '.join(errors.keys())))
            return False

        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "water_coning_well_performance_calculations_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)

        self.filename = tk.StringVar
        model = WpvCSVModel(filename=default_filename)
        data = self.entryform.get()
        fw = model.fwcalc(data)
        tBT = model.tBTcalc(data)
        N = model.Ncalc(data)
        cummNp = model.cummNpcalc(data)
        Qw = model.Qwcalc(data)
        nQo = model.nQocalc(data)
        RF = model.RFcalc(data)
        b = "days"
        c = "STB"
        d = "STB"
        e = "STB/day"
        f = "STB/day"
        g = "%"

        model.save_entry(data)
        self.status.set(
            "Water Cut: {}".format(fw))

        self.tBT.config(text="Water Breakthrough Time: {}".format(tBT, b))

        self.N.config(text="Initial Oil In Place: {}".format(N, c))

        self.cummNp.config(text="Cummulative Oil Production after assumed time(t): {}".format(cummNp, d))

        self.Qw.config(text="Water Flow Rate: {}".format(Qw, e))

        self.nQo.config(text="Current Oil Flow Rate: {}".format(nQo, f))

        self.RF.config(text="Recovery Factor: {}".format(RF, g))

