# coding: utf8
import os
import sys

if sys.version_info < (3,):
    import ConfigParser as cp
else:
    import configparser as cp

prjDir = os.path.split(os.path.realpath(__file__))[0]
conf_path = os.path.join(prjDir, u'conf.ini')
print(conf_path)


class Parser:
    def __init__(self):
        self.path = conf_path

    def getConf(self, section, option):
        result = {
            u'code': -1,
            u'msg': u'',
            u'value': u''
        }

        parser = cp.ConfigParser()
        parser.read(self.path)
        try:
            value = parser.get(section, option)
            result[u'code'] = 200
            result[u'value'] = value
            result[u'msg'] = u'success'

        except cp.NoOptionError as err:
            result[u'code'] = 404
            result[u'msg'] = err.message

        return result


if __name__ == '__main__':
    parser = Parser()
    print(parser.getConf(u'url', u'search'))
