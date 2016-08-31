# coding: utf8
"""
This module is designed for parse the weather data
"""
from conf import ConfParser

import requests

headers = {
    u'User-Agent': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0'
}


class WeatherAPI:
    def __init__(self, confParser):
        self.session = requests.Session()

        self.confParser = confParser

    def queryCityInfo(self, city):
        """
        city name or pinyin
        :param city:
        :return:
        """
        data = {u'q': city}

        result = self.confParser.getConf(u'url', u'search')

        if result.get(u'code') == 200:
            url = result.get(u'value')
            response = self.session.post(url, data=data)
            # print(response.text)
            return response.json()
        else:
            print(u'Serach Error: %s', result.get(u'msg'))

    def getWeather(self, cityId):
        data = {u'id': cityId}

        result = self.confParser.getConf(u'url', u'weather')

        if result.get(u'code') == 200:
            url = result.get(u'value')
            response = self.session.post(url, data=data)
            return response.content


if __name__ == '__main__':
    api = WeatherAPI(ConfParser(u'../conf.ini'))
    cityinfo = api.queryCityInfo(u'纽约')
    print api.getWeather(cityinfo[0].get(u'id'))
