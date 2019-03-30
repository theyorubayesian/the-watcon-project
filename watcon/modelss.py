from .constants import FieldTypes as FT
from math import sqrt
import csv
import os
import json
from math import log, log10


class CSVModel:

    fields = {
        "Date": {'req': True, 'type': FT.iso_date_string},
        "Time": {'req': True, 'type': FT.iso_date_string},
        "Well name": {'req': True, 'type': FT.string},
        "Engineer name": {'req': True, 'type': FT.string},
        "Field name": {'req': True, 'type': FT.string},
        "Oil column thickness": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Area of reservoir":  {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Length of horizontal well": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Half distance between two wells": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Distance between WOC & horizontal well": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Drainage radius": {'req': True, 'type': FT.decimal,
                            'min': 0, 'max': 99999, 'inc': .01},
        "Wellbore radius": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Perforated interval": {'req': True, 'type': FT.decimal,
                                'min': 0, 'max': 99999, 'inc': .01},
        "Water-Oil mobility": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Oil viscosity": {'req': True, 'type': FT.decimal,
                          'min': 0, 'max': 99999, 'inc': .01},
        "Oil formation volume factor": {'req': True, 'type': FT.decimal,
                                        'min': 0, 'max': 99999, 'inc': .01},
        "Oil density": {'req': True, 'type': FT.decimal,
                        'min': 0, 'max': 99999, 'inc': .01},
        "Water density": {'req': True, 'type': FT.decimal,
                          'min': 0, 'max': 99999, 'inc': .01},
        "Connate water saturation": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Residual oil saturation": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Oil production rate": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Vertical permeability": {'req': True, 'type': FT.decimal,
                                  'min': 0, 'max': 99999, 'inc': .01},
        "Horizontal permeability": {'req': True, 'type': FT.decimal,
                                    'min': 0, 'max': 99999, 'inc': .01},
        "Porosity": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Assumed time": {'req': True, 'type': FT.decimal,
                                 'min': 0, 'max': 99999, 'inc': .01},
        "Notes": {'req': False, 'type': FT.long_string},
        "Critical oil rate": {'req': False, 'type': FT.decimal},
        "Cumulative Production": {'req': False, 'type': FT.decimal},
        "Initial Oil in place": {'req': False, 'type': FT.decimal},
        "Water production rate": {'req': False, 'type': FT.decimal},
        "Recovery factor": {'req': False, 'type': FT.decimal},
        "Time to breakthrough": {'req': False, 'type': FT.decimal},
        "New oil production rate": {'req': False, 'type': FT.decimal},
        "Cumulative production after breakthrough" : {'req': False, 'type': FT.decimal},
        "Water cut": {'req': False, 'type': FT.decimal}
    }

    def __init__(self, filename):
        self.filename = filename

    def save_record(self, data):
        newfile = not os.path.exists(self.filename)

        with open(self.filename, 'a', encoding='utf-8') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys(), restval='not given'
                                                            'or many not apply to well type')
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)


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


class CriticalRateVerticalModel(CSVModel):

    @staticmethod
    def _compute_alpha(re, h, kv, kh):
        alpha = (re / h) * (sqrt((kv / kh)))
        return alpha

    def _compute_qc(self, re, h, kv, kh):
        qc = 0.7311 + (1.943 / self._compute_alpha(re, h, kv, kh))
        return qc

    def _compute_qoc(self, kh, kv, re, h, hp, visc, fvf, rho_w, rho_o):
        qoc = (0.0783 * (10 ** -4) * ((kh * ((h - hp) ** 2)) / (visc * fvf)) *
               (rho_w - rho_o) * self._compute_qc(re, h, kv, kh))
        return qoc

    def calc(self, data):
        qoc = self._compute_qoc(kh=data['Horizontal Permeability'], kv=data['Vertical Permeability'],
                                re=data['Drainage radius'], h=data['Oil column thickness'],
                                hp=data['Perforated interval'], visc=data['Oil viscosity'],
                                fvf=data['Oil formation volume factor'],
                                rho_w=data['Water density'],
                                rho_o=data['Oil density'])
        data["Critical oil rate"] = qoc
        return qoc


