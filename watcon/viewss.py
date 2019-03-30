import tkinter as tk
from datetime import datetime
from . import widgets as w
from tkinter import messagebox, ttk


class DataEntryForm(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.inputs = {}

    "pulling form data"
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    "resetting form"
    def reset(self):

        for widget in self.inputs.values():
            widget.set('')

        current_date = datetime.today().strftime('%Y-%m-%d')
        current_time = datetime.today().strftime('%H:%M')

        self.inputs['Date'].set(current_date)
        self.inputs['Time'].set(current_time)

    "error getter"
    def get_errors(self):

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors


class CrtVertForm(DataEntryForm):

    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        "self.settings = settings"
        self.callbacks = callbacks
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inputs = {}

        style = ttk.Style()
        style.configure('details.TLabel', background='khaki')
        style.configure('dimensions.TLabel', background='cyan')
        style.configure('fluidprops.TLabel', background='cyan')
        style.configure('rockprops.TLabel', background='cyan')

        "details"
        details = tk.LabelFrame(self, text="Details", bg='khaki', padx=10, pady=10)

        self.inputs["Engineer Name"] = w.LabelInput(details, "Name:",
                                                    field_spec=fields['Engineer name'],
                                                    label_args={'style': 'details.TLabel'})
        self.inputs["Engineer Name"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Well Name"] = w.LabelInput(details,
                                                "Well Name",
                                                field_spec=fields['Well name'],
                                                label_args={'style': 'details.TLabel'})
        self.inputs["Well Name"].grid(row=0, column=1, sticky='NSEW')

        self.inputs["Field Name"] = w.LabelInput(details, "Field Name",
                                                 field_spec=fields['Field name'],
                                                 label_args={'style': 'details.TLabel'})
        self.inputs["Field Name"].grid(row=0, column=2, sticky='NSEW')

        self.inputs["Date"] = w.LabelInput(details, "Date",
                                           field_spec=fields['Date'],
                                           label_args={'style': 'details.TLabel'})
        self.inputs["Date"].grid(row=1, column=0, sticky='NSEW')

        self.inputs["Time"] = w.LabelInput(details, "Time",
                                           field_spec=fields['Time'],
                                           label_args={'style': 'details.TLabel'})
        self.inputs["Time"].grid(row=1, column=1, sticky='NSEW')

        details.grid(row=0, column=0, sticky='NSEW')

        dimensions = tk.LabelFrame(self, text="Dimensions", bg="cyan", padx=10, pady=10)

        self.inputs["h"] = w.LabelInput(dimensions,
                                        "Oil column thickness, h (ft)",
                                        field_spec=fields['Oil column thickness'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["h"].grid(row=0, column=0, padx=1, pady=1,  sticky='NSEW')

        self.inputs["re"] = w.LabelInput(dimensions,
                                         "Drainage radius, re (ft)",
                                         field_spec=fields['Drainage radius'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["re"].grid(row=0, column=1, padx=1, pady=1,  sticky='NSEW')

        self.inputs["hp"] = w.LabelInput(dimensions,
                                         "Perforated interval, hp (ft)",
                                         field_spec=fields['Perforated interval'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["hp"].grid(row=0, column=2, padx=1, pady=1,  sticky='NSEW')

        dimensions.grid(row=1, column=0, sticky='NSEW')

        "fluid properties"
        fluidprops = tk.LabelFrame(self, text="Fluid Properties", bg='khaki',
                                   padx=10, pady=10)

        self.inputs["Oil viscosity"] = w.LabelInput(fluidprops,
                                                    "Oil viscosity, µ (cp)",
                                                    field_spec=fields['Oil viscosity'],
                                                    label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Oil viscosity"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Oil formation volume factor"] = w.LabelInput(fluidprops,
                                                                  "Oil formation volume factor, Bo (bbl/STB)",
                                                                  field_spec=fields['Oil formation volume factor'],
                                                                  label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Oil formation volume factor"].grid(row=0, column=1, sticky='NSEW')

        self.inputs["Oil density"] = w.LabelInput(fluidprops,
                                                  "Oil density, ?o (lb/ft3)",
                                                  field_spec=fields['Oil density'],
                                                  label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Oil density"].grid(row=1, column=0, sticky='NSEW')

        self.inputs["Water density"] = w.LabelInput(fluidprops,
                                                    "Water density, ?w (lb/ft3)",
                                                    field_spec=fields['Water density'],
                                                    label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Water density"].grid(row=1, column=1, sticky='NSEW')

        fluidprops.grid(row=2, column=0, sticky='NSEW')

        "rock properties"
        rockprops = tk.LabelFrame(self, text="Rock Properties", bg='khaki',
                                  padx=10, pady=10)

        self.inputs["Vertical Permeability"] = w.LabelInput(rockprops,
                                                            "Vertical Permeability, (md)",
                                                            field_spec=fields['Vertical permeability'],
                                                            label_args={'style': 'rockprops.TLabel'})
        self.inputs["Vertical Permeability"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Horizontal Permeability"] = w.LabelInput(rockprops,
                                                              "Horizontal Permeability, (md)",
                                                              field_spec=fields['Horizontal permeability'],
                                                              label_args={'style': 'rockprops.TLabel'})
        self.inputs["Horizontal Permeability"].grid(row=0, column=1, sticky='NSEW')

        rockprops.grid(row=3, column=0, sticky='NSEW')

        "Notes"
        self.inputs["Notes"] = w.LabelInput(self, "Notes", input_class=tk.Text,
                                            input_args={"width": 75, "height": 10})
        self.inputs["Notes"].grid(row=4, column=0,
                                  padx=10, pady=10, sticky='NSEW')

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=callbacks["on_calc"])
        self.calcbutton.grid(sticky=tk.E, row=5, padx=10)

        "reset form at start"
        self.reset()


class CrtHorForm(DataEntryForm):

    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inputs = {}

        style = ttk.Style()
        style.configure('dimensions.TLabel', background='cyan')
        style.configure('fluidprops.TLabel', background='cyan')
        style.configure('rockprops.TLabel', background='cyan')

        dimensions = tk.LabelFrame(self, text="Dimensions", bg="cyan", padx=1, pady=1)

        self.inputs["h"] = w.LabelInput(dimensions,
                                        "Oil column thickness, h (ft)",
                                        field_spec=fields['h'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["h"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["L"] = w.LabelInput(dimensions,
                                        "Length of horizontal well, L (ft)",
                                        field_spec=fields['L'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["L"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["ye"] = w.LabelInput(dimensions,
                                         "Half distance between two lines of horizontal wells, ye (ft)",
                                         field_spec=fields['ye'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["ye"].grid(row=1, column=0, padx=1, pady=1)

        self.inputs["Db"] = w.LabelInput(dimensions,
                                         "Distance between WOC and horizontal well, Db (ft)",
                                         field_spec=fields['Db'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["Db"].grid(row=1, column=1, padx=1, pady=1)

        dimensions.grid(row=1, column=0, sticky='NSEW')

        fluidprops = tk.LabelFrame(self, text="Fluid Properties",
                                   bg="cyan", padx=1, pady=1)

        self.inputs["visc"] = w.LabelInput(fluidprops,
                                           "Oil viscosity, µo (cp)",
                                           field_spec=fields['visc'],
                                           label_args={'style': 'fluidprops.TLabel'})
        self.inputs["visc"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["fvf"] = w.LabelInput(fluidprops,
                                          "Oil formation volume factor, Bo (bbl/STB)",
                                          field_spec=fields['fvf'],
                                          label_args={'style': 'fluidprops.TLabel'})
        self.inputs["fvf"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["rho_o"] = w.LabelInput(fluidprops,
                                            "Oil density, ρo (lb/ft3)",
                                            field_spec=fields['rho_o'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_o"].grid(row=0, column=2, padx=1, pady=1)

        self.inputs["rho_w"] = w.LabelInput(fluidprops,
                                            "Water density, ρw (lb/ft3)",
                                            field_spec=fields['rho_w'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_w"].grid(row=0, column=3, padx=1, pady=1)

        fluidprops.grid(row=2, column=0, sticky='NSEW')

        rockprops = tk.LabelFrame(self, text="Rock Properties",
                                  bg="cyan", padx=1, pady=1)

        self.inputs["kv"] = w.LabelInput(rockprops,
                                         "Vertical Permeability, kv (md)",
                                         field_spec=fields['kv'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kv"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["kh"] = w.LabelInput(rockprops,
                                         "Horizontal Permeability, kh (md)",
                                         field_spec=fields['kh'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kh"].grid(row=0, column=1, padx=1, pady=1)

        rockprops.grid(row=3, column=0, sticky='NSEW')

        "Notes"
        self.inputs["Notes"] = w.LabelInput(self, "Notes", input_class=tk.Text,
                                            input_args={"width": 75, "height": 10})
        self.inputs["Notes"].grid(row=4, column=0,
                                  padx=10, pady=10, sticky='NSEW')

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=callbacks["on_calc"])
        self.calcbutton.grid(sticky=tk.E, row=5, padx=10)

        "reset form at start"
        self.reset()


class WbVertForm(DataEntryForm):

    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inputs = {}

        style = ttk.Style()
        style.configure('dimensions.TLabel', background='cyan')
        style.configure('fluidprops.TLabel', background='cyan')
        style.configure('rockprops.TLabel', background='cyan')

        dimensions = tk.LabelFrame(self, text="Dimensions", bg="cyan", padx=1, pady=1)

        self.inputs["h"] = w.LabelInput(dimensions,
                                        "Oil column thickness, h (ft)",
                                        field_spec=fields['h'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["h"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["hp"] = w.LabelInput(dimensions,
                                         "Perforated interval, hp (ft)",
                                         field_spec=fields['hp'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["hp"].grid(row=0, column=1, padx=1, pady=1)

        dimensions.grid(row=1, column=0, sticky='NSEW')

        fluidprops = tk.LabelFrame(self, text="Fluid Properties",
                                   bg="cyan", padx=1, pady=1)

        self.inputs["visc"] = w.LabelInput(fluidprops,
                                           "Oil viscosity, µo (cp)",
                                           field_spec=fields['visc'],
                                           label_args={'style': 'fluidprops.TLabel'})
        self.inputs["visc"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["fvf"] = w.LabelInput(fluidprops,
                                          "Oil formation volume factor, Bo (bbl/STB)",
                                          field_spec=fields['fvf'],
                                          label_args={'style': 'fluidprops.TLabel'})
        self.inputs["fvf"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["rho_o"] = w.LabelInput(fluidprops,
                                            "Oil density, ρo (lb/ft3)",
                                            field_spec=fields['rho_o'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_o"].grid(row=0, column=2, padx=1, pady=1)

        self.inputs["rho_w"] = w.LabelInput(fluidprops,
                                            "Water density, ρw (lb/ft3)",
                                            field_spec=fields['rho_w'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_w"].grid(row=1, column=0, padx=1, pady=1)

        self.inputs["M"] = w.LabelInput(fluidprops,
                                        "Water-oil mobility, M",
                                        field_spec=fields['M'],
                                        label_args={'style': 'fluidprops.TLabel'})
        self.inputs["M"].grid(row=1, column=1, padx=1, pady=1)

        self.inputs["Qo"] = w.LabelInput(fluidprops,
                                         "Oil production rate, Qo (STB/day)",
                                         field_spec=fields['Qo'],
                                         label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Qo"].grid(row=1, column=2, padx=1, pady=1)

        fluidprops.grid(row=2, column=0, sticky='NSEW')

        rockprops = tk.LabelFrame(self, text="Rock Properties",
                                  bg="cyan", padx=1, pady=1)

        self.inputs["kv"] = w.LabelInput(rockprops,
                                         "Vertical Permeability, kv (md)",
                                         field_spec=fields['kv'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kv"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["kh"] = w.LabelInput(rockprops,
                                         "Horizontal Permeability, kh (md)",
                                         field_spec=fields['kh'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kh"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["por_o"] = w.LabelInput(rockprops,
                                            "Oil porosity, ɸ",
                                            field_spec=fields['por_o'],
                                            label_args={'style': 'rockprops.TLabel'})
        self.inputs["por_o"].grid(row=0, column=2, padx=1, pady=1)

        rockprops.grid(row=3, column=0, sticky='NSEW')

        "Notes"
        self.inputs["Notes"] = w.LabelInput(self, "Notes", input_class=tk.Text,
                                            input_args={"width": 75, "height": 10})
        self.inputs["Notes"].grid(row=4, column=0,
                                  padx=10, pady=10, sticky='NSEW')

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=callbacks["on_calc"])
        self.calcbutton.grid(sticky=tk.E, row=5, padx=10)

        "reset form at start"
        self.reset()


class WbHorForm(DataEntryForm):

    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inputs = {}

        style = ttk.Style()
        style.configure('dimensions.TLabel', background='cyan')
        style.configure('fluidprops.TLabel', background='cyan')
        style.configure('rockprops.TLabel', background='cyan')

        dimensions = tk.LabelFrame(self, text="Dimensions", bg="cyan", padx=1, pady=1)

        self.inputs["h"] = w.LabelInput(dimensions,
                                        "Oil column thickness, h (ft)",
                                        field_spec=fields['h'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["h"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["L"] = w.LabelInput(dimensions,
                                        "Length of horizontal well, L (ft)",
                                        field_spec=fields['L'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["L"].grid(row=0, column=1, padx=1, pady=1)

        dimensions.grid(row=1, column=0, sticky='NSEW')

        fluidprops = tk.LabelFrame(self, text="Fluid Properties",
                                   bg="cyan", padx=1, pady=1)

        self.inputs["visc"] = w.LabelInput(fluidprops,
                                           "Oil viscosity, µo (cp)",
                                           field_spec=fields['visc'],
                                           label_args={'style': 'fluidprops.TLabel'})
        self.inputs["visc"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["fvf"] = w.LabelInput(fluidprops,
                                          "Oil formation volume factor, Bo (bbl/STB)",
                                          field_spec=fields['fvf'],
                                          label_args={'style': 'fluidprops.TLabel'})
        self.inputs["fvf"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["rho_o"] = w.LabelInput(fluidprops,
                                            "Oil density, ρo (lb/ft3)",
                                            field_spec=fields['rho_o'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_o"].grid(row=0, column=2, padx=1, pady=1)

        self.inputs["rho_w"] = w.LabelInput(fluidprops,
                                            "Water density, ρw (lb/ft3)",
                                            field_spec=fields['rho_w'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_w"].grid(row=1, column=0, padx=1, pady=1)

        self.inputs["Qo"] = w.LabelInput(fluidprops,
                                         "Oil production rate, Qo (STB/day)",
                                         field_spec=fields['Qo'],
                                         label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Qo"].grid(row=1, column=1, padx=1, pady=1)

        fluidprops.grid(row=2, column=0, sticky='NSEW')

        rockprops = tk.LabelFrame(self, text="Rock Properties",
                                  bg="cyan", padx=1, pady=1)

        self.inputs["kv"] = w.LabelInput(rockprops,
                                         "Vertical Permeability, kv (md)",
                                         field_spec=fields['kv'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kv"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["kh"] = w.LabelInput(rockprops,
                                         "Horizontal Permeability, kh (md)",
                                         field_spec=fields['kh'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kh"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["por_o"] = w.LabelInput(rockprops,
                                            "Oil porosity, ɸ",
                                            field_spec=fields['por_o'],
                                            label_args={'style': 'rockprops.TLabel'})
        self.inputs["por_o"].grid(row=0, column=2, padx=1, pady=1)

        rockprops.grid(row=3, column=0, sticky='NSEW')

        "Notes"
        self.inputs["Notes"] = w.LabelInput(self, "Notes", input_class=tk.Text,
                                            input_args={"width": 75, "height": 10})
        self.inputs["Notes"].grid(row=4, column=0,
                                  padx=10, pady=10, sticky='NSEW')

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=callbacks["on_calc"])
        self.calcbutton.grid(sticky=tk.E, row=5, padx=10)

        "reset form at start"
        self.reset()


class WpVertForm(DataEntryForm):

    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inputs = {}

        style = ttk.Style()
        style.configure('dimensions.TLabel', background='cyan')
        style.configure('fluidprops.TLabel', background='cyan')
        style.configure('rockprops.TLabel', background='cyan')

        dimensions = tk.LabelFrame(self, text="Dimensions", bg="cyan", padx=1, pady=1)

        self.inputs["h"] = w.LabelInput(dimensions,
                                        "Oil column thickness, h (ft)",
                                        field_spec=fields['h'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["h"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["A"] = w.LabelInput(dimensions,
                                        "Drainage radius, A (ft)",
                                        field_spec=fields['A'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["A"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["rw"] = w.LabelInput(dimensions,
                                         "Wellbore radius, rw (ft)",
                                         field_spec=fields['rw'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["rw"].grid(row=0, column=2, padx=1, pady=1)

        self.inputs["hp"] = w.LabelInput(dimensions,
                                         "Perforated interval, hp (ft)",
                                         field_spec=fields['hp'],
                                         label_args={'style': 'dimensions.TLabel'})
        self.inputs["hp"].grid(row=0, column=3, padx=1, pady=1)

        self.inputs["t"] = w.LabelInput(dimensions,
                                        "Assumed time, t (days)",
                                        field_spec=fields['t'],
                                        label_args={'style': 'dimensions.TLabel'})
        self.inputs["t"].grid(row=0, column=4, padx=1, pady=1)

        dimensions.grid(row=1, column=0, sticky='NSEW')

        fluidprops = tk.LabelFrame(self, text="Fluid Properties", bg="cyan", padx=1, pady=1)

        self.inputs["visc"] = w.LabelInput(fluidprops,
                                           "Oil viscosity, µo (cp)",
                                           field_spec=fields['visc'],
                                           label_args={'style': 'fluidprops.TLabel'})
        self.inputs["visc"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["fvf"] = w.LabelInput(fluidprops,
                                          "Oil formation volume factor, Bo (bbl/STB)",
                                          field_spec=fields['fvf'],
                                          label_args={'style': 'fluidprops.TLabel'})
        self.inputs["fvf"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["rho_o"] = w.LabelInput(fluidprops,
                                            "Oil density, ρo (lb/ft3)",
                                            field_spec=fields['rho_o'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_o"].grid(row=0, column=2, padx=1, pady=1)

        self.inputs["rho_w"] = w.LabelInput(fluidprops,
                                            "Water density, ρw (lb/ft3)",
                                            field_spec=fields['rho_w'],
                                            label_args={'style': 'fluidprops.TLabel'})
        self.inputs["rho_w"].grid(row=1, column=0, padx=1, pady=1)

        self.inputs["M"] = w.LabelInput(fluidprops,
                                        "Water-oil mobility, M",
                                        field_spec=fields['M'],
                                        label_args={'style': 'fluidprops.TLabel'})
        self.inputs["M"].grid(row=1, column=1, padx=1, pady=1)

        self.inputs["Qo"] = w.LabelInput(fluidprops,
                                         "Oil production rate, Qo (STB/day)",
                                         field_spec=fields['Qo'],
                                         label_args={'style': 'fluidprops.TLabel'})
        self.inputs["Qo"].grid(row=1, column=2, padx=1, pady=1)

        fluidprops.grid(row=2, column=0, sticky='NSEW')

        rockprops = tk.LabelFrame(self, text="Rock Properties", bg="cyan", padx=1, pady=1)

        self.inputs["kv"] = w.LabelInput(rockprops,
                                         "Vertical Permeability, kv (md)",
                                         field_spec=fields['kv'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kv"].grid(row=0, column=0, padx=1, pady=1)

        self.inputs["kh"] = w.LabelInput(rockprops,
                                         "Horizontal Permeability, kh (md)",
                                         field_spec=fields['kh'],
                                         label_args={'style': 'rockprops.TLabel'})
        self.inputs["kh"].grid(row=0, column=1, padx=1, pady=1)

        self.inputs["por_o"] = w.LabelInput(rockprops,
                                            "Oil porosity, ɸ",
                                            field_spec=fields['por_o'],
                                            label_args={'style': 'rockprops.TLabel'})
        self.inputs["por_o"].grid(row=0, column=2, padx=1, pady=1)

        self.inputs["Swc"] = w.LabelInput(rockprops,
                                          "Connate water saturation, Swc",
                                          field_spec=fields['Swc'],
                                          label_args={'style': 'rockprops.TLabel'})
        self.inputs["Swc"].grid(row=1, column=0, padx=1, pady=1)

        self.inputs["Sor"] = w.LabelInput(rockprops,
                                          "Residual Oil Saturation, Sor",
                                          field_spec=fields['Sor'],
                                          label_args={'style': 'rockprops.TLabel'})
        self.inputs["Sor"].grid(row=1, column=1, padx=1, pady=1)

        rockprops.grid(row=3, column=0, sticky=tk.W + tk.E)

        "Notes"
        self.inputs["Notes"] = w.LabelInput(self, "Notes", input_class=tk.Text,
                                            input_args={"width": 75, "height": 10})
        self.inputs["Notes"].grid(row=4, column=0,
                                  padx=10, pady=10, sticky='NSEW')

        self.calcbutton = ttk.Button(self, text="Calculate",
                                     command=callbacks["on_calc"])
        self.calcbutton.grid(sticky=tk.E, row=5, padx=10)

        "reset form at start"
        self.reset()