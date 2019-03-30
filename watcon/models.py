from .constants import FieldTypes as FT
from math import sqrt
import csv
import os
import json


class CSVModel:

    fields = {
            "Date": {'req':True, 'type':FT.iso_date_string},
            "Time": {'req':True, 'type':FT.iso_date_string},
            "Well Name": {'req':True, 'type':FT.string},
            "Engineer Name": {'req':True, 'type':FT.string},
            "Field Name" : {'req':True, 'type':FT.string},
            "Oil column thickness" : {'req':True, 'type':FT.decimal, 
                                      'min': 100, 'max': 99999, 'inc':.01},
            "Drainage radius" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Perforated interval" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Oil viscosity" :    {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Oil formation volume factor" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Oil density" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Water density" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Vertical Permeability" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Horizontal Permeability" : {'req':True, 'type':FT.decimal, 
                                      'min': 0, 'max': 99999, 'inc':.01},
            "Notes" : {'req':False, 'type':FT.long_string},
            "Critical oil rate" : {'req':True, 'type':FT.decimal}
            }            

    def __init__(self, filename):
        self.filename = filename
        
    def save_record(self, data):
        
        newfile = not os.path.exists(self.filename)
        
        with open(self.filename, 'a', encoding='utf-8') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys(),
                                       restval="not specified or may not "
                                               "apply for well type")
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

    @staticmethod
    def _compute_alpha(re, h, kv, kh):
        alpha = (re/h) * (sqrt((kv/kh)))
        return alpha

    def _compute_qc(self, re, h, kv, kh):
        qc = 0.7311 + (1.943 / self._compute_alpha(re, h, kv, kh))
        return qc

    def _compute_qoc(self, kh, kv, re, h, hp, visc, fvf, rho_w, rho_o):
        qoc = (0.0783 * (10**-4) * ((kh * ((h-hp)**2))/(visc*fvf)) *
               (rho_w - rho_o) * self._compute_qc(re, h, kv, kh))
        return qoc
    
    def calc(self, data):
        qoc =  self._compute_qoc(kh=data['Horizontal Permeability'], kv=data['Vertical Permeability'],
                                 re=data['Drainage radius'], h=data['Oil column thickness'],
                                 hp=data['Perforated interval'], visc=data['Oil viscosity'],
                                 fvf=data['Oil formation volume factor'],
                                 rho_w=data['Water density'],
                                 rho_o=data['Oil density'])
        data["Critical oil rate"] = qoc
        return qoc
    
        
class SettingsModel:
    "A model for saving settings"""

    variables = {'font size': {'type':'int', 'value': 9}}

    def __init__(self, filename='watcon_settings.json',
                 path='~'):

        self.filepath = os.path.join(
                            os.path.expanduser(path), filename)
        self.load()

    def load(self):

        if not os.path.exists(self.filepath):
            return
        else:
            with open(self.filepath, 'r', encoding='utf-8') as fh:
                raw_values = json.loads(fh.read())

        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value

    def save(self, settings=None):

        json_string = json.dumps(self.variables)
        with open(self.filepath, 'w', encoding='utf-8') as fh:
            fh.write(json_string)

    def set(self, key, value):

        if (
                key in self.variables and
                type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")