class CriticalRateHorizontalModel(CSVModel):

    @staticmethod
    def _compute_alpha(ye, h, kv, kh):
        alpha = (ye/h) * (sqrt((kv/kh)))
        return alpha

    def _compute_qc(self, ye, h, kv, kh):
        qc = 3.9624955 + (0.0616438 * self._compute_alpha(ye, h, kv, kh)) - (
                            0.000504 * (self._compute_alpha(ye, h, kv, kh))**2)


        return qc

    def _compute_qoc(self, ye, h, kv, kh, l, rho_w, rho_o, db, visc, fvf):
        qoc = 0.0783 * ((10**-4)*((l * self._compute_qc(ye, h, kv, kh))/ye) * (rho_w - rho_o) *
                                                        ((kh * ((h - (h - db))**2))/(visc * fvf)))
        return qoc

    def calc(self, data):

        qoc = self._compute_qoc(ye=data["Half distance between two horizontal wells"],
                                h=data["Oil column thickness"],
                                kv=data["Vertical permeability"],
                                kh=data["Horizontal permeability"],
                                l=data["Length of horizontal well"],
                                rho_w=data["Water density"],
                                rho_o=data["Oil density"],
                                visc=data["Oil viscosity"],
                                db=data["Distance between WOC & horizontal well"],
                                fvf=data["Oil formation volume factor"])
        data["Critical oil rate"] = qoc
        return qoc


class WaterBreakthroughVerticalModel(CSVModel):

    @staticmethod
    def _compute_dimen_z(rho_w, rho_o, kh, h, hp, visc, fvf, qo):
        dimen_z = 0.492 * (10 ** -4) * (((rho_w - rho_o) * kh * h * (h - hp)) / (visc * fvf * qo))
        return dimen_z

    def _compute_dimen_bt(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo):
        dimen_bt = self._compute_dimen_z(rho_w, rho_o, kh, h, hp, visc, fvf, qo) / (
                    3 - (0.7 * self._compute_dimen_z(rho_w, rho_o, kh, h, hp, visc, fvf, qo)))
        return dimen_bt

    def _compute_tbt(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M):
        if (M <= 1):
            alpha = 0.5
        else:
            alpha = 0.6

        time_to_breakthrough = (20325 * visc * h * por_o * self._compute_dimen_bt(
                                            rho_w, rho_o, kh, h, hp, visc, fvf, qo)) / (
                                                (rho_w - rho_o) * kv * (1 + (M ** alpha)))
        return time_to_breakthrough

    def calc(self, data):

        time_to_breakthrough = self._compute_tbt(rho_w=data["Water density"],
                                                 rho_o=data["Oil density"],
                                                 kh=data["Horizontal permeability"],
                                                 h=data["Oil colmn thickness"],
                                                 hp=data["Perforated interval"],
                                                 visc=data["Oil viscosity"],
                                                 fvf=data["Oil formation volume factor"],
                                                 qo=data["Oil production rate"],
                                                 por_o=data["Porosity"],
                                                 kv=data["Vertical permeability"],
                                                 M=data["Water-Oil mobility"])
        data["Time to breakthrough"] = time_to_breakthrough
        return time_to_breakthrough


class WaterBreakthroughHorizontalModel(CSVModel):

    @staticmethod
    def _compute_dimen_q(visc, fvf, qo, l, h, rho_w, rho_o, kv, kh):
        dimen_q = (20333.66 * visc * fvf * qo) / (l * h * (rho_w - rho_o) * (sqrt(kv * kh)))
        return dimen_q

    def _compute_dimen_bt(self, visc, fvf, qo, l, h, rho_w, rho_o, kv, kh):
        a = 3 * self._compute_dimen_q(visc, fvf, qo, l, h, rho_w, rho_o, kv, kh)
        b = a - 1
        c = log(a / b)
        d = b * c
        dimen_bt = 1 - d
        return dimen_bt

    def _compute_tbt(self, visc, fvf, qo, l, h, rho_w, rho_o, kv, kh, por_o):
        a = 22758.528 * h * por_o * visc * self._compute_dimen_bt(visc, fvf, qo, l, h, rho_w, rho_o, kv, kh)
        b = kv * (rho_w - rho_o)
        time_to_breakthrough = a / b
        return time_to_breakthrough

    def calc(self, data):

        time_to_breakthrough = self._compute_tbt(visc=data["Oil viscosity"],
                                                 fvf=data["Oil formation volume factor"],
                                                 qo=data["Oil production rate"],
                                                 l=data["Length of horizontal well"],
                                                 h=data["Oil column thickness"],
                                                 rho_w=data["Water density"],
                                                 rho_o=data["Oil density"],
                                                 kv=data["Vertical permeability"],
                                                 kh=data["Horizontal permeability"],
                                                 por_o=data["Porosity"])
        data["time_to_breakthrough"] = time_to_breakthrough
        return time_to_breakthrough


