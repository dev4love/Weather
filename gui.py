# coding: utf-8
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
    from Tkinter import scrolledtext
    from Tkinter import messagebox
else:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import scrolledtext
    from tkinter import messagebox
    from tkinter.simpledialog import askinteger

from bs4 import BeautifulSoup, Tag

from threading import Thread

from core.weather import WeatherAPI
from conf_parser import Parser


class APP:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title(u'Assistant')
        self.win.iconbitmap(r'./res/app.ico')

        self.api = WeatherAPI(Parser())

        self.createWidget()

    def createWidget(self):
        label1 = ttk.Label(self.win, text=u'请输入城市名:')
        label1.grid(sticky=tk.W, row=0, column=0)

        self.cityName = tk.StringVar()
        searchBox = ttk.Entry(self.win, width=12, textvariable=self.cityName)
        searchBox.grid(sticky=u'WE', row=0, column=1)
        searchBox.focus()

        searchBtn = ttk.Button(self.win, text=u'Search', command=self._searchBtn)
        searchBtn.grid(sticky=u'WE', row=1, columnspan=2)

        self.info = scrolledtext.ScrolledText(self.win, width=60, height=15, wrap=tk.WORD)
        self.info.grid(column=0, sticky=u'WE', columnspan=2)

    def _searchBtn(self):
        searchThread = Thread(target=self._searchCity)
        searchThread.setDaemon(True)
        searchThread.start()

    def _searchCity(self):
        self.info.delete(u'1.0', tk.END)

        _cityName = self.cityName.get()
        if len(_cityName) == 0:
            messagebox.showwarning(u'Please input a city name', u'Please input a city name for search.')
            return

        cities = self.api.queryCityInfo(_cityName)
        # print(cities)
        if len(cities) == 0:
            messagebox.showerror(u'没有查询到城市', u'没有查询到城市，请检查输入！')
            return
        elif len(cities) == 1:
            self._showWeather(cities[0])

        else:
            self._askForSelect(cities)

    def _showWeather(self, city):
        self.info.insert(tk.INSERT, u'正在为您查询 #%s, %s# 的天气...\n\n\n' % (
            city.get(u'city_name_ch'), city.get(u'parent_name_ch')))

        weather_content = self.api.getWeather(city.get(u'id'))
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

    def _askForSelect(self, cities):
        title = u'Please select a city by number'
        msg = ''
        for no in range(len(cities)):
            city = cities[no]
            msg += '(%d) %s\n' % (no, self._prettyShow(city))

        # FIX: TclError: window ".34672232" was deleted before its visibility changed
        t_root = tk.Tk()
        t_root.withdraw()
        no = askinteger(parent=t_root, title=title, prompt=msg)
        # no = askinteger(title=title, prompt=msg)
        if no:
            self._showWeather(cities[no])

    def _prettyShow(self, city):
        return u'%s, %s' % (city.get(u'city_name_ch'), city.get(u'parent_name_ch'))


app = APP()
app.win.mainloop()
