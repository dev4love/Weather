# coding: utf8
import ConfigParser
import os


class ConfParser:
    def __init__(self, path):
        self.path = path

    def getConf(self, section, option):
        result = {
            u'code': -1,
            u'msg': u'',
            u'value': u''
        }

        parser = ConfigParser.ConfigParser()
        parser.read(self.path)
        try:
            value = parser.get(section, option)
            result[u'code'] = 200
            result[u'value'] = value
            result[u'msg'] = u'success'

        except ConfigParser.NoOptionError, err:
            result[u'code'] = 404
            result[u'msg'] = err.message

        return result


if __name__ == '__main__':
    print(os.path.abspath(u'../conf.ini'))
    parser = ConfParser(u'../conf.ini')
    print parser.getConf(u'url', u'search')
