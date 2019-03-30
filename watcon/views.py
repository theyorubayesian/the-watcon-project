import tkinter as tk
from datetime import datetime
from . import widgets as w
from tkinter import messagebox, ttk


class DataEntryForm(tk.Frame):
    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
        self.callbacks = callbacks
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.inputs = {}
        style = ttk.Style()

        style.configure('details.TLabel', background='khaki')
        style.configure('dimensions.TLabel', background='khaki')
        style.configure('fluidprops.TLabel', background='khaki')
        style.configure('rockprops.TLabel', background='khaki')
        "details"
        details = tk.LabelFrame(self, text="Details", bg='khaki', padx=10, pady=10)

        self.inputs["Engineer Name"] = w.LabelInput(details, "Name:",
                                                    field_spec=fields['Engineer Name'],
                                                    label_args={'style':'details.TLabel'})
        self.inputs["Engineer Name"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Well Name"] = w.LabelInput(details,
                                                "Well Name",
                                                field_spec=fields['Well Name'],
                                                label_args={'style': 'details.TLabel'})
        self.inputs["Well Name"].grid(row=0, column=1, sticky='NSEW')

        self.inputs["Field Name"] = w.LabelInput(details, "Field Name",
                                                 field_spec=fields['Field Name'],
                                                 label_args={'style': 'details.TLabel'})
        self.inputs["Field Name"].grid(row=0, column=2, sticky='NSEW')

        self.inputs["Date"] = w.LabelInput(details, "Date",
                                           field_spec=fields['Date'],
                                           label_args={'style':'details.TLabel'})
        self.inputs["Date"].grid(row=1, column=0, sticky='NSEW')

        self.inputs["Time"] = w.LabelInput(details, "Time",
                                           field_spec=fields['Time'],
                                           label_args={'style':'details.TLabel'})
        self.inputs["Time"].grid(row=1, column=1, sticky='NSEW')

        details.grid(row=0, column=0, sticky='NSEW')

        "dimensions"
        dimensions = tk.LabelFrame(self, text="Dimensions",
                                  bg='khaki', padx=10, pady=10)

        self.inputs["Drainage radius"] = w.LabelInput(dimensions,
                                                      "Drainage radius (ft)",
                                                      field_spec=fields['Drainage radius'],
                                                      label_args={'style':'dimensions.TLabel'})
        self.inputs["Drainage radius"].grid(row=0, column=1, sticky='NSEW')

        self.inputs["Oil column thickness"] = w.LabelInput(dimensions,
                                                           "Oil column thickness(ft)",
                                                           field_spec=fields['Oil column thickness'],
                                                           label_args={'style':'dimensions.TLabel'})
        self.inputs["Oil column thickness"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Perforated interval"] = w.LabelInput(dimensions,
                                                          "Perforated interval (ft)",
                                                          field_spec=fields['Perforated interval'],
                                                          label_args={'style':'dimensions.TLabel'})
        self.inputs["Perforated interval"].grid(row=0, column=2, sticky='NSEW')

        dimensions.grid(row=1, column=0, sticky='NSEW')

        "fluid properties"
        fluidprops = tk.LabelFrame(self, text="Fluid Properties", bg='khaki',
                                   padx=10, pady=10)

        self.inputs["Oil viscosity"] = w.LabelInput(fluidprops,
                                                    "Oil viscosity, µ (cp)",
                                                    field_spec=fields['Oil viscosity'],
                                                    label_args={'style':'fluidprops.TLabel'})
        self.inputs["Oil viscosity"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Oil formation volume factor"] = w.LabelInput(fluidprops,
                                                                  "Oil formation volume factor, Bo (bbl/STB)",
                                                                  field_spec=fields['Oil formation volume factor'],
                                                                  label_args={'style':'fluidprops.TLabel'})
        self.inputs["Oil formation volume factor"].grid(row=0, column=1, sticky='NSEW')

        self.inputs["Oil density"] = w.LabelInput(fluidprops,
                                                  "Oil density, ?o (lb/ft3)",
                                                  field_spec=fields['Oil density'],
                                                  label_args={'style':'fluidprops.TLabel'})
        self.inputs["Oil density"].grid(row=1, column=0, sticky='NSEW')

        self.inputs["Water density"] = w.LabelInput(fluidprops,
                                                    "Water density, ?w (lb/ft3)",
                                                    field_spec=fields['Water density'],
                                                    label_args={'style':'fluidprops.TLabel'})
        self.inputs["Water density"].grid(row=1, column=1, sticky='NSEW')

        fluidprops.grid(row=2, column=0, sticky='NSEW')

        "rock properties"
        rockprops = tk.LabelFrame(self, text="Rock Properties", bg='khaki',
                                  padx=10, pady=10)

        self.inputs["Vertical Permeability"] = w.LabelInput(rockprops,
                                                            "Vertical Permeability, (md)",
                                                            field_spec=fields['Vertical Permeability'],
                                                            label_args={'style':'rockprops.TLabel'})
        self.inputs["Vertical Permeability"].grid(row=0, column=0, sticky='NSEW')

        self.inputs["Horizontal Permeability"] = w.LabelInput(rockprops,
                                                              "Horizontal Permeability, (md)",
                                                              field_spec=fields['Horizontal Permeability'],
                                                              label_args={'style':'rockprops.TLabel'})
        self.inputs["Horizontal Permeability"].grid(row=0, column=1, sticky='NSEW')

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
