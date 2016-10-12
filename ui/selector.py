import tkinter as tk
from tkinter import ttk


class SelectDialog(object):
    root = None

    def __init__(self, cities, selected):
        self.top = tk.Toplevel(SelectDialog.root)

        self.cities = cities

        frame = tk.Frame(self.top, width=100, relief='ridge')
        frame.grid()


        for se in range(len(cities)):
            cityRadio = tk.Radiobutton(frame, text=self._prettyShow(cities[se]), variable=selected, value=se,
                                       command=self._chooseCity)
            cityRadio.grid(sticky=tk.W, row=se, column=0)

    def _prettyShow(self, city):
        return u'%s, %s' % (city.get(u'city_name_ch'), city.get(u'parent_name_ch'))

    def _chooseCity(self):
        # se = self.selected.get()
        # print(self.cities[se])
        self.top.destroy()
















        #
        #
        #     frm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        #     frm.pack(fill='both', expand=True)
        #
        #     label = tk.Label(frm, text=msg)
        #     label.pack(padx=4, pady=4)
        #
        #     caller_wants_an_entry = dict_key is not None
        #
        #     if caller_wants_an_entry:
        #         self.entry = tk.Entry(frm)
        #         self.entry.pack(pady=4)
        #
        #         b_submit = tk.Button(frm, text='Submit')
        #         b_submit['command'] = lambda: self.entry_to_dict(dict_key)
        #         b_submit.pack()
        #
        #     b_cancel = tk.Button(frm, text='Cancel')
        #     b_cancel['command'] = self.top.destroy
        #     b_cancel.pack(padx=4, pady=4)
        #
        # def entry_to_dict(self, dict_key):
        #     data = self.entry.get()
        #     if data:
        #         d, key = dict_key
        #         d[key] = data
        #         self.top.destroy()