class WellPerformanceModel(CSVModel):

    @staticmethod
    def _compute_dimen_z(rho_w, rho_o, kh, h, hp, visc, fvf, qo):

        dimen_z = 0.492 * (10 ** -4) * (((rho_w - rho_o) * kh * h * (h - hp)) /
                                        (visc * fvf * qo))
        return dimen_z

    def _compute_dimen_bt(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo):

        dimen_bt = self._compute_dimen_z(rho_w, rho_o, kh, h, hp, visc, fvf, qo) / (
                    3 - (0.7 * self._compute_dimen_z(rho_w, rho_o, kh, h, hp, visc, fvf, qo)))
        return dimen_bt

    def _compute_time_to_breakthrough(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M):

        if (M <= 1):
            alpha = 0.5
        else:
            alpha = 0.6
        time_to_breakthrough = (20325 * visc * h * por_o * self._compute_dimen_bt(rho_w, rho_o, kh, h,
                                                                                  hp, visc, fvf, qo)) / ((rho_w - rho_o) * kv * (1 + (M ** alpha)))
        return time_to_breakthrough

    def _compute_oip(self, A, por_o, h, swc, fvf):

        oiip = (7758 * A * por_o * h * (1 - swc)) / fvf
        return oiip

    def _compute_Np(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M):

        cum_oil_prod = qo * self._compute_time_to_breakthrough(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M)
        return cum_oil_prod

    def _compute_r(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, A, swc, sor):

        r = (self._compute_Np(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M) / self._compute_oip(A,
                                por_o, h, swc, fvf)) * ((1 - swc) / (1 - sor - swc))
        return r

    def _compute_wc1(self, rho_w, rho_o, kh, h, hp, visc, fvf, Qo, por_o, kv, M, A, swc, sor):

        a = self._compute_r(rho_w, rho_o, kh, h, hp, visc, fvf, Qo, por_o, kv, M, A, swc, sor)
        b = 1 - a
        c = h * b
        d = hp + (h * a)
        wc_1 = M / (M + (c / d))
        return wc_1

    def _compute_a_tbt(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t):
        atBT = t / self._compute_time_to_breakthrough(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M)
        return atBT

    def _compute_fw(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor):

        e = self._compute_a_tbt(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t)
        if e < 0.5:
            fw_d = 0
        elif e > 5.7:
            fw_d = 1
        else:
            fw_d = 0.29 + 0.94 * log10(e)

        fw = self._compute_wc1(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, A, swc, sor) * fw_d
        return fw

    def _compute_qw(self, rho_w, rho_o, kh, h, hp, visc, fvf, Qo, por_o, kv, M, t, A, swc, sor):

        qw = (self._compute_fw(rho_w, rho_o, kh, h, hp, visc, fvf, Qo, por_o, kv, M, t, A, swc, sor) * Qo)
        return qw

    def _compute_n_qo(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor):
        n_qo = qo - self._compute_qw(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor)
        return n_qo

    def _compute_cum_oil_prod_after_breakthrough(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor):

        f = self._compute_time_to_breakthrough(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M)
        g = self._compute_n_qo(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor)
        h = self._compute_Np(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M)

        a = ((qo + g) / 2) * (t - f)
        cum_oil_prod_after_breakthrough = h + a
        return cum_oil_prod_after_breakthrough

    def _compute_rf(self, rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor):

        i = self._compute_cum_oil_prod_after_breakthrough(rho_w, rho_o, kh, h, hp, visc, fvf, qo, por_o, kv, M, t, A, swc, sor)
        j = self._compute_oip(A, por_o, h, swc, fvf)

        rf = (i / j) * 100
        return rf

    def fw_calc(self, data):

        fw = self._compute_fw(kh=data['Horizontal permeability'],
                              kv=data['Vertical permeability'], swc=data['Swc'],
                              A=data['A'], h=data['Oil column thickness'],
                              sor=data['Residual oil saturation'],
                              hp=data['Perforated interval'],
                              visc=data['Oil viscosity'],
                              fvf=data['Oil formation volume factor'],
                              qo=data['Oil production rate'],
                              rho_w=data['Water density'],
                              por_o=data['Porosity'],
                              rho_o=data['Oil density'],
                              M=data['Water-oil mobility'],
                              t=data['Assumed time'])
        data["Water cut"] = fw
        return fw

    def time_to_breakthrough_calc(self, data):

        time_to_breakthrough = self._compute_time_to_breakthrough(kh=data['Horizontal permability'],
                                                          kv=data['Vertical permeability'],
                                                          qo=data['Oil production rate'],
                                                          h=data['Oil column thickness'],
                                                          por_o=data['Porosity'],
                                                          hp=data['Perforated interval'],
                                                          visc=data['Oil viscosity'],
                                                          fvf=data['Oil formation volume factor'],
                                                          M=data['Water-oil mobility'],
                                                          rho_w=data['Water density'],
                                                          rho_o=data['Oil density'])
        data["Time to breakthrough"] = time_to_breakthrough
        return time_to_breakthrough

    def oiip_calc(self, data):

        oiip = self._compute_oip(A=data['Area of reservoir'],
                              por_o=data['Porosity'],
                              h=data['Oil column thickness'],
                              swc=data['Connate water saturation'],
                              fvf=data['Oil formation volume factor'])
        data["Initial Oil Place"] = oiip
        return oiip

    def cum_oil_prod_after_breakthrough_calc(self, data):

        cum_oil_prod_after_breakthrough = self._compute_cum_oil_prod_after_breakthrough(kh=data['Horizontal permeability'],
                                                        kv=data['Vertical permeability'],
                                                        M=data['Water-oil mobility'],
                                                        h=data['Oil column thickness'],
                                                        qo=data['Oil production rate'],
                                                        swc=data['Connate water saturation'],
                                                        hp=data['Perforated interval'],
                                                        visc=data['Oil viscosity'],
                                                        fvf=data['Oil formation volume factor'],
                                                        por_o=data['Porosity'],
                                                        rho_w=data['Water density'],
                                                        A=data['Area of reservoir'],
                                                        sor=data['Residual oil saturation'],
                                                        rho_o=data['Oil density'],
                                                        t=data['Assumed time'])
        data["Cumulative oil production after breakthrough"] = cum_oil_prod_after_breakthrough
        return cum_oil_prod_after_breakthrough

    def water_prod_rate_calc(self, data):

        qw = self._compute_qw(kh=data['kh'],
                              kv=data['kv'],
                              A=data['A'],
                              h=data['h'],
                              swc=data['Swc'],
                              hp=data['hp'],
                              visc=data['visc'],
                              fvf=data['fvf'],
                              sor=data['Sor'],
                              rho_w=data['rho_w'],
                              Qo=data['Qo'],
                              por_o=data['por_o'],
                              M=data['M'],
                              rho_o=data['rho_o'],
                              t=data['t'])
        data["Water production rate"] = qw
        return qw

    def n_qo_calc(self, data):

        n_qo = self._compute_n_qo(kh=data['Horizontal permeability'],
                                kv=data['Vertical permeability'],
                                t=data['Assumed time'],
                                A=data['Area of reservoir'],
                                h=data['Oil column thickness'],
                                hp=data['Perforated interval'],
                                visc=data['Oil viscosity'],
                                fvf=data['Oil formation volume factor'],
                                swc=data['Connate water saturation'],
                                rho_w=data['Water density'],
                                sor=data['Residual oil saturation'],
                                qo=data['Oil production rate'],
                                por_o=data['Porosity'],
                                rho_o=data['Oil density'],
                                M=data['Water-oil mobility'])
        data["New oil production rate"] = n_qo
        return n_qo

    def rf_calc(self, data):

        rf = self._compute_rf(kh=data['Horizontal permeability'],
                              kv=data['Vertical permeability'],
                              swc=data['Connate water saturation'],
                              A=data['Area of reservoir'],
                              h=data['Oil column thickness'],
                              sor=data['Residual oil saturation'],
                              hp=data['Perforated interval'],
                              visc=data['Oil viscosity'],
                              fvf=data['Oil formation volume factor'],
                              qo=data['Oil production rate'],
                              rho_w=data['Water density'],
                              por_o=data['Porosity'],
                              rho_o=data['Oil density'],
                              M=data['Water-oil mobility'],
                              t=data['Assumed time'])
        data["Recovery factor"] = rf
        return rf