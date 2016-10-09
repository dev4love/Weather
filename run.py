# coding: utf8
from bs4 import BeautifulSoup, NavigableString, Tag

from core.conf import ConfParser
from core.weather import WeatherAPI

api = WeatherAPI(ConfParser(u'conf.ini'))


def show_weather(cityinfo):
    print(u'正在为您查询 #%s,%s# 的天气...' % (cityinfo.get(u'parent_name_ch'), cityinfo.get(u'city_name_ch')))
    weather_content = api.getWeather(cityinfo.get(u'id'))
    soup = BeautifulSoup(weather_content, u'html.parser')
    # print(soup.prettify())
    # print(soup.title)
    table_tag = soup.find_all(u'table', class_=u'sevendays')[0]
    for child in table_tag.children:
        if not isinstance(child, Tag):
            continue

        date = child.find(u'td', class_=u'date').get_text()
        temp = child.find(u'td', class_=u'temp').get_text()
        desc = child.find(u'td', class_=u'desc').get_text()
        print(''.join(date.split()))
        print(''.join(temp.split()))
        print(''.join(desc.split()))
        print(u'=================')


def choose_city(citysinfo, index):
    try:
        index = int(index)
        if 0 <= index < len(citysinfo):
            cityinfo = citysinfo[index]
            show_weather(cityinfo)
        else:
            index = input('请输入正确的数字编号:')
            choose_city(citysinfo, index)
    except:
        index = input('请输入正确的数字编号:')
        choose_city(citysinfo, index)


def accept_input():
    city_name = input('请输入希望查询的城市名或拼音:')
    citysinfo = api.queryCityInfo(city_name)
    if len(citysinfo) > 0:
        if len(citysinfo) == 1:
            city_info = citysinfo[0]
            show_weather(city_info)
        else:
            print('为您查询到以下几个城市,请选择:')
            temp = '(%d) %s,%s'
            count = 0
            for city in citysinfo:
                print(temp % (count, city.get(u'city_name_ch'), city.get(u'parent_name_ch')))
                count += 1

            index = input(u'\n>')
            choose_city(citysinfo, index)
    else:
        print('没有查询到相关城市!')
        accept_input()


if __name__ == '__main__':
    accept_input()
