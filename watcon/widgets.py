import tkinter as tk
from tkinter import ttk
from decimal import Decimal, InvalidOperation
from .constants import FieldTypes as FT
            

class ValidatedMixin:

    def __init__(self, *args, error_var=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.error = error_var or tk.StringVar()
        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        style = ttk.Style()
        widget_class = self.winfo_class()
        validated_style = 'ValidatedInput.' + widget_class
        style.map(
            validated_style, foreground=[('invalid', 'white'), ('!invalid', 'black')],
            fieldbackground=[('invalid', 'darkred'), ('!invalid', 'white')])

        self.config(style=validated_style, validate='all',
                    validatecommand = (vcmd,'%P','%s','%S','%V','%i','%d'),
                    invalidcommand = (invcmd, '%P', '%s','%S','%V','%i','%d'))
        
    def _validate(self, proposed, current, char, event, index, action):

        self.error.set('')
        valid = True
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(proposed=proposed, current=current, 
                                       char=char, event=event, index=index, 
                                       action=action)
        return valid
    
    def _focusout_validate(self, **kwargs):

        return True
    
    def _key_validate(self, **kwargs):

        return True
    
    def _invalid(self, proposed, current, char, event, index, action):

        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event=='key':
            self._key_invalid(proposed=proposed,current=current, char=char, 
                              event=event, index=index, action=action)

    def _focusout_invalid(self, **kwargs):
        pass
        
    def _key_invalid(self, **kwargs):

        pass
    
    def trigger_focusout_validation(self):

        valid = self._validate('','','', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid
    
    
class RequiredEntry(ValidatedMixin, ttk.Entry):
    
    def _focusout_validate(self, event):
        valid= True
        if not self.get():
            valid = False
            self.error.set('Field cannot be empty')
        return valid


class TtkSpinbox(ttk.Entry):

    def __init__(self, parent=None, **kwargs):

        super().__init__(parent, 'ttk::spinbox', **kwargs)


class ValidatedSpinbox(ValidatedMixin, TtkSpinbox):
    
    def __init__(self, *args, min_var=None, max_var=None, focus_update_var=None, 
                 from_='0', to='Infinity', **kwargs):

        super().__init__(*args, from_=from_, to=to, **kwargs)
        self.resolution = Decimal(str(kwargs.get('increment', '1.0')))
        self.precision = (self.resolution
                          .normalize()
                          .as_tuple()
                          .exponent)

    def _key_validate(self, char, index, current, proposed, action, **kwargs):

        valid=True
        min_val = self.cget('from')
        max_val=self.cget('to')
        no_negative = min_val >= 0
        no_decimal = self.precision >= 0
        
        if action == '0':
            return True
            
        if any([
                (char not in ('-1234567890.')),
                (char == '-' and (no_negative or index != '0')),
                (char == '.' and (no_decimal or '.' in current))]):
            return False
        
        if proposed in '-.':
            return True
        
        proposed = Decimal(proposed)
        proposed_precision = proposed.as_tuple().exponent
        
        if any([
                (proposed > max_val),
                (proposed_precision < self.precision)]):
            return False
        
        return valid
    
    def _focusout_validate(self, **kwargs):

        valid = True
        value = self.get()
        min_val = self.cget('from')
        max_val = self.cget('to')
        
        try:
            value = Decimal(value)
        except InvalidOperation:
            self.error.set('Invalid number string: {}'.format(value))
            return False
        
        if value < min_val:
            self.error.set('Value is too low(min {})'.format(min_val))
            valid = False
        
        if value > max_val:
            self.error.set('Value is too high (max {})'.format(max_val))
            valid = False
        
        return valid
    
    
class LabelInput(tk.Frame):
    
    field_types = {
            FT.string: (RequiredEntry, tk.StringVar),
            FT.iso_date_string : (RequiredEntry, tk.StringVar),
            FT.long_string: (tk.Text, lambda: None),
            FT.decimal: (ValidatedSpinbox, tk.DoubleVar),
            FT.integer: (ValidatedSpinbox, tk.IntVar),
            FT.boolean: (ttk.Checkbutton, tk.BooleanVar)
            }
    
    def __init__(self, parent, label='', input_class=None, input_var=None,
                 input_args=None, label_args=None, field_spec=None, **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)[0]
            var_type = self.field_types.get(field_type)[1]
            self.variable = input_var if input_var else var_type()
            
            if 'min' in field_spec and 'from_' not in input_args:
                input_args['from_'] = field_spec.get('min')
            if 'max' in field_spec and 'to' not in input_args:
                input_args['to'] = field_spec.get('max')
            if 'inc' in field_spec and 'increment' not in input_args:
                input_args['increment'] = field_spec.get('inc')   
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')
        else:
            self.variable = input_var
        
        if input_class in (ttk.Button, ttk.Checkbutton, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = self.variable
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = self.variable
            
        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)
        
        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable=self.error, **label_args)
        self.error_label.grid(row=2, column=0, sticky=(tk.W + tk.E))
        
    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)
        
    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ''
        
    def	set(self, value, *args,	**kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args,	**kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0',tk.END)
            self.input.insert('1.0', value)
        else:

            self.input.delete(0, tk.END)
            self.input.insert(0, value)