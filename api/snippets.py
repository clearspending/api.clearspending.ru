# coding=utf-8
import re
from bson import objectid, ObjectId
import datetime


def str_key_from_dict(key_row, item):
    if '.' in key_row:
        for key in key_row.split('.'):
            if isinstance(item, dict):
                item = item.get(key, '')
            elif isinstance(item, list):
                return ''
            elif isinstance(item, str):
                return item
        return item
    else:
        value = item.get(key_row, None)

        if isinstance(value, list) or isinstance(value, dict):
            return ''
        elif isinstance(value, unicode):
            return value
        elif isinstance(value, float):
            return unicode(value)
        elif isinstance(value, datetime.datetime):
            return unicode(value)
        else:
            return ''


def delete_item_in_list(li, item):
    try:
        li.pop(li.index(item))
    except ValueError:
        return False


def dbid(val):
    """
    преобразует строку,полученную из апи в id базы монго
    """
    try:
        return objectid.ObjectId(str(val))
    except:
        return None


def isFloat(val):
    """
    проверяет является ли строка вещественным числом
    """
    try:
        if len(val) < 1: return False
        if val.isdigit(): return True
        if val.count(u".") > 1: return False
        if val.count(".") > 1: return False
        if val.replace(u".", u"").isdigit(): return True
        if val.replace(".", "").isdigit(): return True
    except:
        return False


def asIs(val):
    return val


def okdp_okpd(value):
    """
    поиск в двух колонках одновременно
    """
    if re.match("^[0-9.]+$", value):
        return {"$or": [{"products.OKDP.code": value}, {"products.OKPD.code": value}]}
    else:
        return None


def yearfilter(field, val):
    """
    преобразует строку, полученную из апи в диапазон дат для селекта в монге
    """
    try:
        if val <> None and int(val) > 1900 and int(val) < 2100:
            return [{field: {"$gte": datetime.datetime(int(val), 1, 1)}},
                    {field: {"$lt": datetime.datetime(int(val) + 1, 1, 1)}}]
        else:
            return None
    except:
        return None


def placingtype(val, params):
    """
    единый поавщик в базе кодов обозначен как EP44
    Но его нужно искать в другом месте.
    """
    if re.match("^[A-Za-z0-9,_-]*$", val):
        if ',' in val:
            return {u"$in": map(lambda get_param: get_param.strip(), (field for field in val.split(",")))}
        elif "SC" in val:
            params['field'] = "foundation.singleCustomer"
            return "true"
        else:
            return val


def dateRange(val):
    """
    преобразует строку, полученную из апи в диапазон дат для селекта в монге
    """
    if len(val) <> 21: return None
    try:
        yearStart = int(val[6:10])
        monthStart = int(val[3:5])
        dayStart = int(val[0:2])
        yearEnd = int(val[17:21])
        monthEnd = int(val[14:16])
        dayEnd = int(val[11:13])
        return {"$gte": datetime.datetime(yearStart, monthStart, dayStart),
                "$lt": datetime.datetime(yearEnd, monthEnd, dayEnd) + datetime.timedelta(days=1)}
    except:
        return None

def less_int(val):
    if val.isdigit():
        return {"$lte": int(val)}

def floatRange(val):
    """
    преобразует строку, полученную из апи в диапазон вещественных чисел для селекта в монге
    """
    try:
        val = val.replace(u",", u".")
        try:
            minNumber, maxNumber = val.split(u"-")
        except:
            if isFloat(val):
                minNumber = val
                maxNumber = ""
            else:
                return None
        if isFloat(minNumber) and isFloat(maxNumber):
            if minNumber < 0 or maxNumber < 0: return None
            if minNumber > maxNumber: minNumber, maxNumber = maxNumber, minNumber
            return {"$gte": float(minNumber), "$lte": float(maxNumber)}
        elif isFloat(minNumber) and not isFloat(maxNumber):
            if minNumber < 0: return None
            return {"$gte": float(minNumber)}
        elif not isFloat(minNumber) and isFloat(maxNumber):
            if maxNumber < 0: return None
            return {"$lte": float(maxNumber)}
    except:
        return None


def toListAnd(fieldsString):
    """
    преобразует строку, полученную из апи в список "И" для селекта в монге
    """
    fieldsDict = None
    try:
        fields = unicode(fieldsString).replace(u"[", u"").replace(u"]", u"").replace(u"{", u"").replace(u"}",
                                                                                                        u"").replace(
            u"+", u"").strip()
        if fields <> "": fieldsDict = {u"$all": map(lambda f: f.strip(), (field for field in fields.split(",")))}
    except:
        fieldsDict = None
    return fieldsDict


def toListOr(fieldsString):
    """
    преобразует строку, полученную из апи в список "ИЛИ" для селекта в монге
    """
    fieldsDict = None
    try:
        fields = unicode(fieldsString).replace(u"[", u"").replace(u"]", u"").replace(u"{", u"").replace(u"}",
                                                                                                        u"").replace(
            u"+", u"").strip()
        if fields <> "": fieldsDict = {u"$in": map(lambda f: f.strip(), (field for field in fields.split(",")))}
    except:
        fieldsDict = None
    return fieldsDict


def is_guid(value):
    """
    проверяет на наличие только [a-zA-z/-]
    """
    if re.match("^[A-Za-z0-9_-]*$", value):
        return value
    return None


def unicode_whitespace(value):
    return value.replace("+", " ") if value else None


def mongo_id(value):
    """
    проверяет на наличие только [a-zA-z/-]
    """
    if re.match("^[A-Za-z0-9_-]*$", value):
        return ObjectId(value)
    return None


def toList(fieldsString):
    """
    преобразует строку, полученную из апи в список
    """
    fieldList = None
    try:
        fields = unicode(fieldsString).replace(u"[", u"").replace(u"]", u"").replace(u"{", u"").replace(u"}",
                                                                                                        u"").replace(
            u"+", u"").strip()
        if fields <> "": fieldList = map(lambda f: f.strip(), (field for field in fields.split(",")))
    except:
        fieldList = None
    return fieldList


def booleaniator(val):
    """
    преобразует строку, полученную из апи в булево значение
    """
    if isinstance(val, bool): return val
    trueVals = ["1", "true", "yes", "on", "y", "t"]
    falseVals = ["0", "false", "no", "off", "n", "f"]
    try:
        if val.lower() in trueVals:
            return True
        elif val.lower() in falseVals:
            return False
        else:
            return None
    except:
        return None


def dthandler(obj):
    """
    если на входе datetime, то преобразует в ИСО формат дату
    """
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))


def lookahead(iterable):
    """
    :param iterable:  коллекция для итерирования
    :return: элемент, позиция(1 - первый, '-1' - последний)

    doctest:
    >>> [i for i in lookahead([])]
    []

    >>> [i for i in lookahead([1,2,3,4])]
    [(1, 1), (2, 0), (3, 0), (4, -1)]
    """
    it = iter(iterable)
    yield it.next(), 1
    last = it.next() # next(it) in Python 3
    for val in it:
        yield last, 0
        last = val
    yield last, -1