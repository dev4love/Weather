# coding: utf-8
import sys

if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
    from Tkinter import scrolledtext
else:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import scrolledtext
    from tkinter import messagebox

from bs4 import BeautifulSoup, NavigableString, Tag
from core.weather import WeatherAPI
from core.conf import ConfParser


class APP:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title(u'Assistant')
        self.win.iconbitmap(r'res/app.ico')

        self.api = WeatherAPI(ConfParser(u'conf.ini'))

        self.createWidget()

    def createWidget(self):

        label1 = ttk.Label(self.win, text='请输入城市名:')
        label1.grid(sticky=tk.W, column=0, row=0)

        self.cityName = tk.StringVar()
        searchBox = ttk.Entry(self.win, width=12, textvariable=self.cityName)
        searchBox.grid(sticky=tk.W, column=0, row=1)

        searchBtn = ttk.Button(self.win, text='Search', command=self._searchCity)
        searchBtn.grid(column=1, row=1)

        self.info = scrolledtext.ScrolledText(self.win, width=60, height=15, wrap=tk.WORD)
        self.info.grid(column=0, sticky='WE', columnspan=2)

    def _searchCity(self):
        _cityName = self.cityName.get()
        if len(_cityName) == 0:
            messagebox.showwarning(u'please input a city name', u'please input a city name for search.')
            return
        else:
            cities = self.api.queryCityInfo(_cityName)
            print(cities)
            if len(cities) == 0:
                messagebox.showerror(u'没有查询到城市！')
                return

            self._shwoWeather(cities[0].get(u'id'))

    def _shwoWeather(self, cityId):
        weather_content = self.api.getWeather(cityId)
        soup = BeautifulSoup(weather_content, u'html.parser')

        table_tag = soup.find_all(u'table', class_=u'sevendays')[0]
        for child in table_tag.children:
            if not isinstance(child, Tag):
                continue

            date = child.find(u'td', class_=u'date').get_text()
            temp = child.find(u'td', class_=u'temp').get_text()
            desc = child.find(u'td', class_=u'desc').get_text()

            self.info.insert(tk.INSERT, ''.join(date.split()) + '\n')
            self.info.insert(tk.INSERT, ''.join(temp.split()) + '\n')
            self.info.insert(tk.INSERT, ''.join(desc.split()) + '\n')
            self.info.insert(tk.INSERT, u'=================' + '\n')


app = APP()
app.win.mainloop()
