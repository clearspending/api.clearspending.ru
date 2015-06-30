# -*- coding: utf-8 -*-
import re
import hashlib
import logging

from tornado.web import RequestHandler
import tornado.web

from common.settings import DEBUG, MEMCACHE_ENABLED
from common.query_settings import APIdict

if MEMCACHE_ENABLED:
    from api.db_selectors import mc

_asciire = re.compile('([\x00-\x7f]+)')


def _is_unicode(x):
    return isinstance(x, unicode)


_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a + b, chr(int(a + b, 16)))
                 for a in _hexdig for b in _hexdig)


def unquote(input_str):
    """unquote('abc%20def') -> 'abc def'."""
    if _is_unicode(input_str):
        if '%' not in input_str:
            return input_str
        bits = _asciire.split(input_str)
        res = [bits[0]]
        append = res.append
        for i in range(1, len(bits), 2):
            append(unquote(str(bits[i])).decode('utf-8'))
            append(bits[i + 1])
        return ''.join(res)

    bits = input_str.split('%')
    # fastpath
    if len(bits) == 1:
        return input_str
    res = [bits[0]]
    append = res.append
    for item in bits[1:]:
        try:
            append(_hextochr[item[:2]])
            append(item[2:])
        except KeyError:
            append('%')
            append(item)
    return ''.join(res)


class MainHandler(RequestHandler):
    def get(self):
        self.write("ClearSpending.ru API v3")


class InvalidRequestHandler(RequestHandler):
    def get(self, query_str, resource_name, method_name):
        self.write(u"Invalid request.")


class AllHandler(RequestHandler):
    def get(self, query_str):
        print query_str
        self.write("api ")
        self.write(query_str)


def parse_returnfields(fields_string):
    '''
    Преобразует параметр запроса, содержащий список запрашиваемых полей, в словарь запрашиваемых полей вида
    {'название': u'значение'}
    '''
    fields_dict = None
    try:
        fields = unicode(fields_string).replace(u"[", u"").replace(u"]", u"").replace(u"{", u"").replace(u"}",
                                                                                                         u"").strip()
        if fields <> "":
            fields_dict = dict(map(lambda f: (f.strip(), 1), (field for field in fields.split(","))))
    except:
        fields_dict = None
    return fields_dict


def parse_pameters(parameters):
    '''
    Преобразует get-параметры запроса в словарь параметров вида {'название': u'значение'...}.
    :param parameters: строка вида u'название1=значение1&название2=значение2'
    :return: словарь вида {u'название1': u'значение1', u'название2': u'значение2'}
    '''
    parametersDict = dict(map(lambda p: (p.split("=", 2)[0], p.split("=", 2)[1]),
                              (parameter for parameter in parameters.strip().split("&"))))
    returnfields = parametersDict.get("returnfields")
    if returnfields <> None: parametersDict["returnfields"] = parse_returnfields(returnfields)
    return parametersDict


class ApiV2Handler(RequestHandler):
    @tornado.web.asynchronous
    def get(self, query_str, resource_name, method_name):
        parameters = unquote(unicode(self.request.query))
        query_str = unquote(unicode(query_str)) + parameters
        if DEBUG:
            self.real_get_handler(query_str, resource_name, method_name, parameters)
            return
        try:
            self.real_get_handler(query_str, resource_name, method_name, parameters)
        except Exception as e:
            self.set_status(500)
            self.finish(u"Invalid request.")
            logging.warning('Invalid request: %s' % query_str)
            logging.warning('Invalid request: %s \n resourceName: %s, methodName: %s, parameters: %s' % (
                query_str, resource_name, method_name, parameters))
            logging.warning('Exception: %s' % str(e))

    def real_get_handler(self, query_str, resource_name, method_name, parameters):
        '''
        Основной обработчик запросов c get-параметрами.
        :param query_str: URL-путь вместе с get-параметрами
        :param resource_name: название коллекции
        :param method_name:
        :param parameters: строка вида u'название1=значение1&название2=значение2'
        '''
        if MEMCACHE_ENABLED:
            mc_key = hashlib.sha224(query_str.encode("UTF-8").replace(" ", "%20")).hexdigest()
            data_str = mc.get(mc_key)
            if data_str:
                self.set_header("Content-Type", "application/json")
                self.finish(data_str)
                return None
        parameters_for_db_query = parse_pameters(parameters)
        parameters_for_db_query["queryStr"] = query_str
        parameters_for_db_query["resourceName"] = resource_name
        parameters_for_db_query["methodName"] = method_name
        f_data = APIdict[method_name][resource_name]["function"]
        data_str = f_data(parameters_for_db_query)
        if data_str:
            format = parameters_for_db_query.get('format', 'json')
            if 'csv' in format:
                self.set_header("Content-Type", "text/csv")
            elif 'xls' in format:
                self.set_header("Content-Type", "application/vnd.ms-excel")
            else:
                self.set_header("Content-Type", "application/json")
            self.finish(data_str)
            # Cache record will expired after 12 hours
            if MEMCACHE_ENABLED:
                mc.set(mc_key, data_str, time=43200)
        else:
            self.set_status(404)
            self.finish(u"Data not found.")
